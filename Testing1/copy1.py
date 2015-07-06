import os, sys
import socket
from thread import *
import imaplib
import getpass
import email
import email.header
import datetime
from pprint import pprint
from hashlib import sha256
import quopri, re
max_connection = 20
buffer_size = 8192
listening_port = 9999

list_response_pattern = re.compile(r'\((?P<flags>.*?)\) "(?P<delimiter>.*)" (?P<name>.*)')

def parse_list_response(line):
    flags, delimiter, mailbox_name = list_response_pattern.match(line).groups()
    mailbox_name = mailbox_name.strip('"')
    return mailbox_name


def calculate_hashfile(filename):
    print "Calculating the hash of the file"
    chunk_size = 1024
    file_sha256_checksum = sha256()
    try:
        with open(filename, "rb") as f:
            byte = f.read(chunk_size)
            previous_byte = byte
            byte_size = len(byte)
            file_read_iterations = 1
            while byte:
                file_sha256_checksum.update(byte)
                previous_byte = byte
                byte = f.read(chunk_size)
                byte_size += len(byte)
                file_read_iterations += 1
    except IOError:
        print ('File could not be opened: %s' % (filename))
        #exit()
        return
    print "Hash of the file is:\n"
    print file_sha256_checksum.hexdigest()

def select_mailbox(conn,c,mailbox_name):
    status, data = c.select(mailbox_name,readonly=True)
    if(status=='OK'):
        num_messages = int(data[0])
        print "Number of messages are " , num_messages

    status, msg_ids = c.search(None, 'ALL')
    if(status=='OK'):
        print "In search", mailbox_name, msg_ids
        uids = msg_ids[0].split()
        print uids

    for i in range(len(uids)):
        typ, msg_data = c.fetch(uids[i], "(RFC822)")
        #print msg_data

        mail = email.message_from_string(msg_data[0][1])
        decode = email.header.decode_header(mail['Subject'])[0]
        subject = unicode(decode[0])
        #tosend = quopri.decodestring(mail)
        #print '\ntosend \n', tosend
        conn.send(subject)
        if mail.get_content_maintype() == 'multipart':
            for part in mail.walk():
                if part.get_content_maintype() == 'multipart':
                    continue            
                elif part.get_content_type() == 'text/plain':
                    body = part.get_payload(decode=False)
                    body = unicode(body)
                    conn.send(body)
                    print body
                if part.get('Content-Disposition') is None:
                    continue
                else:
                    attachment = part.get_payload(decode=False)
                    attachment = unicode(attachment)
                    filename = part.get_filename()
                    fp = open(filename, 'wb')
                    fp.write(part.get_payload(decode=True))
                    #calculate_hashfile(filename)
                    fp.close()
    c.logout()
    conn.close()

def print_allmailbox(conn, connection):
    mailbox_list = []
    try:
        typ, data = connection.list()
    except Exception, e:
        print e
    print 'Response code:', typ
    for line in data:
        name = parse_list_response(line)
        mailbox_list.append(name)

    i = 1
    for val in mailbox_list:
        s = str(i) + ":" + val
        print s
        i = i + 1
    print "\n"
    n = raw_input("Select the Mailbox Number: ")
    n = int(n)
    mailbox = mailbox_list[n-1]
    print "You selected this mailbox ", mailbox
    select_mailbox(conn, connection, mailbox)

def handle_request(conn, serverip, username, password, verbose=False):
    if verbose: 
        print 'Connecting to IMAP server ' + serverip
    connection = imaplib.IMAP4_SSL(serverip)
    if verbose: 
        print 'Logging in as %s\n' % username
    connection.login(username, password)
    print_allmailbox(conn, connection)
    #select_mailbox(conn, connection, 'Drafts')


def handle_connection(conn, data, addr):
    try:
        #ds = data.split(" ")
        #serverip = ds[0]
        #username = ds[1]
        #password = ds[2]
        print "Connected with client %s:%s" %(addr[0] , str(addr[1]))
        #print serverip, username, password
        handle_request(conn, '173.37.183.72','ashissi3','gamma1414$',verbose=True)
    except Exception, e:
        pass

def start():
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.bind(('',listening_port))
		s.listen(max_connection)
		print ("Starting Server on the port %d\n" % listening_port)
	except Exception, e:
		print "Unable to initialize socket\n"
		print e
		sys.exit(1)

	while True:
		try:
			conn, addr = s.accept()
			data = conn.recv(buffer_size)
			start_new_thread(handle_connection, (conn, data, addr))
		except KeyboardInterrupt:
			s.close()
			print "Proxy Server exiting\n"
			sys.exit(1)
	s.close()


if __name__ == '__main__':
 	start() 
