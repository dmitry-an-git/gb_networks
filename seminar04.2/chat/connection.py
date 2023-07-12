import socket

# this class opens a socket

class Connection():
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = None

    def start(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))
        self.socket.listen()
        self.socket.settimeout(1)
        # return self.server
    
    def stop(self):
        #self.socket.shutdown(socket.SHUT_RDWR)
        #self.socket.close()
        print("Socket was shut down")

