#!/bin/python3

from connection import Connection 
from sandbox import Sandbox
from listener import Listener

# just an old good main.py
# it contains a menu interface, as i have spend too much time threading and socketing
# may be next version will fix it...

connection = Connection('127.0.0.1',55556)
connection.start()
sandbox = Sandbox()
listener = Listener(connection, sandbox)

server_is_running = False

def command():

    print("* * * Superchat server 0.01 * * *")
    print("Available commands: 'start' | 'kick' | 'show all' | 'exit'")

    global server_is_running
    #global listener
    while True:

        command = input(">>> ")

        if command == "start":
            if server_is_running == False:
                server_is_running = True
                listener.start()
            else:
                print("The server was started earlier.")

        elif (command == "stop") | (command == "exit"):
            listener.stop()
            print("Bye.")
            break

        elif (command == "drop") | (command == "kick"):
            if server_is_running == True:
                if sandbox.get_len() == 0:
                    print ("Nobody to kick.")
                else: 
                    index = 0
                    for participant in sandbox.get_participants():
                        index += 1
                        print(f"{index} - {participant.get_nickname()}")
                    victim = sandbox.get_participants()[int(input("Enter the number of the user to be kicked: "))-1]
                    victim.kill()
            else:
                print("Server is not running")

        elif (command == "show all"):
            if server_is_running == True:
                if sandbox.get_len() == 0:
                    print ("Nobody is on the server.")
                else: 
                    index = 0
                    for participant in sandbox.get_participants():
                        index += 1
                        print(f"{index} - {participant.get_nickname()}")
            else:
                print("Server is not running")

        else:
            print("Wrong command!")


if __name__ == "__main__":
    command()

