#!/usr/bin/env python
# coding: utf-8
# http://musta.sh/2012-03-04/twisted-tcp-proxy.html

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

class ProxyClientProtocol(basic.LineReceiver):
    def connectionMade(self):
        log.msg("Client: connected to peer")
        self.cli_queue = self.factory.cli_queue
        self.cli_queue.get().addCallback(self.serverDataReceived)
        self.setRawMode()

    def serverDataReceived(self, chunk):
        if chunk is False:
            self.cli_queue = None
            log.msg("Client: disconnecting from peer")
            self.factory.continueTrying = False
            self.transport.loseConnection()
        elif self.cli_queue:
            log.msg("Client: writing %d bytes to peer" % len(chunk))
            self.transport.write(chunk)
            self.cli_queue.get().addCallback(self.serverDataReceived)
        else:
            self.factory.cli_queue.put(chunk)

    def rawDataReceived(self, chunk):
        #print chunk
        log.msg("Client: %d bytes received from peer" % len(chunk))
        f = open('out.txt', 'wa')
        f.write(chunk)
        f.close()
        self.factory.srv_queue.put(chunk)

    def lineReceived(self, chunk):
        print "message from the server",chunk

    """
    def dataReceived(self, chunk):
        log.msg("Client: %d bytes received from peer" % len(chunk))
        #mail = email.message_from_string(chunk[0][1])
        #print chunk
        #log.msg(chunk)
        #log.msg("Type of chunk")
        #log.msg(tell_me_about(chunk))
        #s1 = chunk.decode('ISO-8859-1')
        #f = open('out.txt', 'wa')
        #f.write(chunk)
        #f.close()
        self.factory.srv_queue.put(chunk)"""

    def connectionLost(self, why):
        if self.cli_queue:
            self.cli_queue = None
            log.msg("Client: peer disconnected unexpectedly")


class ProxyClientFactory(protocol.ReconnectingClientFactory):
    maxDelay = 10
    continueTrying = True
    protocol = ProxyClientProtocol

    def __init__(self, srv_queue, cli_queue):
        self.srv_queue = srv_queue
        self.cli_queue = cli_queue

class ProxyServer(protocol.Protocol):
    def connectionMade(self):
        self.srv_queue = defer.DeferredQueue()
        self.cli_queue = defer.DeferredQueue()
        self.srv_queue.get().addCallback(self.clientDataReceived)

        factory = ProxyClientFactory(self.srv_queue, self.cli_queue)
        reactor.connectTCP("173.37.183.72", 143, factory)

    def clientDataReceived(self, chunk):
        log.msg("Server: writing %d bytes to original client" % len(chunk))
        self.transport.write(chunk)
        self.srv_queue.get().addCallback(self.clientDataReceived)

    def dataReceived(self, chunk):
        log.msg("Server: %d bytes received" % len(chunk))
        log.msg("data from client ", chunk)
        self.cli_queue.put(chunk)

    def connectionLost(self, why):
        self.cli_queue.put(False)

if __name__ == "__main__":
    log.startLogging(sys.stdout)
    factory = protocol.Factory()
    factory.protocol = ProxyServer
    reactor.listenTCP(9888, factory)
    reactor.run()