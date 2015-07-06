import sys
from twisted.internet import defer
from twisted.internet import protocol
from twisted.internet import reactor
from twisted.python import log
from twisted.protocols import basic
from twisted.internet import stdio
import imaplib
import getpass
import email
import email.header
import codecs


def tell_me_about(s): 
    return (type(s))

def file():
	f  = open('out.txt' , 'r')
	s = f.read()
	print tell_me_about(s)
	print s
	f.close()

class TrivialPrompter(basic.LineReceiver):
    from os import linesep as delimiter

    promptDeferred = None

    def prompt(self, msg):
        assert self.promptDeferred is None
        self.display(msg)
        self.promptDeferred = defer.Deferred()
        return self.promptDeferred

    def display(self, msg):
        self.transport.write(msg)

    def lineReceived(self, line):
        if self.promptDeferred is None:
            return
        d, self.promptDeferred = self.promptDeferred, None
        d.callback(line)

if __name__ == '__main__':
	tp = TrivialPrompter()
	stdio.StandardIO(tp)
	tp.display("HI ashish")





