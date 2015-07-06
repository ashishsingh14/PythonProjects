import time, zmq;

def start_server():
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5555")
    
    while(True):
        message = socket.recv()
        print("Received message from the client %s\n" % message)
        time.sleep(1)
        socket.send(b"hello world")


if __name__ == '__main__':
    start_server()