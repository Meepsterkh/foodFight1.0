import importlib
import pygame
import time
import random
import os
import unittest
from rooms import*

# start pygame
pygame.init()

# colors

white = (255, 255 ,255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 155, 0)
blue = (0, 0, 255)
orange = (255,69,0)

def center(num1, num2):
    return num1 + (num2 /2)

def percent(part, whole):
    return (part/whole) * 100


# setting up clock
clock = pygame.time.Clock()
FPS = 30

# running variables
running = True
gameOver = False

# import sprites
# Movement
stand = pygame.transform.scale(pygame.image.load("stand.png"), (100, 80))
forward1 = pygame.transform.scale(pygame.image.load("Forward1.png"), (100, 80))
forward2 = pygame.transform.scale(pygame.image.load("Forward2.png"), (100, 80))
left1 = pygame.transform.scale(pygame.image.load("left1.png"), (100, 80))
left2 = pygame.transform.scale(pygame.image.load("left2.png"), (100, 80))
left3 = pygame.transform.scale(pygame.image.load("left3.png"), (100, 80))
right1 = pygame.transform.scale(pygame.image.load("right1.png"), (100, 80))
right2 = pygame.transform.scale(pygame.image.load("right2.png"), (100, 80))
right3 = pygame.transform.scale(pygame.image.load("right3.png"), (100, 80))
back1 = pygame.transform.scale(pygame.image.load("up2.png"), (100, 80))
back2 = pygame.transform.scale(pygame.image.load("up1.png"), (100, 80))
back3 = pygame.transform.scale(pygame.image.load("up3.png"), (100, 80))
# Floor
g = pygame.transform.scale(pygame.image.load("grass.png"), (100, 100))
p = pygame.transform.scale(pygame.image.load("plank.png"), (100, 100))
t = pygame.transform.scale(pygame.image.load("tile.png"), (100, 100))
T = pygame.transform.scale(pygame.image.load("tilesF.png"), (100, 100))
tallGrass = pygame.transform.scale(pygame.image.load("tallGrass1.1.png"), (100, 100))
# Wall
wallW = pygame.transform.scale(pygame.image.load("wallWindow.png"), (300, 60))
wallB = pygame.transform.scale(pygame.image.load("wallBlank.png"), (300, 60))
wallDoor = pygame.transform.scale(pygame.image.load("wallDoor.png"), (300, 60))
wallC = pygame.transform.scale(pygame.image.load("wallCorner.png"), (280, 280))

wall = [wallB, wallW]

walkLeft = left2, left1, left2, left3, left2
walkRight = right2, right1, right2, right3, right2
walkForward = stand, forward1, stand, forward2, stand
walkBack = back1, back2, back1, back3, back1

