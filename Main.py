#importing the nesescary librarys
import pygame
import eztext
from pygame.locals import *
import os
import sys
import random
import math
import time

from FileManager import FileManager

fileManager = FileManager("gameDatabase.db")

def weighted_choice(choices):  # function to weight the probability of certian tiles being generated
    total = sum(w for c, w in choices) #returns the total of all of the choices
    r = random.uniform(0, total) #returns a random number in the range of 0 to the total sum
    upto = 0
    for c, w in choices: #loops through every choice
        if upto + w >= r: #if the selected probabilty is greater than the random number
            return c #returns the weighted item in the array
        upto += w
    assert False, "Shouldn't get here" #for debugging purposes

def dist(x1, y1, x2, y2): #function to generate circle distances
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2) #pythagorases theorem

def generatePonds(numOfPonds): #generates the randomly positioned ponds
    for i in range(numOfPonds): #loops numOfPonds times
        r = random.randint(3, 7) #random radius of pond between 3 and 7
        cx = random.randint(0 + r, MAPHEIGHT - r)
        cy = random.randint(0 + r, MAPWIDTH - r)
        for x in range(cx - r, cx + r):
            for y in range(cy - r, cy + r):
                if dist(cx, cy, x, y) <= r:
                    tileMap[x][y][0] = WATER #appends pond tile to tile map array

def generateNpc(num, size):
    x = random.randint(0, MAPHEIGHT)
    y = random.randint(0, MAPWIDTH)
    if num % 2 == 0:
        for i in range(size):
            for j in range(size):
                tileMap[x + i][y + j][0] = WOOD

def generatePortal(): #function to randomly generate one portal per level
    x = random.randint(0, MAPWIDTH) #random x coord
    y = random.randint(1, MAPHEIGHT) #random y coord
    for i in range(len(tileMap)):
        for j in range(len(tileMap[i])):
            if i == y and j == x:
                if tileMap[i][j][0] != WATER: #makes sure the portal isn't generated on water
                    tileMap[i][j][0] = PORTAL #sets the specified tile to water
                else:
                    generatePortal() #generate new portal
            else:
                tileMap[i][j][1] = recourceValue[tileMap[i][j][0]]

def generateTileMap(): #generating the 2D tile array
    generateMonster(playerLevel) #first generating monsters
    # generating the tile map below
    global tileMap #setting the array variable global
    tileMap = [[[weighted_choice(tiles), 0] for i in range(MAPWIDTH)] for j in range(MAPHEIGHT)] #creating a 2D array in the size of the width and height specified
    generatePonds(random.randint(1, 6)) # generate ponds
    generateNpc(random.randint(0, 100), random.randint(3, 5)) #generate NPCs
    generatePortal() #generate portal

def renderEnviroment(): #function to render the tilemap
    for row in range(MAPHEIGHT):
        for column in range(MAPWIDTH):
            pygame.draw.rect(screen, colours[(tileMap[row][column])[0]],
                             (column * TILESIZE, row * TILESIZE, TILESIZE, TILESIZE)) #draw a rectangle for each item in the tile map with the specific colour
            screen.blit(font_player.render(str(tileMap[row][column][1]), True, (0, 0, 0)),
                        (column * TILESIZE, row * TILESIZE))
    pygame.draw.rect(screen, BLACK, (0, 0, TILESIZE * MAPWIDTH, TILESIZE)) #drawing a black menue bar at the top of the screen

def generateMonster(playerLevel): #generating monsters
    for i in range(random.randint(0,TILESIZE)): #random ammount of monsters
        monsterHealth = playerLevel*MONSTERHEALTH #monster health is relative to the player's level
        x=random.randint(0,MAPWIDTH)
        y=random.randint(0,MAPHEIGHT)
        monsters.append([x,y,monsterHealth]) #adding a monster to the monster array

def renderMonster(): #function to render monsters
    if len(monsters) > 0: #making sure the monster list isn't empty
        for i in range(len(monsters)): #looping through the monster array
            pygame.draw.rect(screen, PINK, ( monsters[i][0] * TILESIZE, monsters[i][1] * TILESIZE, TILESIZE, TILESIZE))  # rendering the monster
            screen.blit(font_monster.render(str(monsters[i][2]), True, (0, 0, 0)),(monsters[i][0] * TILESIZE, monsters[i][1] * TILESIZE))  # redering the monster health

