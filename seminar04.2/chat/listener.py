import threading
from participant import Participant

# this class listens for the new connections and wraps them into new threads
# some complications due to necessity to shut them down at any point in time

class Listener():

    def __init__(self, connection, sandbox):
        self.connection = connection
        self.sandbox = sandbox
        self._killed = threading.Event()
        self.thread = None

    def start(self):
        self.thread = threading.Thread(target=self.receive, args=())
        self.thread.start()
        print("Server is listening.")
        
    def receive(self):
        while not self._killed.is_set():
            # Accept Connection
            try:
                client, address = self.connection.socket.accept()
                #self.connection.socket.settimeout(None)
                print("Connected with {}".format(str(address)))
                # Request And Store Nickname
                client.send('NICK'.encode('utf-8'))
                nickname = client.recv(1024).decode('utf-8')
                # users[client] = nickname

                # Print And Broadcast Nickname
                # print("Nickname is {}".format(nickname))
                self.sandbox.broadcast("{} joined!".format(nickname))
                client.send('Connected to server!'.encode('utf-8'))

                # Start Handling Thread For Client
                participant = Participant(client, nickname, self.sandbox)
                participant.start()
                self.sandbox.add_participant(participant)
            except Exception: # to make it cancellable
                pass
   

    def stop(self):
        self._killed.set()
        if self.thread != None:
            self.thread.join()
        print("Listener was stopped.")
        self.connection.stop()
        #self.connection.shutdown(socket.SHUT_RDWR)
        #self.connection.close()
        self.sandbox.kill_all()
        
        