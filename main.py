import cmd
import argparse
import shlex

from common.man import *
from sundries.color import banner
from sundries import color

version = 0.1
author = "Knuckles"

man = Man('punsssst')
Threads = []
class main(cmd.Cmd):
	def __init__(self):
		cmd.Cmd.__init__(self,completekey='tab')
		self.prompt = color.setcolor('$ ',color='red')
	def do_list(self,arg):
		man.list()
	def do_loadDB(self, arg):
		man.load()
	def do_kill(self,arg):
		parser = argparse.ArgumentParser(description="I am bored")
		parser.add_argument("-s",'--sess',help="sess", required=True)
		try:
			args = vars(parser.parse_args(shlex.split(arg)))
			man.killSess(int(args['sess']))
		except:
			return
		#print "Loading %s" % args['file']
	def do_loadfile(self,arg):
		parser = argparse.ArgumentParser(description="I am bored")
		parser.add_argument("-f",'--file',help="file", required=True)
		try:
			args = vars(parser.parse_args(shlex.split(arg)))
			Threads.append(Thread(target=man.loadfile, args=(args['file'],)).start())
		except:
			return
		#print "Loading %s" % args['file']
		
	def do_connect(self,arg):
		parser = argparse.ArgumentParser(description="I am bored")
		parser.add_argument("-i",'--id',help="id", required=True)
		try:
			args = vars(parser.parse_args(shlex.split(arg)))
			man.load(ID=int(args['id']))
		except:
			return

	def do_execute(self, arg):
		parser = argparse.ArgumentParser(description="I am bored")
		parser.add_argument("-s",'--sess',help="sess", required=True)
		parser.add_argument("-c",'--cmd', help="cmd", required=True)
		try:
			args = vars(parser.parse_args(shlex.split(arg)))
			if 'all' not in args['sess']:
				Threads.append(Thread( target=man.execute, args=(int(args['sess']), args['cmd'],None,None)).start())
			else:
				Threads.append(Thread(target=man.execute_all, args=(args['cmd'],)).start())
		except:
			return

	def do_dumpDB(self,args):
		man.dumpDB()
	def emptyline(self):
		man.updateDB()
	def do_exit(self, line):
		#for i in Threads: i.join()
		man.updateDB()
		sys.exit()
		return True
	def do_addhost(self, arg):
		parser = argparse.ArgumentParser(description="I am bored")
		parser.add_argument("-H",'--host',help="Host", required=True)
		parser.add_argument("-P",'--port', help="Port")
		parser.add_argument("-u",'--user', help="User")
		parser.add_argument("-p",'--pass', help="Pass")
		try:
			args = vars(parser.parse_args(shlex.split(arg)))
			host = args['host']
			port = int(args['port']) if args['port'] else 23
			user = args['user'] if  args['user'] else ''
			pword = args['pass'] if args['pass'] else ''
			Threads.append(Thread( target=man.addHost, args=(host,port,user,pword,)).start())
		except: return

	def do_EOF(self, line):
		man.updateDB()
		sys.exit()
		return True


if __name__ == '__main__':
	main().cmdloop(banner(version,author))