def moveMonster(): #function to move each monster
    if len(monsters) > 0: #making sure the array isn't empty
        for i in range(len(monsters)): #looping through the monster array
            x = random.randint(-monsterMovementPoints, monsterMovementPoints)
            y = random.randint(-monsterMovementPoints, monsterMovementPoints)
            monsters[i] = [monsters[i][0] + x, monsters[i][1] + y, monsters[i][2]]

def monsterAttack(): #function to make the monster attack
    global playerHealth #making the playerHealth variable global so it can be accessed anywhere
    playerHealth = playerHealth - MONSTERATTACK #removing health off the player
    if playerHealth < 0: #check if the player is dead
        global died #making the dead variable global so it can be accessed anywhere
        died = True #setting the dead variable true so the game knows the player is dead

def renderPlayer(): #function to render the player and all related variables
    pygame.draw.rect(screen, RED, (playerx, playery, TILESIZE, TILESIZE))  # rendering the player
    screen.blit(font_player.render("health: "+str(playerHealth), True, (255, 255, 255)),(0, 0))  # redering the player health
    screen.blit(font_player.render("xp: " + str(xp), True, (255, 255, 255)),(100, 0))  # redering the player xp
    screen.blit(font_player.render("level: " + str(playerLevel), True, (255, 255, 255)), (150, 0))  # redering the player xp
    screen.blit(font_player.render("recource points: "+str(playerPoints), True, (255, 255, 255)),(300, 0))  # redering the player recource points
    screen.blit(font_player.render("iron: " + str(iron), True, (255, 255, 255)),(440, 0))  # redering the player iron
    screen.blit(font_player.render("water: " + str(water), True, (255, 255, 255)),(500, 0))  # redering the player water

def playerAttack(i): #function to make the player attack #i being the specific monster in the array
    monsters[i][2]=monsters[i][2]-playerAttackPoints #removing health from the indexed monster
    if monsters[i][2]==0: #checking if the monster is dead
        del monsters[i] #deleting the monster from the array
        global xp #making the player xp variable global so it can be accessed anywhere
        xp=xp+1 #incrementing the player xp variable by 1

def saveOptions():
    pygame.draw.rect(screen, WHITE, (width/2-(width/4), height/2-(height/4), width/2, height/2))
    pygame.draw.rect(screen, BLACK, (width / 2 - (width / 4), height / 2 - (height / 4), width / 2, height / 2), 5)

    screen.blit(font_saveOptions.render("SAVE GAME", True, (0, 0, 0)), ((width/2)-160, (height/2)-130))
    pygame.draw.rect(screen, (169, 169, 169), ((width / 2)+60, (height / 2) - 50, width / 16, height / 16))
    pygame.draw.rect(screen, BLACK, ((width / 2)+60, (height / 2)-50, width / 16, height / 16), 5)
    screen.blit(font_saveOptions.render("save", True, (0, 0, 0)), ((width / 2) - 125, (height / 2) - 50))

    screen.blit(font_saveOptions.render("LOAD GAME", True, (0, 0, 0)), ((width / 2) + 40, (height / 2) - 130))
    pygame.draw.rect(screen, (169, 169, 169), ((width / 2) - 140, (height / 2) - 50, width / 16, height / 16))
    pygame.draw.rect(screen, BLACK, ((width / 2) - 140, (height / 2) - 50, width / 16, height / 16), 5)
    screen.blit(font_saveOptions.render("load", True, (0, 0, 0)), ((width / 2) + 80, (height / 2) - 50))



    # fileManager = FileManager("gameDatabase.db")
    # name = input("username")
    # fileManager.saveGame(name, done)

#game dimenions
TILESIZE = 20 #the size in pixels of each square tile
MAPWIDTH = 60 #the ammount of tiles on the x axis
MAPHEIGHT = 30 #the ammount of tiles on the y axis

#tile values
DIRT = 0
STONE = 1
IRON = 2
WATER = 3
PORTAL = 4
WOOD = 5

