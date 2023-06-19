# car_racing_network.py

import socket
import pickle
# This class represents the network connection between the client and the server.
class Network:
    def __init__(self): # Initialize the network connection with the server address and port number.
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "192.168.1.130" # The IP address of the server.
        self.port = 5555 # The port number of the server.
        self.addr = (self.server, self.port)
        self.p = self.connect() # The player ID, received from the server.

 # Get the player ID.
    def get_p(self):
        return self.p
 # Connect to the server.
    def connect(self):
        try:  # Try to connect to the server.
            self.client.connect(self.addr) # Receive the player ID from the server.
            return self.client.recv(2048).decode() 
         # If the connection fails, print an error message.
        except:
            pass
 # Send data to the server.
    def send(self, data):
        try: 
            self.client.send(str.encode(data)) # Send the data to the server.
            return pickle.loads(self.client.recv(2048*2)) # Receive the response from the server.
        except socket.error as e:
            print(e)
 # Send a chat message to the server.           
    def send_chat(self, message):
        try:
            self.client.send(str.encode("chat," + message + "\n"))  # Send the chat message to the server.
            return pickle.loads(self.client.recv(2048*2)) # Receive the response from the server.
        except socket.error as e:
            print(e)


