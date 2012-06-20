import pyuv
from guvnor import guvnor, Watcher
import socket as _real

class socket(_real.socket):
	def __init__(self, *args, **kwargs):
		_real.socket.__init__(self)
		if self.type = _real.SOCK_STREAM:
			self.handle = pyuv.TCP(guvnor.loop)
		else:
			raise TypeError("only tcp sockets are supported by guvnor")

		self.backlog = None

	def bind(self, address):
		self.handle.bind(address)

	def listen(self, backlog):
		self.backlog = backlog
	
	def accept(self):
		self.handle.listen(self.backlog, Watcher())
		guvnor.switch()

		client = socket()
	 	self.handle.accept(client.handle)
		return client

	def connect(self, address):
		

	def close(self):
		_real.socket.close(self)
		self.handle.close(Watcher())
		guvnor.switch()



def gethostbyname(hostname):
	guvnor.dns.gethostbyname(hostname, Watcher())
	return guvnor.switch()

def gethostbyaddr(ip_address):
	guvnor.dns.gethostbyaddr(ip_address, Watcher())
	return guvnor.switch()

def getnameinfo(sockaddr, flags):
	guvnor.dns.getnameinfo(*args, **kwargs)
	return guvnor.switch()

def getaddrinfo(host, port, family=0, type=0, proto=0, flags=0):
	guvnor.dns.getaddrinfo(host, Watcher(), port, family, type, proto, flags)
	return guvnor.switch()