tiles = [(STONE,5),(DIRT,0),(IRON,0.25),(WATER,0)]

recourceValue = {
    DIRT : 0,
    IRON : 3,
    STONE : 0,
    WATER : 1,
    WOOD : 4
}

#item ids
HEALTHPOTION = 0
ATTACKPOTION = 1
HELMET = 2
CHESTPLATE = 3
CHAPS = 4
BOOTS = 5
SWORD = 6


#colour RGB values
BLACK = (0,0,0)
GRAY = (168, 168, 168)
BROWN = (153,76,0)
IRONBROWN = (210,105,30)
GREEN = (92, 214, 94)
LIGHTGREEN = (66, 244, 98)
BLUE = (0,0,255)
RED = (255,0,0)
PINK = (255,0,255)
MAHOGANY = (103,10,10)
WHITE = (255,255,255)

colours = { #library linking each tile ID to a colour
    DIRT : BROWN,
    IRON : IRONBROWN,
    STONE: GRAY,
    WATER: BLUE,
    PORTAL: BLACK,
    WOOD: MAHOGANY
}

pygame.init() #initialise all imported PyGame modules

#set the screen size of the grid and making the window resizable
screen = pygame.display.set_mode((MAPWIDTH*TILESIZE, MAPHEIGHT*TILESIZE),pygame.RESIZABLE)

#inititalising fonts
font_player = pygame.font.SysFont('Arial', 15)
font_monster = pygame.font.SysFont('Arial', 10)
font_timer = pygame.font.SysFont('Arial', 50)
font_died = pygame.font.SysFont('Arial', 300)
font_saveOptions = pygame.font.SysFont('Arial', 25)

width, height = pygame.display.get_surface().get_size() #storing width and height of screen in variables
done = False #variable to be used when exiting
pause = False #variable to pause the game

CURSOR = Rect(0, 0, TILESIZE, TILESIZE) #initialising a rectangle to be used as a cursor

# x=0
# y=0

#main player variables
playerHealth = 100
playerAttackPoints = 50
playerPoints = 0
playerLevel = 1
movementPoints = 1
iron=0
water=0
xp=0
died = False

username = eztext.Input(maxlength=45, color=(255,0,0), prompt='username: ')

#monster variables
monsters = []
MONSTERHEALTH = 100
MONSTERATTACK = 30
monsterMovementPoints = 2
MOVEMONSTER = 3000
moveMonsterEvent = pygame.USEREVENT

clock = pygame.time.Clock()
pygame.time.set_timer(moveMonsterEvent, MOVEMONSTER)

generateTileMap()

playerx = random.randint(0,MAPWIDTH)*TILESIZE #giving the player a random x coord on the grid
playery = random.randint(0,MAPHEIGHT)*TILESIZE #giving the player a random x coord on the grid


