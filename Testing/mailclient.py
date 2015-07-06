import sys

from twisted.internet import protocol, defer, endpoints, task
from twisted.mail import imap4
from twisted.python import failure

@defer.inlineCallbacks
def main(reactor, username="ashissi3", password="gamma1414$",
         strport="ssl:host=173.37.183.72:port=993"):
    endpoint = endpoints.clientFromString(reactor, strport)
    factory = protocol.Factory()
    factory.protocol = imap4.IMAP4Client
    try:
        client = yield endpoint.connect(factory)
        yield client.login(username, password)
        yield client.select('INBOX')
        info = yield client.fetchEnvelope(imap4.MessageSet(1))
        print 'First message subject:', info[1]['ENVELOPE'][1]
    except:
        print "IMAP4 client interaction failed"
        failure.Failure().printTraceback()

# This API requires Twisted 12.3 or later, or a trunk checkout:
task.react(main, sys.argv[1:])