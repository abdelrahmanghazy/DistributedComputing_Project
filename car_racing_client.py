# This file defines the client for the car racing game.
# Import the network and car racing classes.
from car_racing_network import Network
from car_racing import CarRacing
# Define a function to run the game.
def run_game():
    
    n = Network()# Create a network connection object.
    player = int(n.get_p())  # Get the player ID from the server.
    print("You are player:", player) # Print the player ID.
    
    game = CarRacing(n, player) # Create a car racing object.
    game.run_car() # Run the car racing game.

if __name__ == "__main__": # If this file is being run as the main file, run the game.
    run_game()
