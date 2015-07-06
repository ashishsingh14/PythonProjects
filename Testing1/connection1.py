import sys
import imaplib
import getpass
import email
import email.header
import datetime
from pprint import pprint
import re, os
from hashlib import sha256


list_response_pattern = re.compile(r'\((?P<flags>.*?)\) "(?P<delimiter>.*)" (?P<name>.*)')
detach_dir = '.'
def open_connection(verbose=False):
    # Connect to the server
    #hostname = raw_input('IMAP4 Server Hostname: ')
    if verbose: print 'Connecting to IMAP server'
    connection = imaplib.IMAP4_SSL('173.37.183.72')

    # Login to our account
    #username = raw_input('IMAP4 Username: ')
    #password = raw_input('IMAP4 Password: ')
    if verbose: print 'Logging in as Ashish'
    connection.login('ashissi3', 'gamma1414$')
    return connection

def parse_list_response(line):
    flags, delimiter, mailbox_name = list_response_pattern.match(line).groups()
    mailbox_name = mailbox_name.strip('"')
    return (flags, delimiter, mailbox_name)


def status_mailbox(c,mailbox_name):
    print c.status(mailbox_name, '(MESSAGES RECENT UIDNEXT UIDVALIDITY UNSEEN)')

def select_mailbox(c,mailbox_name):
    status, data = c.select(mailbox_name,readonly=True)
    if(status=='OK'):
        num_messages = int(data[0])
        print "Number of messages are " , num_messages

    status, msg_ids = c.search(None, 'ALL')
    if(status=='OK'):
        print "In search", mailbox_name, msg_ids
        uids = msg_ids[0].split()
        print uids

    """
    print 'HEADER:'
    typ, msg_data = c.fetch('5', '(BODY.PEEK[HEADER])')
    for response_part in msg_data:
        if isinstance(response_part, tuple):
            print response_part[1]"""
    
    print 'BODY TEXT:'
    typ, msg_data = c.fetch(uids[-1], "(RFC822)")
    print msg_data

    """
    for response_part in msg_data:
        if isinstance(response_part, tuple):
            print response_part[1]"""

    mail = email.message_from_string(msg_data[0][1])

    if mail.get_content_maintype() == 'multipart':
        for part in mail.walk():
            # multipart are just containers, so we skip them
            if part.get_content_maintype() == 'multipart':
                continue

            # is this part an attachment ?
            if part.get('Content-Disposition') is None:
                continue
            
            # if there is no filename, we create one with a counter to avoid duplicates
            filename = part.get_filename()
            att_path = os.path.join(detach_dir, filename)

            print "payload in the memory\n", part.get_payload(decode=True)
            print "\n"

            if not os.path.isfile(att_path):
                fp = open(filename, 'wb')
                fp.write(part.get_payload(decode=True))
                fp.close()
            calculate_hashfile(filename)

def calculate_hashstring(input):
    chunk_size = 1024
    input_hash = sha256()
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
    print "Hash of the string is:\n"
    print file_sha256_checksum.hexdigest()


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


def list_mailboxes(c):
    typ, data = c.list()
    print 'Response code:', typ
    print 'Response:'
    pprint(data)

    for line in data:
        flags, delimiter, mailbox_name = parse_list_response(line)
        print 'Parsed response:', mailbox_name
    #status_mailbox(c,'Drafts')

if __name__ == '__main__':
    c = open_connection(verbose=True)
    try:
        print c
        list_mailboxes(c)
        select_mailbox(c,'Drafts')
    finally:
        c.logout()