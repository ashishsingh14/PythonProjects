import socket, sys

def server():
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
	#host = socket.gethostname()
	port = 12345
	host = ''
	s.bind((host, port))
	s.listen(5)

	while True:
		c, addr = s.accept()
		print " The Host name is ", addr
		c.send("Thanks for connecting")
		c.close()

if __name__ == '__main__':
  server()
	