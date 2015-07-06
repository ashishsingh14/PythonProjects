from twisted.web import proxy, http
from twisted.internet import reactor
from twisted.python import log
import sys
from twisted.internet import protocol, ssl
from twisted.internet import defer
from twisted.internet import stdio
from twisted.mail import imap4
from twisted.protocols import basic
from twisted.python import util

log.startLogging(sys.stdout)

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

class IMAP4ProxyServer(imap4.IMAP4Server):
	def rawDataReceived(self, data):
		stdout.write("Data from the client")


class IMAP4ProxyServerFactory(protocol.ServerFactory):
	def buildProtocol(self, addr):	
		return IMAP4ProxyServer()

class ProxyFactory(http.HTTPFactory):
    protocol = proxy.Proxy



if __name__ == '__main__':
	reactor.listenTCP(9000, IMAP4ProxyServerFactory())
	reactor.run()

