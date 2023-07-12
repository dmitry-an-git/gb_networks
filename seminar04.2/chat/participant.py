import threading
import socket

# each new participant is a separate thread. Threads contain a reference to the sandbox and can communicate 
# both ways. They call a checker function after threading events are set, so the sandbox can keep the 
# list of active threads up to date. Also I have made all eternal while cycles to be splitable (by timeout), 
# so threads dont freeze listening to the socket.

class Participant(threading.Thread):
    def __init__(self, client, nickname, sandbox):
        super().__init__()
        self._killed = threading.Event()
        self._disconnected = threading.Event()
        self.client = client
        self.nickname = nickname
        self.sandbox = sandbox

    def run(self):
        self.client.settimeout(1)
        while True:

            if self._killed.is_set():
                self.client.close()
                self.sandbox.checker()
                break

            try:
                # Broadcasting Messages
                message = self.client.recv(1024).decode('utf-8')
                self.sandbox.broadcast(message)
                if len(message) == 0:
                    raise Exception

            except socket.timeout:
                # To make the connection killable
                continue

            except:
                # Removing And Closing Clients
                self.sandbox.broadcast('{} left!'.format(self.nickname))
                self._disconnected.set()
                self.client.close()
                self.sandbox.checker()
                break
            
            
    def send(self, message):
        self.client.send(message.encode('utf-8'))

    def kill(self):
        self.sandbox.broadcast('{} has been kicked!'.format(self.nickname))
        self._killed.set()

    def get_nickname(self):
        return self.nickname
    
    def disconnected(self):
        return self._disconnected.is_set()
            
    def killed(self):
        return self._killed.is_set()