import socket

def client():
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	host = '127.0.0.1'
	port = 12345
	s.connect(host , port)
	print s.recv(1024)
	s.close()

if '__name__' == '__main__':
	client()