from twisted.internet import reactor, protocol
from twisted.python import log
import sys
log.startLogging(sys.stdout)
class EchoClient(protocol.Protocol):
   def connectionMade(self):
       self.transport.write("Hello, world!")

   def dataReceived(self, data):
       print "Server said:", data
       self.transport.loseConnection()

class EchoFactory(protocol.ClientFactory):
   def buildProtocol(self, addr):
       return EchoClient()

   def clientConnectionFailed(self, connector, reason):
       print "Connection failed."
       reactor.stop()

   def clientConnectionLost(self, connector, reason):
       print "Connection lost."
       reactor.stop() 

if __name__ == '__main__':
  reactor.connectTCP("localhost", 9000, EchoFactory(), 3)
  reactor.run()

