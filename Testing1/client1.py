import os, sys, socket
import quopri
import getpass
proxyhostname = '127.0.0.1'
port = 9999
buffer_size = 8192

def send_request():
	try:		
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)		
		#payload = '173.37.183.72' + ' ' + 'ashissi3' + ' ' + 'gamma1414$'
		hostname = raw_input('IMAP4 Server Hostname: ')
		username = raw_input('IMAP4 Username: ')
		password = getpass.getpass()
		payload = hostname + ' ' + username + ' ' + password
		s.connect((proxyhostname, port))
		s.send(payload)
		while True:
			datafromserver = s.recv(buffer_size)
			#datafromserver = quopri.encodestring(datafromserver)
			if not datafromserver: break
			print "Data from Server\n", datafromserver
		s.close()
	except Exception, e:
		print "Unable to initialize socket\n"
		print e
		sys.exit(1)

if __name__ == '__main__':
	send_request()