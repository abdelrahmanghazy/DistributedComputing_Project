import random
import pygame
import sys
import time


def parseMessage(message):
    
    out = message
    if(type(message) == list):
        if(type(message[1]) == list):
            flatten_list = [i for sublist in message for i in sublist]
        else:
            flatten_list = message
        out = '\n'.join(flatten_list) 

    messages = out.split('\n')
    return messages

class CarRacing:
    def __init__(self, network, player):
        pygame.init()

        self.network = network
        self.player = player
        self.display_width = 800
        self.display_height = 600
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.clock = pygame.time.Clock()
        self.gameDisplay = None
        pygame.font.init()  # you need to call this at the start if you want to use this module
        self.font = pygame.font.Font(None, 24)  # Font object (Font to use, size in pixels, optional)
        self.chat_messages = []
        self.current_chat_message = ""

        self.initialize()

    def initialize(self):
        self.crashed = False

        self.carImg = pygame.image.load('/Users/macbookair/Downloads/CSE_354/SourceCode/img/car.png')
        self.car_x_coordinate = [(self.display_width * 0.45), (self.display_width * 0.55)] # x coordinates for player 0 and 1
        self.car_y_coordinate = (self.display_height * 0.8)
        self.car_width = 49

        self.enemy_car = pygame.image.load('/Users/macbookair/Downloads/CSE_354/SourceCode/img/enemy_car_1.png')
        self.enemy_car_startx = random.randrange(310, 450)
        self.enemy_car_starty = -600
        self.enemy_car_speed = 5
        self.enemy_car_width = 49
        self.enemy_car_height = 100

        self.bgImg = pygame.image.load('/Users/macbookair/Downloads/CSE_354/SourceCode/img/back_ground.png')
        self.bg_x1 = (self.display_width / 2) - (360 / 2)
        self.bg_x2 = (self.display_width / 2) - (360 / 2)
        self.bg_y1 = 0
        self.bg_y2 = -600
        self.bg_speed = 3
        self.count = 0

    def car(self, car_x_coordinate, car_y_coordinate):
        self.gameDisplay.blit(self.carImg, (car_x_coordinate, int(car_y_coordinate)))



    def run_car(self):
        self.gameDisplay = pygame.display.set_mode((self.display_width, self.display_height))
        pygame.display.set_caption("Player" + " " + str(self.player + 1))

        while not self.crashed:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.network.send(f"quit,{self.player}\n")
                    self.display_message("YOU LOST!!")

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.car_x_coordinate[self.player] -= 50
                    if event.key == pygame.K_RIGHT:
                        self.car_x_coordinate[self.player] += 50
                    elif event.key == pygame.K_RETURN:  # Handle chat event when Return key is pressed
                        self.handle_chat_event(event)
                    elif event.key == pygame.K_BACKSPACE:  # Handle backspace event
                        self.handle_chat_event(event)
                    else:
                        self.handle_chat_event(event)

            game_state = self.network.send(f"update,{self.player},{self.car_x_coordinate[self.player]}\n")
            self.update_state(game_state["game_state"])
            self.enemy_car_startx = game_state["enemy_car_state"]["startx"]
            self.enemy_car_starty = game_state["enemy_car_state"]["starty"]
            self.enemy_car_speed = game_state["enemy_car_state"]["speed"]

            self.gameDisplay.fill(self.black)
            self.back_ground_road()
            self.run_enemy_car(self.enemy_car_startx, self.enemy_car_starty)
            self.enemy_car_starty += self.enemy_car_speed

            

            self.car(self.car_x_coordinate[0], self.car_y_coordinate)
            self.car(self.car_x_coordinate[1], self.car_y_coordinate)

            self.highscore(self.count)
            self.count += 1
            if (self.count % 100 == 0):
                self.enemy_car_speed += 1
                self.bg_speed += 1
            if self.car_y_coordinate < self.enemy_car_starty + self.enemy_car_height:
                if self.car_x_coordinate[0] > self.enemy_car_startx and self.car_x_coordinate[0] < self.enemy_car_startx + self.enemy_car_width or self.car_x_coordinate[0]+ self.car_width > self.enemy_car_startx and self.car_x_coordinate[0] + self.car_width < self.enemy_car_startx + self.enemy_car_width:
                    self.crashed = False
                    self.display_message("Player 2 WINS !!!")

            if self.car_x_coordinate[0]< 310 or self.car_x_coordinate[0] > 460:
                self.crashed = False
                self.display_message("Player 2 WINS!!!")
            
            if self.car_y_coordinate < self.enemy_car_starty + self.enemy_car_height:
                if self.car_x_coordinate[1] > self.enemy_car_startx and self.car_x_coordinate[1] < self.enemy_car_startx + self.enemy_car_width or self.car_x_coordinate[1]+ self.car_width > self.enemy_car_startx and self.car_x_coordinate[1] + self.car_width < self.enemy_car_startx + self.enemy_car_width:
                    self.crashed = False
                    self.display_message("Player 1 WINS !!!")

            if self.car_x_coordinate[1]< 310 or self.car_x_coordinate[1] > 460:
                self.crashed = False
                self.display_message("Player 1 WINS !!!")
            self.draw_chat()
            pygame.display.update()
            self.clock.tick(60)

    def draw_chat(self):
        y = 10
        for message in self.chat_messages[-10:]:  # only display the last 10 messages
            text = self.font.render(message, True, self.white)
            self.gameDisplay.blit(text, (610, y))
            y += text.get_height()

        # draw the current chat message
        text = self.font.render(self.current_chat_message, True, self.white)
        self.gameDisplay.blit(text, (610, y))

    def handle_chat_event(self, event):
        if event.key == pygame.K_RETURN:
            if self.current_chat_message:
                if self.player == 1:
                    self.current_chat_message = "Player 2: " + self.current_chat_message
                else:
                    self.current_chat_message = "Player 1: " + self.current_chat_message
                self.network.send_chat(self.current_chat_message)
                self.current_chat_message = ""
        elif event.key == pygame.K_BACKSPACE:
            self.current_chat_message = self.current_chat_message[:-1]
        else:
            self.current_chat_message += event.unicode


    def display_message(self, msg):
        font = pygame.font.SysFont("comicsansms", 72, True)
        text = font.render(msg, True, (255, 255, 255))
        self.gameDisplay.blit(text, (400 - text.get_width() // 2, 240 - text.get_height() // 2))
        self.display_credit()
        pygame.display.update()
        self.clock.tick(60)
        pygame.time.wait(2000)
        pygame.quit()


    def update_state(self, game_state):
        if game_state is not None:
            if game_state == "win":
                self.display_message("YOU WON!!")
            else:
                try:
                    messages = parseMessage(game_state)
                    for game_state in messages:
                        if game_state.startswith("update"):
                            splitted = game_state.split(",")
                            player, x_coordinate = int(splitted[1]), float(splitted[2])
                            self.car_x_coordinate[player] = x_coordinate
                        elif game_state.startswith("quit"):
                            player = int(game_state.split(",")[1])
                            self.display_message("Player {} WON!!!".format(player + 1))
                        elif game_state.startswith("chat"):
                            chat_message = game_state.split(",", 1)[1]
                            self.chat_messages.append(chat_message)
                except KeyError as e:
                    print("Error updating game state:", e)




    def back_ground_road(self):
        self.gameDisplay.blit(self.bgImg, (self.bg_x1, self.bg_y1))
        self.gameDisplay.blit(self.bgImg, (self.bg_x2, self.bg_y2))

        self.bg_y1 += self.bg_speed
        self.bg_y2 += self.bg_speed

        if self.bg_y1 >= self.display_height:
            self.bg_y1 = -600

        if self.bg_y2 >= self.display_height:
            self.bg_y2 = -600

    def run_enemy_car(self, thingx, thingy):
        self.gameDisplay.blit(self.enemy_car, (thingx, thingy))

    def highscore(self, count):
        font = pygame.font.SysFont("arial", 20)
        text = font.render("Score : " + str(count), True, self.white)
        self.gameDisplay.blit(text, (0, 0))

    def display_credit(self):
        font = pygame.font.SysFont("lucidaconsole", 14)
        text = font.render("Thanks for playing!", True, self.white)
        self.gameDisplay.blit(text, (600, 520))
