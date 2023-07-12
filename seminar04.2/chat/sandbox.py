
# the sandbox is where all the threads-participants are contained. When they are dropping or being kicked 
# the sandbox updates its state accordingly. It can also kill-kick them all.

class Sandbox():
    def __init__(self):
        self.participants = []

    def get_participants(self):
        return self.participants
    
    def add_participant(self, participant):
        self.participants.append(participant)
    
    def remove_participant(self, participant):
        self.participants.remove(participant)

    def broadcast(self, message):
        for participant in self.participants:
            participant.send(message)
        print(message)

    def checker(self):
        for participant in self.participants:
            if participant.disconnected() or participant.killed():
                self.participants.remove(participant)
                # participant.join() # will it kill them?

    def get_len(self):
        return len(self.participants)
    
    def kill_all(self):
        for participant in self.participants:
            participant.kill()
        self.checker()
