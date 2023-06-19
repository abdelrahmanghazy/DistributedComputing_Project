from _thread import *
import socket
import pickle
import random
# This class represents the server that will be hosting the game.
class Server:
    # Initialize the server with the server address and port number.
    def __init__(self):
        self.server = '172.19.128.1'
        self.port = 5555
        self.addr = (self.server, self.port)
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = []
        self.car_game_states = [[0, 0], [0, 0]]
        self.enemy_car_state = {"startx": random.randrange(310, 450), "starty": -600, "speed": 5}
 # This method starts the server and listens for connections.
    def start(self):
        self.s.bind(self.addr)
        self.s.listen(2)  # Listen for up to 2 connections
        print('Server Started. Waiting for connections...')
# This loop continuously accepts connections from clients.
        while True:
            conn, addr = self.s.accept()  # Accept a connection
            print(f'Connected to: {addr}')
            self.clients.append(conn)

 # Only start the game when 2 clients have connected.
            if len(self.clients) == 2:
                print("Starting game!")
                 # Create a new thread for each client and start it.
                for i in range(2):
                    start_new_thread(self.threaded_client, (self.clients[i], i))
# This method is called for each client that connects to the server.
    def threaded_client(self, conn, player):
        conn.send(str.encode(str(player)))
        reply = ""
# This loop continuously receives messages from the client.
        while True:
            try:  # Receive a message from the client.
                data = conn.recv(2048 * 2)
                reply = data.decode("utf-8")

                if not data: # If the message is empty, the client has disconnected.
                    print("Player", player, "disconnected")
                    break
                else: # Update the game state for the player.
                    if player == 0:
                        self.car_game_states[0] = reply
                    elif player == 1:
                        self.car_game_states[1] = reply
 # Update the position of the enemy car.
                    self.enemy_car_state["starty"] += self.enemy_car_state["speed"]
                    if self.enemy_car_state["starty"] > 600:  # Assuming 600 is the display height
                        self.enemy_car_state["starty"] = 0 - 100  # Assuming 100 is the enemy car height
                        self.enemy_car_state["startx"] = random.randrange(310, 450)
 # Send the updated game state to the client.            
                    if reply.startswith("chat,"):  # If the message starts with "chat," it is a chat message.
                        chat_message = reply.split(",", 1)[1]
                        if player == 0:
                            self.car_game_states[0] = reply
                            self.clients[1].sendall(pickle.dumps({"chat": chat_message, "game_state": self.car_game_states, "enemy_car_state": self.enemy_car_state}))
                        elif player == 1:
                            self.car_game_states[1] = reply
                            self.clients[0].sendall(pickle.dumps({"chat": chat_message, "game_state": self.car_game_states, "enemy_car_state": self.enemy_car_state}))
                    for connection in self.clients:
                        connection.sendall(pickle.dumps({"game_state": reply, "enemy_car_state": self.enemy_car_state}))

            except ConnectionResetError:
                print("Player", player, "disconnected")
                conn.close()
                self.clients.remove(conn)
                break



        # Check if the other player is still connected
        if len(self.clients) == 1:
            remaining_player = 0 if player == 1 else 1
            print("Player", remaining_player, "wins!")

            # Send winning message to the remaining player
            self.clients[0].sendall(
                pickle.dumps({"game_state": "win", "enemy_car_state": self.enemy_car_state})
            )

server = Server()
server.start()