class player(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.xChange = 0
        self.yChange = 0
        self.width = width
        self. height = height
        self.left = False
        self.right = False
        self.up = False
        self.down = False
        self.walkCount = 0
        self.align = 24
        self.speed = 5
        self.speedCheck = 1
        self.Food = [[20, 5, "Brain Freeze", 0], [10, 12, "Bite"], [40, 4, "Ketchup Leak", 1], [30, 7, "Pickle Toss", 0], 150]
        self.health = self.Food[4]
        self.original = self.Food[4]

    def draw(self, gameDisplay):
        if self.walkCount >= 16:
            self.walkCount = 0
 
        if self.left:
            gameDisplay.blit(walkLeft[self.walkCount // 4], (self.x - self.align, self.y))
            self.walkCount += 1
        if self.right:
            gameDisplay.blit(walkRight[self.walkCount // 4], (self.x - self.align, self.y))
            self.walkCount += 1
        if self.down:
            gameDisplay.blit(walkForward[self.walkCount // 4], (self.x - self.align, self.y))
            self.walkCount += 1
        if self.up:
            gameDisplay.blit(walkBack[self.walkCount // 4], (self.x - self.align, self.y))
            self.walkCount += 1

user = player(600, 300, 50, 77)

class world(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.walls = [random.randrange(2), random.randrange(2), random.randrange(2)]
        self.roomNum = 0
        self.roomType = 0

    def changeRoom(self, num, borders = 0, house = False):
        if house:
            if num == 0:
                if user.y < borders + 1 and user.x > 340 and user.x < 370:
                    user.y = (self.height - user.height) + 60
                    self.roomType += 1

            if num == 1:
                if user.x < borders + 1 and user.y > 240 and user.y < 270:
                    user.x = (self.width - user.width) - 60
                    self.roomNum += 1

            if num == 2:
                if user.y + user.height > self.height - borders and user.x > 340 and user.x < 370:
                    user.y = borders + 60
                    self.roomType -= 1

            if num == 3:
                if user.x + user.width > self.width - borders and user.y > 240 and user.y < 270:
                    user.x = borders + 60
                    self.roomNum -= 1

        else:
            if num == 0:
                if user.y < borders + 1 and user.x > 0 and user.x < self.width:
                    user.y = (self.height - user.height) +60
                    self.roomType += 1

            if num == 1:
                if user.x < borders + 1:
                    user.x = (self.width - user.width) -60
                    self.roomNum += 1

            if num == 2:
                if user.y + user.height > self.height - borders and user.x > 0 and user.x < self.width:
                    user.y = borders +60
                    self.roomType -= 1

            if num == 3:
                if user.x + user.width > self.width - borders and user.y > 0 and user.y < self.height:
                    user.x = borders +60
                    self.roomNum -= 1

        world.border(borders)

    def draw(self, gameDisplay, x, y, width, height):
        # Left
        if user.x + user.width > x and user.x < x - user.speed and user.y < height + y - user.speed and user.y + user.height > y + user.speed:
            user.x = x - user.width
        # Right
        if user.x > x + user.speed and user.x < x + width and user.y < height + y - user.speed and user.y + user.height > y + user.speed:
            user.x = x + width
        # Down
        if user.x + user.width > x + user.speed and user.x < x + width - user.speed and user.y < height + y and user.y > y + user.speed:
            user.y = y + height
        # Up
        if user.x + user.width > x + user.speed and user.x < x + width - user.speed and user.y < height + y - user.speed and user.y + user.height > y:
            user.y = y - user.height

        pygame.draw.rect(gameDisplay, black, [x, y, width, height])

    def room(self, gameDisplay, map):
        tiles = 0
        for column in range(6):
            for row in range(8):
                if map[tiles] == "t":
                    gameDisplay.blit(t, (row * 100, column * 100))
                if map[tiles] == "p":
                    gameDisplay.blit(p, (row * 100, column * 100))
                if map[tiles] == "g":
                    gameDisplay.blit(g, (row * 100, column * 100))
                if map[tiles] == "T":
                    gameDisplay.blit(T, (row * 100, column * 100))
                tiles += 1

    def border(self, border):
        if user.x < border:
            user.x = border
        if user.x > self.width - user.width - border:
            user.x = self.width - user.width - border
        if user.y < 0:
            user.y = 0
        if user.y > self.height - user.height - border:
            user.y = self.height - user.height - border


    def house(self, door, wall):
        world.changeRoom(door, 60, True)
        for i in range(3):
            win.blit(wall[self.walls[i]], (i * 300, 0))
        win.blit(wall[self.walls[1]], (300, 0))
        for i in range(3):
            win.blit(pygame.transform.rotate(wall[self.walls[i]], 90), (0, i * 300))
        win.blit(pygame.transform.rotate(wall[self.walls[1]], 90), (0, 300))
        for i in range(3):
            win.blit(pygame.transform.rotate(wall[self.walls[i]], 270), (self.width - 60, i *300))
        win.blit(pygame.transform.rotate(wall[self.walls[1]], 270), (self.width - 60, 300))
        for i in range(3):
            win.blit(pygame.transform.rotate(wall[self.walls[i]], 180), (i * 300, self.height - 60))
        win.blit(pygame.transform.rotate(wall[self.walls[1]], 180), (300, self.height - 60))

        win.blit(wallC, (self.width - 253, -31))
        win.blit(pygame.transform.rotate(wallC, 90), (-31, -27))
        win.blit(pygame.transform.rotate(wallC, 270), (self.width - 249, self.height - 253))
        win.blit(pygame.transform.rotate(wallC, 180), (-27, self.height - 249))

        if door == 0:
            win.blit(wallDoor, ((self.width/2) - 150, 0))
        elif door == 1:
            win.blit(pygame.transform.rotate(wallDoor, 90), (0, (self.height/2) - 150))
        elif door == 3:
            win.blit(pygame.transform.rotate(wallDoor, 270), (self.width - 60, (self.height/2) - 150))
        else:
            win.blit(pygame.transform.rotate(wallDoor, 180), ((self.width/2) - 150, self.height - 60))


world = world(0, 0, 800, 600)

win = pygame.display.set_mode((world.width, world.height))
pygame.display.set_caption("Food Fight")

def messageToScreen(msg, color, x, y, size):
    font = pygame.font.SysFont(None, size)
    text = font.render(msg, True, color)
    f = pygame.font.Font(None, size)
    t = pygame.compat.as_bytes(msg)
    width, height = f.size(t)
    win.blit(text,[x - (width/2) + 15, center(y, size)])

class food(object):
    def __init__(self):
        self.attack = False
        self.Enemy = pokemon.iceCream()
        self.moves = []
        self.move = pokemon.iceCream()
        self.health = self.move[4]
        self.original = self.move[4]

    class pokemon(object):
        def __init__(self):
            self.who = ["error", "error", "error", "error"]
            self.burger = pygame.transform.scale(pygame.image.load("burger.png"), (200, 200))
            self.icecream = pygame.transform.scale(pygame.image.load("iceCream.png"), (110, 110))

        def burger(self):
            health = 150
            move = ["error", "error", "error", "error", "error"]
            move1 = [20, 5, "Ham-Burgerler", 0]
            move2 = [10, 12, "Bite", 0]
            move3 = [40, 4, "Ketchup Leak", 1]
            move4 = [30, 7, "Pickle Toss", 0]
            move.insert(0, move1)
            move.insert(1, move2)
            move.insert(2, move3)
            move.insert(3, move4)
            move.insert(4, health)
            return move

        def iceCream(self):
            health = 100
            move = ["error", "error", "error", "error", "error"]
            move1 = [20, 5, "Brain Freeze", 0]
            move2 = [10, 12, "Bite", 0]
            move3 = [40, 4, "Ketchup Leak", 1]
            move4 = [30, 7, "Pickle Toss", 0]
            move.insert(0, move1)
            move.insert(1, move2)
            move.insert(2, move3)
            move.insert(3, move4)
            move.insert(4, health)
            return move

    def drawHP(self, place):
        if place == 0:
            pygame.draw.rect(win, black, [50, 330, 270, 65])
            pygame.draw.rect(win, white, [55, 335, 260, 55])
            messageToScreen("Burger", black, 220, 330, 35)
            messageToScreen("HP", green, 70, 340, 20)
            pygame.draw.rect(win, black, [50, 380, 270, 18])
            pygame.draw.rect(win, white, [55, 382, round(percent(user.health, user.original) * 2.6), 13])
            if user.health > 0:
                pygame.draw.rect(win, green, [55, 382, 260, 13])

        if place == 1:
            pygame.draw.rect(win, black, [500, 70, 270, 65])
            pygame.draw.rect(win, white, [505, 75, 260, 55])
            messageToScreen("iceCream", black, 670, 60, 35)
            messageToScreen("HP", green, 520, 80, 20)
            pygame.draw.rect(win, black, [500, 120, 270, 18])
            pygame.draw.rect(win, white, [505, 122, 260, 13])
            if self.health > 0:
                pygame.draw.rect(win, green, [505, 122, round(percent(self.health, self.original) * 2.6), 13])


pokemon = food.pokemon()
food = food()
# user.Food = pokemon.burger()

class moveSet(object):
    def __init__(self):
        self.moves = False

    def text(self, move1, move2, move3, move4):
        messageToScreen(move1, black, battle.LB + 60, battle.UB, 25)
        messageToScreen(move2, black, battle.LB + 60, battle.DB, 25)
        messageToScreen(move3, black, battle.RB + 60, battle.UB, 25)
        messageToScreen(move4, black, battle.RB + 60, battle.DB, 25)

    def attack(self, move, who = 0):
        if who == 1:
            if move[3] == 0:
                user.health -= move[0]
            elif move[3] == 1:
                food.health += move[0]
        else:
            if move[3] == 0:
                food.health -= move[0]
            elif move[3] == 1:
                user.health += move[0]

    def detect(self):
        if battle.enter == True:
            if battle.placeX == battle.LB:
                if battle.placeY == battle.UB:
                    self.attack(user.Food[0])
                    battle.wipe()
                else:
                    self.attack(user.Food[1])
                    battle.wipe()
            else:
                if battle.placeY == battle.UB:
                    self.attack(user.Food[2])
                    battle.wipe()
                else:
                    self.attack(user.Food[3])
                    battle.wipe()

    def movePage(self):
        if self.moves:
            battle.wipe()
            battle.hud()
            battle.ctrlB()
            battle.button()
            moveSet.text(user.Food[0][2], user.Food[1][2], user.Food[2][2], user.Food[3][2])
            moveSet.detect()

moveSet = moveSet()

class battle(object):
    def __init__(self):
        self.userNu = True
        self.hudLen = (world.height /3)
        self.hudY = self.hudLen + self.hudLen
        self.leftB = False
        self.rightB = False
        self.upB = False
        self.downB = False
        self.enter = False
        self.cancel = False
        self.RB = 500
        self.UB = 430
        self.LB = 150
        self.DB = 510
        self.placeX = self.LB
        self.placeY = self.UB
        self.combat = False
        self.stopTest = False
        self.mainSC = True
        self.randChance = random.randrange(5)
        self.playerTurn = True

    def reset(self):
        user.speed = 5
        self.userNu = True
        self.combat = False
        self.stopTest = False
        food.health = 150

    def wipe(self):
        if self.combat:
            user.speed = 0
            pygame.draw.rect(win, white, [0, 0, world.width, world.height])
            self.userNu = False
            pygame.draw.ellipse(win, black, [400, self.hudY - 90, 400, 120], 5)
            pygame.draw.ellipse(win, black, [100, 150, 200, 80], 2)
            battle.foods(200, 200)
            battle.enemyF(80, 80)

    def hud(self):
        pygame.draw.rect(win, black, [0, self.hudY, world.width, self.hudLen])
        pygame.draw.rect(win, white, [10, self.hudY +10, world.width -20, self.hudLen -20])

    def draw(self, color, x, y, sizeChange = 0):
        pygame.draw.rect(win, color, [x -sizeChange, y -sizeChange, 150 +(sizeChange*2), 60 +(sizeChange*2)])

    def ctrlB(self):
        if self.leftB:
            self.placeX = self.LB
        if self.rightB:
            self.placeX = self.RB
        if self.upB:
            self.placeY = self.UB
        if self.downB:
            self.placeY = self.DB

        battle.draw(red, self.placeX, self.placeY, 5)

    def foods(self, width, height):
        win.blit(pokemon.burger, (600 - (width/2), 330 - (height/2)))

    def enemyF(self, width, height):
        win.blit(pokemon.icecream, (205 - (width / 2), 175 - (height / 2)))

    def detect(self):
        if self.enter == True:
            if self.placeX == self.LB:
                if self.placeY == self.UB:
                    moveSet.moves = True
                    battle.mainSC = False
                else:
                    print("2")
            else:
                if self.placeY == self.UB:
                    print("3")
                else:
                    battle.reset()

    def button(self):
        battle.draw(black, self.LB, self.UB)
        battle.draw(black, self.LB, self.DB)
        battle.draw(black, self.RB, self.UB)
        battle.draw(black, self.RB, self.DB)
        battle.draw(white, self.LB, self.UB, -5)
        battle.draw(white, self.LB, self.DB, -5)
        battle.draw(white, self.RB, self.UB, -5)
        battle.draw(white, self.RB, self.DB, -5)

    def text(self):
        messageToScreen("Run", black, self.RB + 60, self.DB, 40)
        messageToScreen("Moves", black, self.LB + 60, self.UB, 40)
        messageToScreen("Foods", black, self.RB + 60, self.UB, 40)

    def display(self):
        battle.wipe()
        battle.hud()
        battle.ctrlB()
        battle.button()

    def Battle(self):
        self.combat = True
        if self.cancel:
            self.mainSC = True
            moveSet.moves = False

        if self.playerTurn:
            if self.mainSC:
                battle.display()
                battle.text()
                battle.detect()

            if moveSet.moves:
                moveSet.movePage()

        food.drawHP(0)
        food.drawHP(1)

        self.cancel = False
        battle.enter = False

        if food.health <= 0:
            battle.reset()

    def enemy(self, x, y, width, height):
        pygame.draw.rect(win, orange, [x, y, width, height])
        if user.x + user.width > x and user.x < x + width and user.y < height + y and y + user.height > y:
            battle.Battle()

    def grass(self, x, y):
        win.blit(tallGrass, (x, y))
        if user.x + user.width > x - user.speed and user.y < 50 + y - user.speed and user.y + user.height > y + user.speed and user.x < x +50 - user.speed:
            if self.randChance == 0:
                self.stopTest = True

battle = battle()

start_ticks = pygame.time.get_ticks()
#game loop function
def gameLoop():
    # movement variables

    global running, gameOver

    # loop for game
    while running:

        class timz(object):
            def __init__(self):
                self.seconds = (pygame.time.get_ticks() - start_ticks) / 1000

            def random(self):
                if round(timz.seconds) % 2 == 0:
                    battle.randChance = random.randrange(10)

        timz = timz()

        timz.random()
        # loop for gameover
        while gameOver == True:
            # draw background
            win.fill(white)
            pygame.display.update()

            # closing window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    gameOver = False

                # game over choice
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        running = False
                        gameOver = False
                    if event.key == pygame.K_c:
                        gameLoop()

        # key press detection
        for event in pygame.event.get():
            # window
            if event.type == pygame.QUIT:
                running = False

            # movement
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    user.xChange = -user.speed
                    user.left = True
                    battle.leftB = True
                    battle.rightB = False
                if event.key == pygame.K_RIGHT:
                    user.xChange = user.speed
                    user.right = True
                    battle.rightB = True
                    battle.leftB = False
                if event.key == pygame.K_UP:
                    user.yChange = -user.speed
                    user.up = True
                    battle.upB = True
                    battle.downB = False
                if event.key == pygame.K_DOWN:
                    user.yChange = user.speed
                    user.down = True
                    battle.downB = True
                    battle.upB = False

                if event.key == pygame.K_SPACE:
                    battle.enter = True
                if event.key == pygame.K_KP0:
                    battle.cancel = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    user.xChange = 0
                if event.key == pygame.K_RIGHT:
                    user.xChange = 0
                if event.key == pygame.K_UP:
                    user.yChange = 0
                if event.key == pygame.K_DOWN:
                    user.yChange = 0

        # change movement
        user.x += user.xChange
        user.y += user.yChange

        # rooms
        if world.roomNum == 0:
            world.room(win, homeBottom)
            world.house(1, wall)

        if world.roomNum == 1 and world.roomType == 0:
            world.room(win, grass)
            battle.grass(100, 100)
            battle.grass(100, 150)
            battle.grass(100, 200)
            battle.grass(100, 250)
            battle.grass(200, 100)
            battle.grass(200, 150)
            battle.grass(200, 200)
            battle.grass(200, 250)
            battle.grass(300, 200)
            world.changeRoom(3)
            world.changeRoom(1)

        if world.roomNum == 2 and world.roomType == 0:
            world.room(win, plank)
            world.changeRoom(3)


        #default Border
        if battle.stopTest:
            battle.Battle()

        # user sprite
        # pygame.draw.rect(win, black, [user.x, user.y, user.width, user.height])
        if battle.userNu:
            if user.xChange == 0 and user.yChange == 0:
                win.blit(stand, (user.x - user.align, user.y))
                user.right = False
                user.left = False
                user.up = False
                user.down = False

            if user.left:
                user.draw(win)
                user.right = False
                user.down = False
                user.up = False
            if user.right:
                user.draw(win)
                user.left = False
                user.own = False
                user.up = False
            if user.down:
                user.draw(win)
                user.right = False
                user.left = False
                user.up = False
            if user.up:
                user.draw(win)
                user.right = False
                user.down = False
                user.left = False



        print(food.health)

        # update screen
        pygame.display.update()

        # fps meter
        clock.tick(FPS)
    # close the window
    pygame.quit()
    quit()

# call the game
gameLoop()
