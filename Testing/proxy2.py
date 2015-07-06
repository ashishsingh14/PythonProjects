import sys,os
from twisted.protocols.portforward import ProxyFactory
from twisted.protocols.portforward import ProxyClientFactory
from twisted.protocols.portforward import ProxyClient
from twisted.protocols.portforward import ProxyServer
from twisted.internet import protocol, reactor

from twisted.python import log
log.startLogging(sys.stdout)

class PS(ProxyServer):
    def dataReceived(self, data):
        print "PS->dataReceived(%s)" %repr(data)
        #print data
        return ProxyServer.dataReceived(self, data)


def main():
    from twisted.internet import reactor 
    pfactory = ProxyFactory('173.37.183.72',993)
    pfactory.protocol = PS
    reactor.listenTCP(9999, pfactory)
    reactor.run()
    
if __name__ == '__main__':
    main()