while not done and died == False:
    clock.tick()
    #events = pygame.event.get()
    if died == True:
        screen.blit(font_died.render("YOU DIED", True, (0,0,0)), (0, 0))  #redering the player health
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == moveMonsterEvent:
            moveMonster()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                if pause == False:
                    saveOptions()
                pause = not pause



        if event.type == pygame.MOUSEBUTTONDOWN:
            (button1, button2, button3,) = pygame.mouse.get_pressed()  # get button pressed

            if pause == True:
                if button1:
                    if mousex > ((width / 2) - 125) and mousex < ((width / 2) - 75): #x bounds of save button
                        if mousey > ((height / 2) - 50) and mousey < ((height / 2) + 25): #y bounds of save button
                            print("saving...")
                            username = input("username")
                            fileManager.saveGame(username,playerHealth,done)
                    if mousex > ((width / 2) + 80) and mousex < ((width / 2) + 180): #x bounds of load button
                        if mousey > ((height / 2) - 50) and mousey < ((height / 2) + 25): #y bounds of load button
                            print("loading...")

            else: #only run if the game isn't paused
                if button1:
                    #move player
                    xDist = ((mousex - playerx) - TILESIZE / 2)#distance to travel
                    yDist = ((mousey - playery) - TILESIZE / 2)#distance to travel

                    xTilePos = (mousex-(TILESIZE/2))/TILESIZE
                    yTilePos = (mousey-(TILESIZE/2))/TILESIZE

                    if tileMap[int(yTilePos)][int(xTilePos)][0] != WATER: #making sure the player cant move onto water
                        # making sure the player can only move a certian distance per click
                        if abs(xDist // TILESIZE) > movementPoints:
                            if xDist > 0:
                                xDist = 2 * TILESIZE
                            else:
                                xDist = -(2 * TILESIZE)
                        if abs(yDist // TILESIZE) > movementPoints:
                            if yDist > 0:
                                yDist = 2 * TILESIZE
                            else:
                                yDist = -(2 * TILESIZE)

                        if tileMap[int((playery + yDist)//TILESIZE)][int((playerx + xDist)//TILESIZE)][0] != WATER: #making sure the player cant land on water/stone
                            #moving player
                            playerx = playerx + xDist
                            playery = playery + yDist
                            cursorColour = LIGHTGREEN
                            for i in range(len(monsters)): #checking if player is attacking monster
                                if monsters[i][0] == int(playerx/TILESIZE) and monsters[i][1] == int(playery/TILESIZE):
                                    playerAttack(i)
                                    monsterAttack()
                                    break

                    #indicating the player cannot move to the selected tile
                        elif tileMap[int((playery + yDist) // TILESIZE)][int((playerx + xDist) // TILESIZE)][0] == WATER:
                            cursorColour = RED
                    else:
                        cursorColour = RED


                    ## moving the player through portals
                    xTilePos = playerx / TILESIZE
                    yTilePos = playery / TILESIZE
                    if tileMap[int(yTilePos)][int(xTilePos)][0] == PORTAL:
                        del monsters[::]
                        generateTileMap()

                elif button3:

                    ##### GETTING TILE POSITIONS OF TILES AND PLAYER ###
                    xTilePos = (mousex - (TILESIZE / 2)) / TILESIZE
                    yTilePos = (mousey - (TILESIZE / 2)) / TILESIZE
                    xPlayerPos = (playerx //TILESIZE)
                    yPlayerPos = (playery //TILESIZE)

                    if -2 < xTilePos-xPlayerPos < 2 and -2 < yTilePos-yPlayerPos < 2:
                        if tileMap[int(yTilePos)][int(xTilePos)][1] > 0:
                            cursorColour=PINK
                            playerPoints=playerPoints+1 #adding player points
                            tileMap[int(yTilePos)][int(xTilePos)][1]=(tileMap[int(yTilePos)][int(xTilePos)][1])-1 #removing points from tile
                            if tileMap[int(yTilePos)][int(xTilePos)][0] == IRON: #adding points to iron stash
                                iron=iron+1
                            elif tileMap[int(yTilePos)][int(xTilePos)][0] == WATER: #adding points to iron stash
                                water=water+1

    if pause != True: #run the following code if the game isn't paused
        renderEnviroment() #call the function to render the enviroment
        renderPlayer() #call the function to render the player
        renderMonster() #call the function to render the monsters
        if xp == 10: #check if the player's xp level is 10
            playerLevel=playerLevel+1 #increment the player's level by 1
            xp=0 #reset the xp level back to 0

        ##### MOUSE LOGIC #####
        mousex,mousey = pygame.mouse.get_pos()
        mousex = mousex-(mousex%TILESIZE)+TILESIZE/2 #getting the x tile the mouse is on
        mousey = mousey-(mousey%TILESIZE)+TILESIZE/2 #getting the y tile the mouse is on

        if event.type == pygame.MOUSEBUTTONDOWN:
            (button1, button2, button3,) = pygame.mouse.get_pressed()  # get button pressed
        else:
            cursorColour = (0,0,0)
        CURSOR.center = (mousex,mousey)
        pygame.draw.rect(screen, cursorColour, CURSOR, 2)
        ##########################
    else:

        username.update(pygame.event.get())
        username.draw(screen)

        ##### MOUSE LOGIC #####
        mousex, mousey = pygame.mouse.get_pos()
        mousex = mousex - (mousex % TILESIZE) + TILESIZE / 2  # getting the x tile the mouse is on
        mousey = mousey - (mousey % TILESIZE) + TILESIZE / 2  # getting the y tile the mouse is on

    pygame.display.update()
