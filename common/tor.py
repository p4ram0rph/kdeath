import socket
import socks

class Tor(object):

	def __init__(self):
		#self.sockstuff()
		self.sock = socket.socket()
		self.s = socket.socket()
		socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 9050)
		socket.socket = socks.socksocket
		self.socket = socket.socket()


	def resetIP(self):
		for i in xrange(5):
			try:
				self.sock.connect(("127.0.0.1",9051))
				self.sock.send( "AUTHENTICATE\r\n" )
				self.sock.send( "SIGNAL NEWNYM\r\n" )
				self.sock.close()
				self.sock = self.s
				return self.newSock()
			except socket.error, e:
				print e
		return "Failed"
	def getIP(self):
		s = socket.socket()
		s.connect(("icanhazip.com",80))
		s.send("GET / \r\n")
		ip = s.recv(1024)
		s.close()

		return ip
	def newSock(self):
		self.socket = socket.socket()
		return self.socket
