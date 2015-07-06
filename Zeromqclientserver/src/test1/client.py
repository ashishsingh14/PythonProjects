import zmq;

def client_initiate():
    context = zmq.Context()
    print("Connecting to the server\n")
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5555")
    for request in range(10):
        print("Sending request\n")
        socket.send(b"Hello")
        message = socket.recv()
        print("Received message from the server is %s %s" %(request, message) )
    

if __name__ == '__main__':
    client_initiate()