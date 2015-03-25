#-------------------------------------------------------------------------------
# Name:        BoT.Py
# Purpose:      ICS4U Programming FSE: Battle of Tyril
#
# Author:      Andrew Godfroy (Killer Rin)
#
# Created:     12/03/2011
# Copyright:   (c) killer rin 2011
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python
#------------------------ Import All Essentials Here ---------------------------
import pygame
from pygame.locals import *
from random import *
from socket import *
import math
import pickle
import os
import ctypes
#------------------------ Import all Extra Files Here --------------------------
import Actor
import Barrier
import GUI
#--------------------------- Initialize Pygame Here ----------------------------
"""
ID: js.get_id()
    0
Name: js.get_name()
    Controller (Xbox 360 Wireless Receiver for Windows)

Buttons: js.get_button(button)
    0 == A
    1 == B
    2 == X
    3 == Y
    4 == LB
    5 == RB
    6 == Back
    7 == Start
    8 == LS
    9 == RS

Axis: js.get_axis(axis_num)
    0: LS X Axis
Left: -1.0  Right: 1.0
    1: LS Y Axis
Up: -1.0    Down: 1.0
    2: LT, RT
LT: 1.0    RT: -1.0
    3: RS Y Axis
Up: -1.0    Down: 1.0
    4: RS X Axis
Left: -1.0  Right: 1.0

Hats: js.get_hat(hat_number)
    0: D-Pad
Left-(-1,0)     Upleft-(-1,1)
Right-(1,0)     Upright-(1,1)
Up-(0,1)        Downleft-(-1,-1)
Down-(0,-1)     Downright-(1,-1)
"""

user32 = ctypes.windll.user32
screen_res_width, screen_res_height = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
screen_width,screen_height = screen_res_width-80, screen_res_height-174
combscreen = screen_width+screen_height
winenvirX, winenvirY = 1 + ((screen_res_width - screen_width) // 2), 1 + ((screen_res_height - screen_height) // 2)
serverIPList = []
pygame.init()

try:
    achivementsfile = open (os.path.join('Program Files', 'Achivements.dll'), 'rb')
    ACHIVEMENTS = pickle.load(achivementsfile)
    achivementsfile.close()

except:
    ACHIVEMENTS = [[0, 'Achivement Name', 'Achivement Discription', 'Achivement Value', 'Unlocked?'],\
    ['You Actually Won!?!', 'Beat The Game', 100, False],\
    ['Star Shooter', 'Kill 50 Enemies', 50, False],\
    ['Two Birds, One Beam', ' Kill 2 Enemies with 1 Bullet', 25, False],\
    ['Martrydom', 'Die 25 Times', 5, False],\
    ['Nyanyanyanayn', 'Unlock Nyan Mode', 0, False],\
    ['Woofoofoofoof', 'Unlock DogNyan Mode', 0, False],\
    ['Trolololol', 'Unlock Troll Mode', 0, False],\
    ['','',0, False]]


    achivementsfile = open (os.path.join('Program Files', 'Achivements.dll'), 'wb')
    pickle.dump(ACHIVEMENTS, achivementsfile)
    achivementsfile.close()

try:
    highscorefile = open (os.path.join('Program Files', 'Highscore.dll'), 'rb')
    HIGHSCORE = pickle.load(highscorefile)
    highscorefile.close()
except:
    HIGHSCORE = [('Rank', 'Name', 'Time', 'Remaining Health'),\
    [1, ' ', 0, 0],\
    [2, ' ', 0, 0],\
    [3, ' ', 0, 0],\
    [4, ' ', 0, 0],\
    [5, ' ', 0, 0],\
    [6, ' ', 0, 0],\
    [7, ' ', 0, 0],\
    [8, ' ', 0, 0],\
    [9, ' ', 0, 0],\
    [10, ' ', 0, 0]]

    highscorefile = open (os.path.join('Program Files', 'Highscore.dll'), 'wb')
    pickle.dump(HIGHSCORE, highscorefile)
    highscorefile.close()

try:
    userfile = open (os.path.join('Program Files', 'Userfiles.dll'),'rb')
    USERFILES = pickle.load(userfile)
    userfile.close()

    screen_width, screen_height = USERFILES[0][0], USERFILES[0][1]
    combscreen = USERFILES[0][2]
    winenvirX, winenvirY = USERFILES[0][3], USERFILES[0][4]
    serverIPList = USERFILES [1]

except:
    USERFILES = [[screen_width,screen_height, combscreen, winenvirX, winenvirY], serverIPList]

    userfile = open (os.path.join('Program Files', 'Userfiles.dll'), 'wb')
    pickle.dump(USERFILES, userfile)
    userfile.close()

#os.environ['SDL_VIDEO_WINDOW_POS'] = '{0},{1}'.format(winenvirX, winenvirY)
os.environ['SDL_VIDEO_CENTERED'] = '1'
screen = pygame.display.set_mode([screen_width,screen_height])
pygame.display.set_caption('Battle of Tyril') # Set the title of the window
screen.fill((0,0,0))

#--------------------------- Insert Resources Here -----------------------------
 #== Fonts ==#
defaultfont = os.path.join('Resources', 'Fonts', 'freesansbold.ttf')
gamefont = os.path.join('Resources', 'Fonts', 'space_and_astronomy.ttf')

 #== Pictures ==#
                        #- Backgrounds -#
titleScreen = pygame.image.load(os.path.join('Resources', 'Backgrounds', 'Titlescreen.png')).convert()
optionScreen = pygame.image.load(os.path.join('Resources', 'Backgrounds', 'Options.png')).convert()
playerselectionScreen = pygame.image.load(os.path.join('Resources', 'Backgrounds', 'Player Selection.png')).convert()

                        #- Ships -#
ship01 = os.path.join('Resources', 'Actor', 'PlayerShip01.png')
ship02 = os.path.join('Resources', 'Actor', 'PlayerShip02.png')


ship01_loaded = pygame.image.load(ship01).convert()
ship02_loaded = pygame.image.load(ship02).convert()
                       #- Bullet Images -#
player_plasmabolt = pygame.image.load(os.path.join('Resources', 'Weapons', 'PlasmaBolt', 'plasmabolt.png')).convert()
enemy_plasmabolt = pygame.image.load(os.path.join('Resources', 'Weapons', 'PlasmaBolt', 'plasmabolt_enemy.png')).convert()


                        #- Other -#
 #== Music ==#
optionsMusic = os.path.join('Resources', 'Music', 'Options Music.mp3')
menuMusic = os.path.join('Resources', 'Music', 'Menu Music.mp3')
pauseMusic = os.path.join('Resources', 'Music', 'Pause Music.mp3')
gameMusic = os.path.join('Resources', 'Music', 'Mysterious Sleeper.mp3')
gameoverDeathMusic = os.path.join('Resources', 'Music', 'Gameover Death.mp3')
gameoverTimeUpMusic = os.path.join('Resources', 'Music', 'End Music.mp3')
#----------------------------- Interpret Resources -----------------------------
backup_TitleScreen = titleScreen
backup_OptionScreen = optionScreen
backup_PlayerSelectionScreen = playerselectionScreen

titleScreen = pygame.transform.scale(backup_TitleScreen,(screen_width, screen_height))
optionScreen = pygame.transform.scale(backup_OptionScreen,(screen_width, screen_height))
playerselectionScreen = pygame.transform.scale(backup_PlayerSelectionScreen,(screen_width, screen_height))

ship01_loaded = pygame.transform.scale(ship01_loaded, (int(screen_width/29.26829268292683),int(screen_height/13.492063492063492)))
ship02_loaded = pygame.transform.scale(ship02_loaded, (int(screen_width/29.26829268292683),int(screen_height/13.492063492063492)))

#------------------- Define Variables, Consts, Lists, Ect Here------------------
gameLoop = True #The Loop that controlls the Game Itself
startMenu = True #The Loop that Controlls the Start Menu
options = False # The Loop that Controlls the Options Menu
playerselection = False #The loop the controlls the Player Selection screen
game = False #Loop that Controlls the Game
gameover = False #Loop that Controlls the Gameover Screen

nyancatmode = False #Bonus Mode Controll
nyandogmode = False #Bonus Mode Controll
trololmode = False #Bonus Mode Controll
musiccheck = True
debugmode = False
pause = False
menudrawOverride = False
titleload,optionsload,playerselload,gameload,gameoverdeathload,gameoveraliveload = True,True,True,False,False,False
onejoystick, twojoystick, threejoystick, fourjoystick = False, False, False, False
p1joined, p2joined, p3joined, p4joined = False, False, False, False
p1ready, p2ready, p3ready, p4ready = False, False, False, False
gameoveraddi, gameoversubt = True, False


p1currentselect, p2currentselect, p3currentselect, p4currentselect = 1,1,1,1
curY, curY = 0,0
y_axis,x_axis = 0,0
FPS = (0)
gameoverctr, gameoverpausectr = 0, 0
currentSelection = 1
charspeed = (int(combscreen/102.5))
windowslidespeed = (int(combscreen/416.0))
aiIncrease = 0
aiDecIncrease = 0
aideaths = 0
playdeathctr = 0
loadstat = 0

gameoverreason = ''

pastseconds = 0
seconds, maxsec = 00, 30
minutes, maxmin = 00, 2
aiseconds = 6 # Used to track the Wave Clock. Also is Initial number of seconds till first wave.
wavetime = 4 # Used to reset 'aiseconds' back to the number specified once 'aiseconds' is less than or equal to 0
gameovereventtimer = 0

#-- Multiplayer Stuff -- #
serverIP = ''
PORT = 28637
BUFSIZ = 1024
multiselection = False
roomselection = False
multiplayermode = False
clienthostselect = True
client = False
clientt = False
host = False
multiwaittostart = False
hostready, clientready  = False, False
hostCurrentSelect, clientCurrentSelect = 1, 1
multiplayerselect = [[hostCurrentSelect,hostready],[clientCurrentSelect, clientready]]
connstat = None
1
#----- Custom Events -----#
TIMECOUNTER = USEREVENT
#--------- Colours ---------#
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
button = pygame.mouse.get_pressed()
clock = pygame.time.Clock()


players = pygame.sprite.RenderPlain()
AIlist = pygame.sprite.RenderPlain()
bulletlist_Player = pygame.sprite.RenderPlain()
bulletlist_AI = pygame.sprite.RenderPlain()

impassable_barrier = pygame.sprite.RenderPlain()
titleMenu = pygame.sprite.RenderPlain()
cliho = pygame.sprite.RenderUpdates()
HUDL = pygame.sprite.RenderPlain()
optionsMenu = pygame.sprite.RenderPlain()
bonusplayselect = pygame.sprite.RenderPlain()


#------- Lists -------#
keycodelist = []
UNLOCKABLES = [['Up', 'Up', 'Down', 'Down', 'Left', 'Right', 'Left', 'Right', 'B', 'Enter'],\
['B', 'Right', 'Left', 'Right', 'Left', 'Down', 'Down', 'Up', 'Up', 'Enter'],\
['Down', 'Down', 'Down', 'Up', 'Up', 'Up', 'Left', 'Left', 'Right', 'Enter']]
SHIPS = ['', ship01, ship02]
LOADEDSHIPS = ['', ship01_loaded, ship02_loaded]
PLAYERWEAPONS = [('Weapon Name', 'Weapon Speed', 'Weapon Damage', 'Weapon Counter', 'Weapon Image', 'Weapon Sound'),\
 ('Plasma Bolt',  30, 1, 5, player_plasmabolt, 'Resources/Weapons/PlasmaBolt/')]
AIWEAPONS = [('Weapon Name', 'Weapon Speed', 'Weapon Damage', 'Weapon Counter', 'Weapon Image', 'Weapon Sound'),\
 ('Plasma Bolt',  30, 2, 15, enemy_plasmabolt, 'Resources/Weapons/PlasmaBolt/')]
#------------------------------- Define Functions ------------------------------
def drawtxt(txt,font,fs,clr,x,y,w,h,tf):
    """Text, Font Size, Colour, x, y, w, h, Black Background (True/False)"""
    if tf == True:
        pygame.draw.rect(screen, BLACK, (x,y,w,h))
    if pygame.font:
            font = pygame.font.Font(font,fs)
    text = font.render(txt, False, clr)
    screen.blit(text, (x,y))
    pygame.display.update(x,y,w,h)

def gameUpdate(p1, p2, p3, p4, bulletlist_Player, bulletlist_AI, aideaths, multiplayer = False):
    if multiplayer == False:
        for i in bulletlist_Player:
            i.update(players, AIlist)
        for i in bulletlist_AI:
            i.update(players, AIlist)
        for i in players:
            bulletlist_Player, bulletlist_AI = i.shoot(players,AIlist,[bulletlist_Player, bulletlist_AI])
            i.update(players, AIlist, [bulletlist_Player, bulletlist_AI], aideaths)
        for i in AIlist:
            bulletlist_Player, bulletlist_AI = i.shoot(players,AIlist,[bulletlist_Player, bulletlist_AI])
            aideaths = i.update(players, AIlist, [bulletlist_Player, bulletlist_AI], aideaths)
        players.draw(screen)
        AIlist.draw(screen)
        bulletlist_Player.draw(screen)
        bulletlist_AI.draw(screen)

            #Draw the HUD over everything else
        HUDL.draw(screen)
        pygame.draw.line(screen, WHITE, (screen_width/1.2244897959183674, screen_height/5.985915492957746),(screen_width/1.2244897959183674,0))

        # -- Time to Update and Draw the HUD --- #
        if p1 == True:
            drawtxt('Player 1', defaultfont, int(combscreen/102.5), WHITE, screen_width/12.0, screen_height/85.0,80,25, False)
            drawtxt(str(player1.get_health()), defaultfont, int(combscreen/102.5), RED, screen_width/10.0, screen_height/21.25,80,25, False)
        if p2 == True:
            drawtxt('Player 2', defaultfont, int(combscreen/102.5), WHITE, screen_width/3.4285714285714284, screen_height/85.0,80,25, False)
            drawtxt(str(player2.get_health()), defaultfont, int(combscreen/102.5), RED, screen_width/3.2432432432432434, screen_height/21.25,80,25, False)
        if p3 == True:
            drawtxt('Player 3', defaultfont, int(combscreen/102.5), WHITE, screen_width/2.0, screen_height/85.0,80,25, False)
            drawtxt(str(player3.get_health()), defaultfont, int(combscreen/102.5), RED, screen_width/1.935483870967742, screen_height/21.25,80,25, False)
        if p4 == True:
            drawtxt('Player 4', defaultfont, int(combscreen/102.5), WHITE, screen_width/1.411764705882353, screen_height/85.0,80,25, False)
            drawtxt(str(player4.get_health()), defaultfont, int(combscreen/102.5), RED, screen_width/1.3793103448275863, screen_height/21.25,80,25, False)

        #--- Draw the Timers ---#
            # Draw the Next Wave Clock
        drawtxt("Next Wave", defaultfont,  int(combscreen/102.5), WHITE, screen_width/1.170731707317073, screen_height/85, 80, 25, False)
        drawtxt(str(aiseconds), defaultfont, int(combscreen/102.5), RED, screen_width/1.1267605633802817, screen_height/21.25,80,25, False)
            # Draw the Game Clock
        drawtxt((str(minutes) + " : " + str(seconds)), defaultfont,  int(combscreen/102.5), WHITE, screen_width/1.1450381679389312, screen_height/8.673469387755102, 80, 25, False)
        return bulletlist_Player, bulletlist_AI, aideaths

    elif multiplayer == True:
        if client == True:
            bulletlist_Player, bulletlist_AI = client_actor.shoot(players,AIlist,[bulletlist_Player, bulletlist_AI])
            client_actor.update(players, AIlist, [bulletlist_Player, bulletlist_AI], aideaths)

            players.draw(screen)
            AIlist.draw(screen)
            bulletlist_Player.draw(screen)
            bulletlist_AI.draw(screen)

                #Draw the HUD over everything else
            HUDL.draw(screen)
            pygame.draw.line(screen, WHITE, (screen_width/1.2244897959183674, screen_height/5.985915492957746),(screen_width/1.2244897959183674,0))

                # -- Time to Update and Draw the HUD --- #
            drawtxt('Client', defaultfont, int(combscreen/102.5), WHITE, screen_width/12.0, screen_height/85.0,80,25, False)
            drawtxt(str(client_actor.get_health()), defaultfont, int(combscreen/102.5), RED, screen_width/10.0, screen_height/21.25,80,25, False)

            drawtxt('Host', defaultfont, int(combscreen/102.5), WHITE, screen_width/3.4285714285714284, screen_height/85.0,80,25, False)
            drawtxt(str(host_actor.get_health()), defaultfont, int(combscreen/102.5), RED, screen_width/3.2432432432432434, screen_height/21.25,80,25, False)

            #--- Draw the Timers ---#
                # Draw the Next Wave Clock
            drawtxt("Next Wave", defaultfont,  int(combscreen/102.5), WHITE, screen_width/1.170731707317073, screen_height/85, 80, 25, False)
            drawtxt(str(aiseconds), defaultfont, int(combscreen/102.5), RED, screen_width/1.1267605633802817, screen_height/21.25,80,25, False)
                # Draw the Game Clock
            drawtxt((str(minutes) + " : " + str(seconds)), defaultfont,  int(combscreen/102.5), WHITE, screen_width/1.1450381679389312, screen_height/8.673469387755102, 80, 25, False)
            return bulletlist_Player, bulletlist_AI
        elif host == True:
            bulletlist_Player, bulletlist_AI = host_actor.shoot(players,AIlist,[bulletlist_Player, bulletlist_AI])
            host_actor.update(players, AIlist, [bulletlist_Player, bulletlist_AI], aideaths)


            players.draw(screen)
            AIlist.draw(screen)
            bulletlist_Player.draw(screen)
            bulletlist_AI.draw(screen)

                #Draw the HUD over everything else
            HUDL.draw(screen)
            pygame.draw.line(screen, WHITE, (screen_width/1.2244897959183674, screen_height/5.985915492957746),(screen_width/1.2244897959183674,0))

                # -- Time to Update and Draw the HUD --- #
            drawtxt('Host', defaultfont, int(combscreen/102.5), WHITE, screen_width/12.0, screen_height/85.0,80,25, False)
            drawtxt(str(client_actor.get_health()), defaultfont, int(combscreen/102.5), RED, screen_width/10.0, screen_height/21.25,80,25, False)

            drawtxt('Client', defaultfont, int(combscreen/102.5), WHITE, screen_width/3.4285714285714284, screen_height/85.0,80,25, False)
            drawtxt(str(host_actor.get_health()), defaultfont, int(combscreen/102.5), RED, screen_width/3.2432432432432434, screen_height/21.25,80,25, False)

            #--- Draw the Timers ---#
                # Draw the Next Wave Clock
            drawtxt("Next Wave", defaultfont,  int(combscreen/102.5), WHITE, screen_width/1.170731707317073, screen_height/85, 80, 25, False)
            drawtxt(str(aiseconds), defaultfont, int(combscreen/102.5), RED, screen_width/1.1267605633802817, screen_height/21.25,80,25, False)
                # Draw the Game Clock
            drawtxt((str(minutes) + " : " + str(seconds)), defaultfont,  int(combscreen/102.5), WHITE, screen_width/1.1450381679389312, screen_height/8.673469387755102, 80, 25, False)
            return bulletlist_Player, bulletlist_AI

def sendPackets(clientorhost):
    if clientorhost is 'Client':
        clienttransdata = [client_actor.get_location(), client_actor.get_rotation()]

        try:
            clientdata = pickle.dumps(clienttransdata,True)
            tcpCliSock.send(clientdata)
            hostdata = tcpCliSock.recv(1024*4)
            hosttransdata = pickle.loads(hostdata)
##            print (hosttransdata)
            host_actor.multi_set_image(hosttransdata)
        except: pass
        return host_actor
    elif clientorhost is 'Host':
        hosttransdata = [host_actor.get_location(), host_actor.get_rotation()]
        try:
            hostdata = pickle.dumps(hosttransdata,True)
            clientsock.send(hostdata)
            clientdata = clientsock.recv(1024*4)
            clienttransdata = pickle.loads(clientdata)
##            print (clienttransdata)
            client_actor.multi_set_image(clienttransdata)
        except: pass
        return client_actor

def resolutionChange(newwidth, newheight, full):
    global screen, screen_width, screen_height, combscreen, winenvirX, winenvirY,\
     backup_TitleScreen, backup_OptionScreen, backup_PlayerSelectionScreen,  backup_GameScreen, backup_GameOverDeathScreen, backup_GameOverTimeUpScreen,\
      titleScreen, optionScreen, playerselectionScreen, gameScreen, gameoverDeathScreen, gameoverTimeUpScreen,\
       barrierLeft, barrierTop, barrierRight, barrierBottom, gameload, gameoverdeathload, gameoveraliveload,\
        HUD, players, AIlist, ship01_loaded, ship02_loaded, LOADEDSHIPS, USERFILES

    screen.fill(BLACK)
    pygame.display.update()
    loadstat = 0
    drawtxt('Loading...'+ str(loadstat)+'%', gamefont, int(combscreen/51.25), WHITE, screen_width/2,screen_height/2, screen_width/1.204705882352941, screen_height/1.7066666666666668, True)

    screen_width,screen_height = newwidth, newheight
    combscreen = screen_width+screen_height

    if newwidth == 800 and newheight == 600:
        winenvirX, winenvirY = 1 + ((screen_res_width - screen_width) // 2), 1 + ((screen_res_height - screen_height) // 2)
    elif newwidth == 1024 and newheight == 768:
        winenvirX, winenvirY = 1 + ((screen_res_width - screen_width) // 2), 1 + ((screen_res_height - screen_height) // 2)
    elif newwidth == 1280 and newheight == 1024:
        winenvirX, winenvirY = 0, 25

    charspeed = int(combscreen/102.5)

            #--- Check to see if anything isn't loaded before we preceed. If it isn't, we load it
    if gameload == False:
        gameScreen = pygame.image.load(os.path.join('Resources', 'Backgrounds', 'Game.png')).convert()
        backup_GameScreen = gameScreen
        gameScreen = pygame.transform.scale(backup_GameScreen,(screen_width, screen_height))
        gameload = True
    loadstat = 10
    drawtxt('Loading...'+ str(loadstat)+'%', gamefont, int(combscreen/51.25), WHITE, screen_width/2,screen_height/2, screen_width/1.204705882352941, screen_height/1.7066666666666668, True)


    if gameoverdeathload == False:
        gameoverDeathScreen = pygame.image.load(os.path.join('Resources', 'Backgrounds', 'Gameover_Death.png')).convert()
        backup_GameOverDeathScreen = gameoverDeathScreen
        gameoverDeathScreen = pygame.transform.scale(backup_GameOverDeathScreen,(screen_width, screen_height))
        gameoverdeathload = True
    loadstat = 20
    drawtxt('Loading...'+ str(loadstat)+'%', gamefont, int(combscreen/51.25), WHITE, screen_width/2,screen_height/2, screen_width/1.204705882352941, screen_height/1.7066666666666668, True)

    if gameoveraliveload == False:
        gameoverTimeUpScreen = pygame.image.load(os.path.join('Resources', 'Backgrounds', 'Gameover_Time Up.png')).convert()
        backup_GameOverTimeUpScreen = gameoverTimeUpScreen
        gameoverTimeUpScreen = pygame.transform.scale(backup_GameOverTimeUpScreen,(screen_width, screen_height))
        gameoveraliveload = True
    loadstat = 30
    drawtxt('Loading...'+ str(loadstat)+'%', gamefont, int(combscreen/51.25), WHITE, screen_width/2,screen_height/2, screen_width/1.204705882352941, screen_height/1.7066666666666668, True)


    titleScreen = pygame.transform.scale(backup_TitleScreen,(screen_width, screen_height))
    optionScreen = pygame.transform.scale(backup_OptionScreen,(screen_width, screen_height))
    gameScreen = pygame.transform.scale(backup_GameScreen,(screen_width, screen_height))
    playerselectionScreen = pygame.transform.scale(backup_PlayerSelectionScreen,(screen_width, screen_height))
    gameoverDeathScreen = pygame.transform.scale(backup_GameOverDeathScreen,(screen_width, screen_height))
    gameoverTimeUpScreen = pygame.transform.scale(backup_GameOverDeathScreen,(screen_width, screen_height))
    loadstat = 40
    drawtxt('Loading...'+ str(loadstat)+'%', gamefont, int(combscreen/51.25), WHITE, screen_width/2,screen_height/2, screen_width/1.204705882352941, screen_height/1.7066666666666668, True)

    ship01_loaded = pygame.transform.scale(ship01_loaded, (int(screen_width/29.26829268292683),int(screen_height/13.492063492063492)))
    ship02_loaded = pygame.transform.scale(ship02_loaded, (int(screen_width/29.26829268292683),int(screen_height/13.492063492063492)))
    LOADEDSHIPS = ['', ship01_loaded, ship02_loaded]
    loadstat = 50
    drawtxt('Loading...'+ str(loadstat)+'%', gamefont, int(combscreen/51.25), WHITE, screen_width/2,screen_height/2, screen_width/1.204705882352941, screen_height/1.7066666666666668, True)


    # Barriers
    barrierLeft.set_pos(screen_width/-300,0,1.0,screen_height/1.0) # Left
    barrierTop.set_pos(0,screen_height/6.071428571428571,screen_width/1.0,1.0) # Top
    barrierRight.set_pos(screen_width/0.9991673605328892,0,1.0,screen_height/1.0) # Right
    barrierBottom.set_pos(0,screen_height/1.0,screen_width/1.0,1.0) #Bottom
    loadstat = 60
    drawtxt('Loading...'+ str(loadstat)+'%', gamefont, int(combscreen/51.25), WHITE, screen_width/2,screen_height/2, screen_width/1.204705882352941, screen_height/1.7066666666666668, True)


    HUD.setimg(0,0,screen_width, screen_height/5.94, os.path.join('Resources', 'GUI', 'HUD.png'))
    bmodes.setimg(screen_width/8.0, screen_height/3.6363636363636362, screen_width/4.040404040404041, screen_height/17.0, os.path.join('Resources', 'GUI', 'Bonus Modes.png'))
    loadstat = 70
    drawtxt('Loading...'+ str(loadstat)+'%', gamefont, int(combscreen/51.25), WHITE, screen_width/2,screen_height/2, screen_width/1.204705882352941, screen_height/1.7066666666666668, True)


    for i in players:
        i.set_scaling(newwidth, newheight)
    loadstat = 80
    drawtxt('Loading...'+ str(loadstat)+'%', gamefont, int(combscreen/51.25), WHITE, screen_width/2,screen_height/2, screen_width/1.204705882352941, screen_height/1.7066666666666668, True)

    for i in AIlist:
        i.set_scaling(newwidth, newheight)
    loadstat = 90
    drawtxt('Loading...'+ str(loadstat)+'%', gamefont, int(combscreen/51.25), WHITE, screen_width/2,screen_height/2, screen_width/1.204705882352941, screen_height/1.7066666666666668, True)

    os.environ['SDL_VIDEO_WINDOW_POS'] = '{0},{1}'.format(winenvirX, winenvirY)
    if full == True:
        screen = pygame.display.set_mode([newwidth, newheight], pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode([newwidth, newheight])

    try:
        if full != True:
            USERFILES = [[screen_width,screen_height, combscreen, winenvirX, winenvirY]]

            userfile = open (os.path.join('Program Files', 'Userfiles.dll'), 'wb')
            pickle.dump(USERFILES, userfile)
            userfile.close()
    except: pass
    loadstat = 100
    drawtxt('Loading...'+ str(loadstat)+'%', gamefont, int(combscreen/51.25), WHITE, screen_width/2,screen_height/2, screen_width/1.204705882352941, screen_height/1.7066666666666668, True)



def resetGame():
    global gameLoop,startMenu, options, game, gameover, musiccheck, pause, menudrawOverride,\
     onejoystick, twojoystick, threejoystick, fourjoystick, p1ready, p2ready, p3ready, p4ready,\
      gameoveraddi, gameoversubt, p1currentselect, p2currentselect, p3currentselect, p4currentselect,\
       y_axis, x_axis, gameoverctr, gameoverpausectr, currentSelection, charspeed, aiIncrease, aiDecIncrease,\
        seconds, minutes, aiseconds, wavetime, gameovereventtimer, gameoverreason, players, AIlist, trololmode,\
         bulletlist_Player, bulletlist_AI, aideaths, keycodelist, nyancatmode, nyandogmode, loadstat,\
          serverIP, roomselection, multiplayermode, clienthostselect, client, host, connstat,\
           clientt, multiselection, hostCurrentSelect, clientCurrentSelect, multiplayerselect, clientready, hostready,\
            multiwaittostart

    """ Reset Game is only called within the Gameover Screen. What we do is we take
    all the variables and reset them back to their default position. By doing this
    we allow the players to continue to play the game without having to reset """

    gameLoop = True #The Loop that controlls the Game Itself
    startMenu = True #The Loop that Controlls the Start Menu
    options = False #The Loop that Controlls the Options Menu
    playerselection = False #The Loop that Controlls the Player Selection Menu
    game = False #The Loop that Controlls the Game
    gameover = False #The Loop that Controlls the Gameover Screen
    nyancatmode = False #Bonus Mode Controll
    nyandogmode = False #Bonus Mode Controll
    trololmode = False
    musiccheck = True
    pause = False
    menudrawOverride = False
    onejoystick,twojoystick,threejoystick,fourjoystick = False, False, False, False
    p1ready, p2ready, p3ready, p4ready = False, False, False, False
    gameoveraddi,gameoversubt = True, False


    p1currentselect, p2currentselect, p3currentselect, p4currentselect = 1,1,1,1
    x_axis,y_axis = 0,0
    gameoverctr, gameoverpausectr = 0, 0
    currentSelection = 1
    charspeed = int(combscreen/102.5)
    aiIncrease = 0
    aiDecIncrease = 0
    aideaths = 0
    loadstat = 0

    seconds, minutes = 00, 00
    aiseconds, wavetime = 6, 4
    gameovereventtimer = 0

    gameoverreason = ''
    keycodelist = []

    #-- Multiplayer Stuff -- #
    serverIP = ''
    roomselection = False
    multiplayermode = False
    clienthostselect = True
    multiselection = False
    client = False
    clientt = False
    multiwaittostart = False
    host = False
    clientready, hostready = False, False
    hostCurrentSelect, clientCurrentSelect = 1, 1
    serverIPList = []
    multiplayerselect = [hostCurrentSelect,clientCurrentSelect]
    connstat = None

        #-- Kill everyone in all the lists --#
    for i in players:
        i.kill()
    for i in AIlist:
        i.kill()
    for i in bulletlist_Player:
        i.kill()
    for i in bulletlist_AI:
        i.kill()

     #-- Reset the Sprite List variables as Sprite Lists to start from a clean slate --#
    players = pygame.sprite.RenderPlain()
    AIlist = pygame.sprite.RenderPlain()
    bulletlist_Player = pygame.sprite.RenderPlain()
    bulletlist_AI = pygame.sprite.RenderPlain()

def unlockAchivement(achivementlist, achivement):
    for i in achivementlist:
        if i[0] == achivement:
            if i[3] != True:
                achivementlist[0][0] += i[2]
                i[3] = True

                if debugmode == True: print ('Achivement Unlocked')
                break
            else: break

    achivementsfile = open (os.path.join('Program Files', 'Achivements.dll'), 'wb')
    pickle.dump(ACHIVEMENTS, achivementsfile)
    achivementsfile.close()
    return achivementlist

def unlockAwards(unlock):
    pygame.mixer.music.stop()
    if unlock == 'NyanCatMode':
        nyctr = 0
        while 1:
            pygame.draw.rect(screen, (0,0,0), (randint(0,screen_width), randint(0,screen_height), 15, 15))
            pygame.draw.rect(screen, (255,255,255), (randint(0,screen_width), randint(0,screen_height), 15, 15))
            pygame.draw.rect(screen, (150,150,150), (randint(0,screen_width), randint(0,screen_height), 15, 15))
            pygame.display.update()
            nyctr +=1
            if nyctr >= combscreen:
                nyctr = 0
                break
        pygame.mixer.music.load(os.path.join('Resources', 'Bonus Modes', 'Nyan', 'Nyan.mp3'))
        pygame.mixer.music.play(-1)
        screen.fill(BLACK)
        pygame.display.update()
        player1.set_image(screen_width/2, screen_height/2, os.path.join ('Resources', 'Bonus Modes', 'Nyan', 'Nyan Cat.png'))
        pygame.time.wait(500)
    elif unlock == 'NyanDogMode':
        nyctr = 0
        while 1:
            pygame.draw.rect(screen, (255,255,255), (randint(0,screen_width), randint(0,screen_height), 15, 15))
            pygame.draw.rect(screen, (155,155,155), (randint(0,screen_width), randint(0,screen_height), 15, 15))
            pygame.draw.rect(screen, (55,55,55), (randint(0,screen_width), randint(0,screen_height), 15, 15))
            pygame.draw.rect(screen, (0,0,0), (randint(0,screen_width), randint(0,screen_height), 15, 15))
            pygame.display.update()
            nyctr +=1
            if nyctr >= combscreen:
                nyctr = 0
                break
        pygame.mixer.music.load(os.path.join('Resources', 'Bonus Modes', 'Nyan', 'Woof.mp3'))
        pygame.mixer.music.play(-1)
        screen.fill(BLACK)
        pygame.display.update()
        player1.set_image(screen_width/2, screen_height/2, os.path.join ('Resources', 'Bonus Modes', 'Nyan', 'Nyan Dog.png'))
        pygame.time.wait(500)
    elif unlock == 'Troll Mode':
        nyctr = 0
        while 1:
            pygame.draw.rect(screen, (255,255,255), (randint(0,screen_width), randint(0,screen_height), 15, 15))
            pygame.draw.rect(screen, (155,155,155), (randint(0,screen_width), randint(0,screen_height), 15, 15))
            pygame.draw.rect(screen, (55,55,55), (randint(0,screen_width), randint(0,screen_height), 15, 15))
            pygame.draw.rect(screen, (0,0,0), (randint(0,screen_width), randint(0,screen_height), 15, 15))
            pygame.display.update()
            nyctr +=1
            if nyctr >= combscreen:
                nyctr = 0
                break
        pygame.mixer.music.load(os.path.join('Resources', 'Bonus Modes', 'Troll', 'Troll.mp3'))
        pygame.mixer.music.play(-1)
        screen.fill(BLACK)
        pygame.display.update()
        player1.set_image(screen_width/2, screen_height/2, os.path.join ('Resources', 'Bonus Modes', 'Troll', 'Troll.png'))
        pygame.time.wait(500)
    return True

def slidingwindow(tf1, tf2, images, slidespeed, slidepos, tblr):
    tf1, tf2 = True, False
    slidectr = 0
    backgroundimg = images[0]
    slidingimg = images[1]
    while 1:
        slidectr += slidespeed
        if slidepos == 'Horizontal':
            if tblr == 'Left':
                screen.blit(backgroundimg, (0,0))
                screen.blit(slidingimg, (0+slidectr, 0))
                pygame.display.update()
            elif tblr == 'Right':
                screen.blit(backgroundimg, (0,0))
                screen.blit(slidingimg, (screen_width-slidectr, 0))
                pygame.display.update()
            if slidectr >= screen_width:
                break
        elif slidepos == 'Vertical':
            if tblr == 'Top':
                screen.blit(backgroundimg, (0,0))
                screen.blit(slidingimg,(0,0+slidectr))
                pygame.display.update()
            elif tblr == 'Bottom':
                screen.blit(backgroundimg, (0,0))
                screen.blit(slidingimg,(0,screen_height-slidectr))
                pygame.display.update()
            if slidectr >= screen_height:
                break
    return tf1, tf2

def spawnAI(increase, decincrease):
    check1,check2,check3 = randint(0,7),randint(0,8),randint(0,9)
    if onejoystick == True:
        base = 6
    elif twojoystick == True:
        base = 7
    elif threejoystick == True:
        base = 8
    elif fourjoystick == True:
        base = 9
    else: base = 6

    if trololmode == True:
        increase +=5

    if increase <= 45:
        if check1 == 2:
            if check2 == 2:
                if check3 == 2: increase += 3
                else: increase += 2
            else: increase += 1
        else: decincrease += .08

        if decincrease >= 1:
            increase += 1
            decincrease -= 1

    numEnemies = base+increase
    if debugmode ==True: print(increase, '|', decincrease)

    if nyancatmode == True:
        enimg = os.path.join('Resources', 'Bonus Modes', 'Nyan', 'Nyan Dog.png')
    elif nyandogmode == True:
        enimg = os.path.join('Resources', 'Bonus Modes', 'Nyan', 'Nyan Cat.png')
    else:
        enimg = os.path.join('Resources', 'Actor', 'AI.png')

    for i in range (int(numEnemies/4)): #leftside
        AI = Actor.Actor ((randint(0, int(screen_width/6.0))),\
         (randint(int(screen_height/5.821917808219178), int(screen_height/1.0493827160493827))),\
          screen_width, screen_height, enimg, AIWEAPONS, 100, 'AI'  )
        AI.set_walls(impassable_barrier)
        AIlist.add(AI)
    for i in range (int(numEnemies/4)): #Rightside
        AI = Actor.Actor ((randint(int(screen_width/1.2903225806451613), int(screen_width))),\
         (randint(int(screen_height/5.821917808219178), int(screen_height/1.0493827160493827))),\
          screen_width, screen_height, enimg, AIWEAPONS, 100, 'AI'  )
        AI.set_walls(impassable_barrier)
        AIlist.add(AI)
    for i in range (int(numEnemies/4)): #Top
        AI = Actor.Actor ((randint(0, int(screen_width))),\
         (randint(int(screen_height/5.821917808219178), int(screen_height/2.8333333333333335))),\
          screen_width, screen_height, enimg, AIWEAPONS, 100, 'AI'  )
        AI.set_walls(impassable_barrier)
        AIlist.add(AI)
    for i in range (int(numEnemies/4)): #Bottom
        AI = Actor.Actor ((randint(0, int(screen_width))),\
         (randint(int(screen_height/1.36), int(screen_height))),\
          screen_width, screen_height, enimg, AIWEAPONS, 100, 'AI'  )
        AI.set_walls(impassable_barrier)
        AIlist.add(AI)

    return increase, decincrease

def time(seconds,minutes):
    seconds += 1
    if seconds == 60:
        seconds = 0
        minutes += 1
    return seconds, minutes

#-------------------------- Define Sprites/Spritelists -------------------------
startGame = GUI.GUI(screen_width/8.0, screen_height/2.4285714285714284, screen_width/4.040404040404041, screen_height/17.0, os.path.join('Resources', 'GUI', 'Play Game.png'))
multiplayerButton = GUI.GUI(screen_width/8.0, screen_height/1.8888888888888888, screen_width/4.040404040404041, screen_height/17.0, os.path.join('Resources', 'GUI', 'Multiplayer.png'))
optionButton = GUI.GUI(screen_width/8.0, screen_height/1.5454545454545454, screen_width/4.040404040404041, screen_height/17.0, os.path.join('Resources', 'GUI', 'Options.png'))
exitGame = GUI.GUI(screen_width/8.0, screen_height/1.307692307692308, screen_width/4.040404040404041, screen_height/17.0, os.path.join('Resources', 'GUI', 'Exit Game.png'))
titleMenu.add(startGame, multiplayerButton, optionButton, exitGame)

op800x600 = GUI.GUI(screen_width/60.0, screen_height/1.1888111888111887, screen_width/4.040404040404041, screen_height/17.0, os.path.join('Resources', 'GUI', '800x600.png'))
op1024x768 =  GUI.GUI(screen_width/3.75, screen_height/1.1888111888111887, screen_width/4.040404040404041, screen_height/17.0, os.path.join('Resources', 'GUI', '1024x768.png'))
op1280x1024 =  GUI.GUI(screen_width/2.1052631578947367, screen_height/1.1888111888111887, screen_width/4.040404040404041, screen_height/17.0, os.path.join('Resources', 'GUI', '1280x1024.png'))
fullscreen = GUI.GUI(screen_width/1.3793103448275863, screen_height/1.1888111888111887, screen_width/4.040404040404041, screen_height/17.0, os.path.join('Resources', 'GUI', 'Fullscreen.png'))
optionsMenu.add(fullscreen, op800x600, op1024x768, op1280x1024)

clientimg = GUI.GUI (screen_width/8.0, screen_height/4.0, screen_width/4.040404040404041, screen_height/17.0, os.path.join('Resources', 'GUI', 'Client.png'))
hostimg = GUI.GUI (screen_width/2.1052631578947367, screen_height/4.0, screen_width/4.040404040404041, screen_height/17.0, os.path.join('Resources', 'GUI', 'Host.png'))
cliho.add(clientimg, hostimg)

HUD = GUI.GUI(0,0,screen_width, screen_height/5.94, os.path.join('Resources', 'GUI', 'HUD.png'))
HUDL.add(HUD)

bmodes = GUI.GUI(screen_width/8.0, screen_height/3.6363636363636362, screen_width/4.040404040404041, screen_height/17.0, os.path.join('Resources', 'GUI', 'Bonus Modes.png'))
cat = GUI.GUI(screen_width/2.0, screen_height/1.1888111888111887, screen_width/29.26829268292683,screen_height/13.492063492063492, os.path.join('Resources', 'Bonus Modes', 'Nyan', 'Nyan Cat.png'))
dog =GUI.GUI(screen_width/1.6, screen_height/1.1888111888111887, int(screen_width/29.26829268292683),int(screen_height/13.492063492063492), os.path.join('Resources', 'Bonus Modes', 'Nyan', 'Nyan Dog.png'))
troll = GUI.GUI(screen_width/1.3763440860215055, screen_height/1.1888111888111887, int(screen_width/29.26829268292683),int(screen_height/13.492063492063492), os.path.join('Resources', 'Bonus Modes', 'Troll', 'Troll.png'))
bonusplayselect.add(bmodes)

# Barriers
barrierLeft=Barrier.Barrier(screen_width/-300,0,1.0,screen_height/1.0) # Left
barrierTop=Barrier.Barrier(0,screen_height/6.071428571428571,screen_width/1.0,1.0) # Top
barrierRight=Barrier.Barrier(screen_width/0.9991673605328892,0,1.0,screen_height/1.0) # Right
barrierBottom=Barrier.Barrier(0,screen_height/1.0,screen_width/1.0,1.0) #Bottom
impassable_barrier.add(barrierLeft,barrierTop,barrierRight,barrierBottom)

for i in AIlist:
    i.set_walls(impassable_barrier)

#------------------------------ Set The Timers ---------------------------------

#------------------------------- Main Program ----------------------------------

while gameLoop == True:

    def STARTMENU_LOOP():
        """ This is used to quickly jump to the Start Menu Loop from the Code Explorer """
        pass

    menumax = 4
    while startMenu == True:
        pygame.display.set_caption('Battle of Tyril     |     FPS: ' + str(clock.get_fps())) # Set the title of the window

        if musiccheck == True:
            pygame.mixer.music.load(menuMusic)
            pygame.mixer.music.play(-1)
            musiccheck = False

        # Check Joystick Inputs and Init as required
        joystick_count = pygame.joystick.get_count()
        if joystick_count == 1 or joystick_count == 2 or joystick_count == 3  or joystick_count == 4:
            if onejoystick == True:
                pass
            else:
                # Use joystick #0 and initialize it
                joy1 = pygame.joystick.Joystick(0)
                joy1.init()
                onejoystick = True


            #------------- Start Code ---------------#
        screen.blit (titleScreen, (0,0))
        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # Exit Game
                gameLoop = False # Flag that we are done so we exit this loop
                startMenu = False # Flag that we want to cancel out of the Start Menu
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: # Exit Game
                    gameLoop=False
                    startMenu = False
                if event.key == pygame.K_UP:
                    if currentSelection > 1:
                        currentSelection-=1
                    else: currentSelection = menumax
                if event.key == pygame.K_DOWN:
                    if currentSelection < menumax:
                        currentSelection+=1
                    else: currentSelection = 1
                if event.key == pygame.K_SPACE:
                    if currentSelection == 1: #Start Game
                        playerselection,startMenu = slidingwindow(playerselection, startMenu, [titleScreen,playerselectionScreen], windowslidespeed, 'Horizontal', 'Right')
                        musiccheck = True
                        screen.fill(BLACK)
                        currentSelection = 1
                        menudrawOverride = True
                    if currentSelection == 2:
                        roomselection, startMenu  = slidingwindow(roomselection, startMenu, [titleScreen,playerselectionScreen], windowslidespeed, 'Horizontal', 'Right')
                        musiccheck = True
                        screen.fill(BLACK)
                        currentSelection = 1
                        clienthostselect = True
                        menudrawOverride = True
                    if currentSelection == 3: #Options
                        options,startMenu = slidingwindow(options,startMenu, [titleScreen,optionScreen], windowslidespeed, 'Vertical', 'Bottom')
                        musiccheck = True
                        screen.fill(BLACK)
                        currentSelection = 1
                        menudrawOverride = True
                    if currentSelection == 4: #Exit Game
                        gameLoop=False
                        startMenu=False
            if onejoystick == True:
                if event.type == pygame.JOYBUTTONDOWN:
                    if joy1.get_button(0): # If User Pressed the A Button
                        if currentSelection == 1: #Start Game
                            playerselection,startMenu = slidingwindow(playerselection, startMenu, [titleScreen,playerselectionScreen], windowslidespeed, 'Horizontal', 'Right')
                            musiccheck = True
                            screen.fill(BLACK)
                            currentSelection = 1
                            menudrawOverride = True
                        if currentSelection == 2:
                            roomselection, startMenu  = slidingwindow(roomselection, startMenu, [titleScreen,playerselectionScreen], windowslidespeed, 'Horizontal', 'Right')
                            musiccheck = True
                            screen.fill(BLACK)
                            currentSelection = 1
                            clienthostselect = True
                            menudrawOverride = True
                        if currentSelection == 3: #Options
                            options,startMenu = slidingwindow(options,startMenu, [titleScreen,optionScreen], windowslidespeed, 'Vertical', 'Bottom')
                            musiccheck = True
                            screen.fill(BLACK)
                            currentSelection = 1
                            menudrawOverride = True
                        if currentSelection == 4: #Exit Game
                            gameLoop=False
                            startMenu=False
                    if joy1.get_button(6): # Exit Game
                        gameLoop=False
                        startMenu = False
                if event.type == pygame.JOYHATMOTION:
                    if joy1.get_hat(0) == (0,1): #Going Up
                        if currentSelection > 1:
                            currentSelection-=1
                        else:
                            currentSelection = menumax
                    if joy1.get_hat(0) == (0,-1): #Going Down
                        if currentSelection < menumax:
                            currentSelection+=1
                        else:
                            currentSelection = 1
                if event.type == pygame.JOYAXISMOTION:
                    if joy1.get_axis(1) > 0.65:
                        currentSelection = 4
                    elif joy1.get_axis(1) < 0.65 and joy1.get_axis(1) > 0.25:
                        currentSelection = 3
                    elif joy1.get_axis(1) < 0.25 and joy1.get_axis(1) > -0.65: #Going Up
                        currentSelection = 2
                    elif joy1.get_axis(1) < -0.65:
                        currentSelection = 1

            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1: #--  Check to see if the Left Mouse Button is pressed
                    curX, curY = pygame.mouse.get_pos()  #-- Update curX and curY
                    if startGame.rect.collidepoint(curX,curY): #Start Game
                        playerselection,startMenu = slidingwindow(playerselection, startMenu, [titleScreen,playerselectionScreen], windowslidespeed, 'Horizontal', 'Right')
                        musiccheck = True
                        screen.fill(BLACK)
                        currentSelection = 1
                        menudrawOverride = True
                    if multiplayerButton.rect.collidepoint(curX, curY):
                        roomselection, startMenu  = slidingwindow(roomselection, startMenu, [titleScreen,playerselectionScreen], windowslidespeed, 'Horizontal', 'Right')
                        musiccheck = True
                        screen.fill(BLACK)
                        currentSelection = 1
                        clienthostselect = True
                        menudrawOverride = True
                    if optionButton.rect.collidepoint(curX,curY): #Options
                        options,startMenu = slidingwindow(options,startMenu, [titleScreen,optionScreen], windowslidespeed, 'Vertical', 'Bottom')
                        musiccheck = True
                        screen.fill(BLACK)
                        currentSelection = 1
                        menudrawOverride = True
                    if exitGame.rect.collidepoint(curX,curY): #Exit Game
                        gameLoop=False
                        startMenu=False

        if menudrawOverride == True:
            pass
        else:
            if currentSelection == 1:
                startGame.setimg(screen_width/8.0, screen_height/2.4285714285714284, screen_width/3.7267080745341614, screen_height/11.333333333333334, os.path.join('Resources', 'GUI', 'Play Game_select.png'))
                multiplayerButton.setimg(screen_width/8.0, screen_height/1.8888888888888888, screen_width/4.040404040404041, screen_height/17.0, os.path.join('Resources', 'GUI', 'Multiplayer.png'))
                optionButton.setimg(screen_width/8.0, screen_height/1.5454545454545454, screen_width/4.040404040404041, screen_height/17.0, os.path.join('Resources', 'GUI', 'Options.png'))
                exitGame.setimg(screen_width/8.0, screen_height/1.307692307692308, screen_width/4.040404040404041, screen_height/17.0, os.path.join('Resources', 'GUI', 'Exit Game.png'))
            elif currentSelection == 2:
                startGame.setimg(screen_width/8.0, screen_height/2.4285714285714284, screen_width/4.040404040404041, screen_height/17.0, os.path.join('Resources', 'GUI', 'Play Game.png'))
                multiplayerButton.setimg(screen_width/8.0, screen_height/1.8888888888888888, screen_width/3.7267080745341614, screen_height/11.333333333333334, os.path.join('Resources', 'GUI', 'Multiplayer_select.png'))
                optionButton.setimg(screen_width/8.0, screen_height/1.5454545454545454, screen_width/4.040404040404041, screen_height/17.0, os.path.join('Resources', 'GUI', 'Options.png'))
                exitGame.setimg(screen_width/8.0, screen_height/1.307692307692308, screen_width/4.040404040404041, screen_height/17.0, os.path.join('Resources', 'GUI', 'Exit Game.png'))
            elif currentSelection == 3:
                startGame.setimg(screen_width/8.0, screen_height/2.4285714285714284, screen_width/4.040404040404041, screen_height/17.0, os.path.join('Resources', 'GUI', 'Play Game.png'))
                multiplayerButton.setimg(screen_width/8.0, screen_height/1.8888888888888888, screen_width/4.040404040404041, screen_height/17.0, os.path.join('Resources', 'GUI', 'Multiplayer.png'))
                optionButton.setimg(screen_width/8.0, screen_height/1.5454545454545454, screen_width/3.7267080745341614, screen_height/11.333333333333334, os.path.join('Resources', 'GUI', 'Options_select.png'))
                exitGame.setimg(screen_width/8.0, screen_height/1.307692307692308, screen_width/4.040404040404041, screen_height/17.0, os.path.join('Resources', 'GUI', 'Exit Game.png'))
            elif currentSelection == 4:
                startGame.setimg(screen_width/8.0, screen_height/2.4285714285714284, screen_width/4.040404040404041, screen_height/17.0, os.path.join('Resources', 'GUI', 'Play Game.png'))
                multiplayerButton.setimg(screen_width/8.0, screen_height/1.8888888888888888, screen_width/4.040404040404041, screen_height/17.0, os.path.join('Resources', 'GUI', 'Multiplayer.png'))
                optionButton.setimg(screen_width/8.0, screen_height/1.5454545454545454, screen_width/4.040404040404041, screen_height/17.0, os.path.join('Resources', 'GUI', 'Options.png'))
                exitGame.setimg(screen_width/8.0, screen_height/1.307692307692308, screen_width/3.7267080745341614, screen_height/11.333333333333334, os.path.join('Resources', 'GUI', 'Exit Game_select.png'))

            titleMenu.draw(screen)

        if debugmode == True:
            curX, curY = pygame.mouse.get_pos()
            drawtxt(("Mouse Pos: " + str(curX) + "," + str(curY)), defaultfont, 15, WHITE, 10, 10, 180, 24, True)
        pygame.display.update()
        clock.tick(FPS) # Limit the Loop
        menudrawOverride = False

    if gameLoop != True:
        break
    # -------------------------------------------------------------------------------------------------------------------------------------------------------------- #

    def OPTIONS_LOOP():
        """ This is used to quickly jump to the Options Loop from the Code Explorer """
        pass


    menumax = 4
    while options == True:
        pygame.display.set_caption('Battle of Tyril     |     FPS: ' + str(clock.get_fps())) # Set the title of the window

        if musiccheck == True:
            pygame.mixer.music.load(optionsMusic)
            pygame.mixer.music.play(-1)
            musiccheck = False

        # Check Joystick Inputs and Init as required
        joystick_count = pygame.joystick.get_count()
        if joystick_count == 1 or joystick_count == 2 or joystick_count == 3  or joystick_count == 4: # Check up to all the joysticks
            if onejoystick == True: # to see if any are initialized
                pass # If onejoystick is already == True, Program knows that one has already been initalized
            else:
                # Use joystick #0 and initialize it
                joy1 = pygame.joystick.Joystick(0)
                joy1.init()
                onejoystick = True

            #------------- Start Code ---------------#
        screen.blit (optionScreen, (0,0))

        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # If user clicked close
                gameLoop = False # Flag that we are done so we exit this loop
                options = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    startMenu,options = slidingwindow(startMenu,options, [titleScreen,optionScreen], windowslidespeed, 'Vertical', 'Top')
                    musiccheck = True
                    currentSelection = 1
                    menudrawOverride = True

                if event.key == pygame.K_UP:
                    if currentSelection > 1:
                        currentSelection-=1
                    else: currentSelection = menumax
                if event.key == pygame.K_DOWN:
                    if currentSelection < menumax:
                        currentSelection+=1
                    else: currentSelection = 1
                if event.key == pygame.K_SPACE:
                    if currentSelection == 1:
                        resolutionChange(800,600,False)
                    elif currentSelection == 2:
                        resolutionChange(1024,768,False)
                    elif currentSelection == 3:
                        resolutionChange(1280,1024,False)
                    elif currentSelection == 4:
                        resolutionChange(screen_res_width,screen_res_height,True)

            if event.type == pygame.JOYBUTTONDOWN:
                if onejoystick == True:
                    if joy1.get_button(0):
                        if currentSelection == 1:
                            resolutionChange(800,600,False)
                        elif currentSelection == 2:
                            resolutionChange(1024,768,False)
                        elif currentSelection == 3:
                            resolutionChange(1280,1024,False)
                        elif currentSelection == 4:
                            resolutionChange(screen_res_width,screen_res_height,True)
                    if joy1.get_button(1): # If User Pressed the B Button
                        startMenu,options = slidingwindow(startMenu,options, [titleScreen,optionScreen], windowslidespeed, 'Vertical', 'Top')
                        musiccheck = True
                        currentSelection = 1
                        menudrawOverride = True
                    if joy1.get_button(6): # If User Pressed the Back Button
                        gameLoop=False
            if onejoystick == True:
                if event.type == pygame.JOYHATMOTION:
                    if joy1.get_hat(0) == (0,1): #Going Up
                        if currentSelection > 1:
                            currentSelection-=1
                        else:
                            currentSelection = menumax
                    if joy1.get_hat(0) == (0,-1): #Going Down
                        if currentSelection < menumax:
                            currentSelection+=1
                        else:
                            currentSelection = 1
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1: #--  Check to see if the Left Mouse Button is pressed
                    curX, curY = pygame.mouse.get_pos()  #-- Update curX and curY

        if menudrawOverride == True:
            pass
        else:
            if currentSelection == 1:
                op800x600.setimg(screen_width/60.0, screen_height/1.1888111888111887, screen_width/3.7267080745341614, screen_height/11.333333333333334, os.path.join('Resources', 'GUI', '800x600_select.png'))
                op1024x768.setimg(screen_width/4.0, screen_height/1.1888111888111887, screen_width/4.040404040404041, screen_height/17.0, os.path.join('Resources', 'GUI', '1024x768.png'))
                op1280x1024.setimg(screen_width/2.1052631578947367, screen_height/1.1888111888111887, screen_width/4.040404040404041, screen_height/17.0, os.path.join('Resources', 'GUI', '1280x1024.png'))
                fullscreen.setimg(screen_width/1.3793103448275863, screen_height/1.1888111888111887, screen_width/4.040404040404041, screen_height/17.0, os.path.join('Resources', 'GUI', 'Fullscreen.png'))
            elif currentSelection == 2:
                op800x600.setimg(screen_width/60.0, screen_height/1.1888111888111887, screen_width/4.040404040404041, screen_height/17.0, os.path.join('Resources', 'GUI', '800x600.png'))
                op1024x768.setimg(screen_width/4.0, screen_height/1.1888111888111887, screen_width/3.7267080745341614, screen_height/11.333333333333334, os.path.join('Resources', 'GUI', '1024x768_select.png'))
                op1280x1024.setimg(screen_width/2.1052631578947367, screen_height/1.1888111888111887, screen_width/4.040404040404041, screen_height/17.0, os.path.join('Resources', 'GUI', '1280x1024.png'))
                fullscreen.setimg(screen_width/1.3793103448275863, screen_height/1.1888111888111887, screen_width/4.040404040404041, screen_height/17.0, os.path.join('Resources', 'GUI', 'Fullscreen.png'))
            elif currentSelection == 3:
                op800x600.setimg(screen_width/60.0, screen_height/1.1888111888111887, screen_width/4.040404040404041, screen_height/17.0, os.path.join('Resources', 'GUI', '800x600.png'))
                op1024x768.setimg(screen_width/4.0, screen_height/1.1888111888111887, screen_width/4.040404040404041, screen_height/17.0, os.path.join('Resources', 'GUI', '1024x768.png'))
                op1280x1024.setimg(screen_width/2.1052631578947367, screen_height/1.1888111888111887, screen_width/3.7267080745341614, screen_height/11.333333333333334, os.path.join('Resources', 'GUI', '1280x1024_select.png'))
                fullscreen.setimg(screen_width/1.3793103448275863, screen_height/1.1888111888111887, screen_width/4.040404040404041, screen_height/17.0, os.path.join('Resources', 'GUI', 'Fullscreen.png'))
            elif currentSelection == 4:
                op800x600.setimg(screen_width/60.0, screen_height/1.1888111888111887, screen_width/4.040404040404041, screen_height/17.0, os.path.join('Resources', 'GUI', '800x600.png'))
                op1024x768.setimg(screen_width/4.0, screen_height/1.1888111888111887, screen_width/4.040404040404041, screen_height/17.0, os.path.join('Resources', 'GUI', '1024x768.png'))
                op1280x1024.setimg(screen_width/2.1052631578947367, screen_height/1.1888111888111887, screen_width/4.040404040404041, screen_height/17.0, os.path.join('Resources', 'GUI', '1280x1024.png'))
                fullscreen.setimg(screen_width/1.3793103448275863, screen_height/1.1888111888111887, screen_width/3.7267080745341614, screen_height/11.333333333333334, os.path.join('Resources', 'GUI', 'Fullscreen_select.png'))
            optionsMenu.draw(screen)
        if debugmode == True:
            curX, curY = pygame.mouse.get_pos()
            drawtxt(("Mouse Pos: " + str(curX) + "," + str(curY)), defaultfont, 15, WHITE, 10, 10, 180, 24, True)

        pygame.display.update()
        clock.tick(FPS) # Limit the Loop

    if gameLoop != True:
        break

    # ----------------------------------------------------------------------------------------------------------------------------------------------------------- #

    def ROOMSELECTION_LOOP():
        """ This is used to quickly jump to the Room Selection Loop from the Code Explorer """
        pass

    while roomselection == True:
        while clienthostselect == True:
            pygame.display.set_caption('Battle of Tyril     |     FPS: ' + str(clock.get_fps())) # Set the title of the window
            screen.blit (playerselectionScreen, (0,0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT: # If user clicked close
                    gameLoop = False
                    roomselection = False # Flag that we are done so we exit this loop
                    clienthostselect = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                            startMenu,roomselection = slidingwindow(startMenu,playerselection, [titleScreen,playerselectionScreen], windowslidespeed, 'Horizontal', 'Left')
                            musiccheck = True
                            currentSelection = 1
                            menudrawOverride = True
                            clienthostselect = False
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1: #--  Check to see if the Left Mouse Button is pressed
                        curX, curY = pygame.mouse.get_pos()  #-- Update curX and curY
                        if clientimg.rect.collidepoint(curX,curY):
                            clientIP = gethostbyname(gethostname())
                            screen.fill(BLACK)
                            currentSelection = 1
                            client = True
                            clienthostselect = False
                            roomwaiting = True
                        if hostimg.rect.collidepoint(curX,curY):
                            hostIP = gethostbyname(gethostname())
                            ADDR = (hostIP, PORT)
                            try:
                                serversock = socket(AF_INET, SOCK_STREAM)
                                serversock.bind(ADDR)
                                serversock.listen(2)
                            except: pass
                            connstat = 'Waiting For Connection ...'
                            screen.fill(BLACK)
                            currentSelection = 1
                            host = True
                            clienthostselect = False
                            roomwaiting = True
                if joystick_count != 0:
                    if event.type == JOYBUTTONDOWN:
                        if onejoystick == True:
                            if joy1.get_button(1): # If User Pressed the B Button
                                startMenu,roomselection = slidingwindow(startMenu,playerselection, [titleScreen,playerselectionScreen], windowslidespeed, 'Horizontal', 'Left')
                                musiccheck = True
                                currentSelection = 1
                                menudrawOverride = True
                                clienthostselect = False
            cliho.draw(screen)
            pygame.display.update()
            clock.tick(FPS) # Limit the Loop


            # -------------------------------------------------------- #
        while client == True:
            pygame.display.set_caption('Battle of Tyril     |     FPS: ' + str(clock.get_fps())) # Set the title of the window
            screen.blit (playerselectionScreen, (0,0))
            for event in pygame.event.get(): # User did something
                if event.type == pygame.QUIT: # If user clicked close
                    gameLoop = False
                    client = False
                    roomselection = False # Flag that we are done so we exit this loop
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        musiccheck = True
                        currentSelection = 1
                        menudrawOverride = True
                        client = False
                        clienthostselect = True

                    if event.key == pygame.K_PERIOD or event.key == pygame.K_KP_PERIOD:
                        serverIPList.append('.')
                    if event.key == pygame.K_0 or event.key == pygame.K_KP0:
                        serverIPList.append('0')
                    if event.key == pygame.K_1 or event.key == pygame.K_KP1:
                        serverIPList.append('1')
                    if event.key == pygame.K_2 or event.key == pygame.K_KP2:
                        serverIPList.append('2')
                    if event.key == pygame.K_3 or event.key == pygame.K_KP3:
                        serverIPList.append('3')
                    if event.key == pygame.K_4 or event.key == pygame.K_KP4:
                        serverIPList.append('4')
                    if event.key == pygame.K_5 or event.key == pygame.K_KP5:
                        serverIPList.append('5')
                    if event.key == pygame.K_6 or event.key == pygame.K_KP6:
                        serverIPList.append('6')
                    if event.key == pygame.K_7 or event.key == pygame.K_KP7:
                        serverIPList.append('7')
                    if event.key == pygame.K_8 or event.key == pygame.K_KP8:
                        serverIPList.append('8')
                    if event.key == pygame.K_9 or event.key == pygame.K_KP9:
                        serverIPList.append('9')

                    if event.key == pygame.K_BACKSPACE or event.key == pygame.K_DELETE:
                        try:
                            serverIPList.pop()
                        except: pass
                    if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                        serverIP = ''.join(serverIPList)
                        if len(serverIP) >=  11 and len(serverIP) <= 13:
                            ADDR = (serverIP, PORT)
                            connstat = True
                            try:
                                tcpCliSock = socket(AF_INET, SOCK_STREAM)
                                tcpCliSock.connect(ADDR)
                                try:
                                    USERFILES = [[screen_width,screen_height, combscreen, winenvirX, winenvirY], serverIPList]
                                    userfile = open (os.path.join('Program Files', 'Userfiles.dll'), 'wb')
                                    pickle.dump(USERFILES, userfile)
                                    userfile.close()
                                except: pass
                                clientt = True
                                break
                            except: connstat = False
                        else: serverIPList, connstat  = [], 'Incorrect IP'
                if joystick_count != 0:
                    if event.type == JOYBUTTONDOWN:
                        if onejoystick == True:
                            if joy1.get_button(1): # If User Pressed the B Button
                                musiccheck = True
                                currentSelection = 1
                                menudrawOverride = True
                                client = False
                                clienthostselect = True

            drawtxt('MY IP: ' + clientIP, gamefont, int(combscreen/144.0),WHITE, screen_width/5.12,screen_height/4.096, 1, 1, False)
            drawtxt('Please Type in the HOST IP: ' + ''.join(serverIPList), gamefont, int(combscreen/102),WHITE, screen_width/7.0,screen_height/4.615384615384615, 1, 1, False)
            if connstat == True:
                drawtxt('Attempting to Connect ...', gamefont, int(combscreen/102),WHITE, screen_width/1.6,screen_height/4.615384615384615, screen_width/3.1449631449631448, screen_height/40.0, True)
            elif connstat == False:
                drawtxt('Error Connecting To Server', gamefont, int(combscreen/102),WHITE, screen_width/1.6,screen_height/4.615384615384615, screen_width/3.1449631449631448, screen_height/40.0, True)
            elif connstat == 'Incorrect IP':
                drawtxt('Incorrect IP Format (xxx.xxx.x.xxx)', gamefont, int(combscreen/102),WHITE, screen_width/1.6,screen_height/4.615384615384615, screen_width/2.6834381551362685, screen_height/40.0, True)

            if clientt == True:
                playerselection = True
                multiselection = True
                clientt = False
                roomselection = False
                break

            if debugmode == True:
                curX, curY = pygame.mouse.get_pos()
                drawtxt(("Mouse Pos: " + str(curX) + "," + str(curY)), defaultfont, 15, WHITE, 10, 10, 180, 24, True)
            pygame.display.update()
            clock.tick(FPS) # Limit the Loop
                # -------------------------------------------------------- #

        while host == True:
            screen.blit (playerselectionScreen, (0,0))
            for event in pygame.event.get(): # User did something
                if event.type == pygame.QUIT: # If user clicked close
                    gameLoop = False
                    host = False
                    roomselection = False # Flag that we are done so we exit this loop
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        musiccheck = True
                        currentSelection = 1
                        menudrawOverride = True
                        host = False
                        clienthostselect = True
                if joystick_count != 0:
                    if event.type == JOYBUTTONDOWN:
                        if onejoystick == True:
                            if joy1.get_button(1): # If User Pressed the B Button
                                musiccheck = True
                                currentSelection = 1
                                menudrawOverride = True
                                host = False
                                clienthostselect = True

            drawtxt('MY IP: ' + hostIP, gamefont, int(combscreen/144.0),WHITE, screen_width/5.12,screen_height/4.096, 1, 1, False)
            drawtxt(connstat, gamefont, int(combscreen/102),WHITE, screen_width/7.0,screen_height/4.615384615384615, 1, 1, False)
            pygame.display.update()

            try:
                clientsock, addr = serversock.accept()
                host = True
            except: pass

            screen.blit (playerselectionScreen, (0,0))
            drawtxt('...Connected from: ' + str(addr[0]) + ' At Port: ' + str(addr[1]), gamefont, int(combscreen/102),WHITE, screen_width/7.0,screen_height/4.615384615384615, 1, 1, False)
            pygame.display.update()
            clock.tick(FPS) # Limit the Loop
            if host == True:
                playerselection = True
                roomselection = False
                multiselection = True
                break
    # ----------------------------------------------------------------------------------------------------------------------------------------------------------- #

    def PLAYERSELECTION_LOOP():
        """ This is used to quickly jump to the GameOver Loop from the Code Explorer """
        pass

    menumax = 2
    while playerselection == True:
        pygame.display.set_caption('Battle of Tyril     |     FPS: ' + str(clock.get_fps())) # Set the title of the window

        if multiselection == False:
            # Check Joystick Inputs and Init as required
            if onejoystick == True and twojoystick == True and threejoystick == True and fourjoystick == True:
                pass
            else:
                joystick_count = pygame.joystick.get_count()
                if joystick_count == 1:
                    if onejoystick == True:
                        pass
                    else:
                        # Use joystick #0 and initialize it
                        joy1 = pygame.joystick.Joystick(0)
                        joy1.init()
                        onejoystick = True
                if joystick_count == 2:
                    if twojoystick == True:
                        pass
                    else:
                        # Use joystick #1 and initialize them
                        joy2 = pygame.joystick.Joystick(1)
                        joy2.init()
                        twojoystick = True
                if joystick_count == 3:
                    if threejoystick == True:
                        pass
                    else:
                        # Use joystick #0 and initialize it
                        joy1 = pygame.joystick.Joystick(0)
                        joy1.init()
                        onejoystick = True
                        joy2 = pygame.joystick.Joystick(1)
                        joy2.init()
                        twojoystick = True
                        # Use joystick #2 and initialize them
                        joy3 = pygame.joystick.Joystick(2)
                        joy3.init()
                        threejoystick = True
                if joystick_count == 4:
                    if fourjoystick == True:
                        pass
                    else:
                        # Use joystick #3 and initialize them
                        joy4 = pygame.joystick.Joystick(3)
                        joy4.init()
                        fourjoystick = True
                #------------- Start Code ---------------#
            screen.blit (playerselectionScreen, (0,0))

            for event in pygame.event.get(): # User did something
                if event.type == pygame.QUIT: # If user clicked close
                    gameLoop = False
                    playerselection = False # Flag that we are done so we exit this loop
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        startMenu,playerselection = slidingwindow(startMenu,playerselection, [titleScreen,playerselectionScreen], windowslidespeed, 'Horizontal', 'Left')
                        menudrawOverride = True
                        musiccheck = True
                    if event.key == pygame.K_SPACE:
                        player1 = Actor.Actor( screen_width/8.0,screen_height/2.4285714285714284, screen_width, screen_height, SHIPS[p1currentselect], PLAYERWEAPONS, 100, 1 )
                        players.add(player1)
                        player1.set_walls(impassable_barrier)
                        p1ready = True
                    if event.key == pygame.K_UP:
                        if p1currentselect > 1:
                            p1currentselect-=1
                        else: p1currentselect = menumax
                    if event.key == pygame.K_DOWN:
                        if p1currentselect < menumax:
                            p1currentselect+=1
                        else: p1currentselect = 1
                if joystick_count != 0:
                    if event.type == JOYBUTTONDOWN:
                        if onejoystick == True:
                            if joy1.get_button(1): # If User Pressed the B Button
                                startMenu,playerselection = slidingwindow(startMenu,playerselection, [titleScreen,playerselectionScreen], windowslidespeed, 'Horizontal', 'Left')
                                musiccheck = True
                                currentSelection = 1
                                menudrawOverride = True
                            if joy1.get_button(2):
                                startMenu,playerselection = slidingwindow(startMenu,playerselection, [titleScreen,playerselectionScreen], windowslidespeed, 'Horizontal', 'Left')
                                menudrawOverride = True
                                musiccheck = True
                            if joy1.get_button(7):
                                if p1joined == True:
                                    player1 = Actor.Actor( screen_width/8.0,screen_height/2.4285714285714284, screen_width, screen_height, SHIPS[p1currentselect], PLAYERWEAPONS, 100, 1 )
                                    if p1ready == False:
                                        players.add(player1)
                                        player1.set_walls(impassable_barrier)
                                        p1ready = True
                                    else:
                                        player1.kill()
                                        p1ready = False
                                else:
                                    p1joined = True
                            if joy1.get_button(6):
                                if p1joined == True:
                                    p1joined = False
                                    p1ready = False
                        if twojoystick == True:
                            if joy2.get_button(7):
                                if p2joined == True:
                                    player2 = Actor.Actor( screen_width/8.0,screen_height/2.4285714285714284, screen_width, screen_height, SHIPS[p2currentselect], PLAYERWEAPONS, 100, 2 )
                                    if p2ready == False:
                                        players.add(player2)
                                        player2.set_walls(impassable_barrier)
                                        p2ready = True
                                    else:
                                        player2.kill()
                                        p2ready = False
                                else:
                                    p2joined = True
                            if joy2.get_button(6):
                                if p2joined == True:
                                    player2.kill()
                                    p2joined = False
                                    p2ready = False
                        if threejoystick == True:
                            if joy3.get_button(7):
                                if p3joined == True:
                                    player3 = Actor.Actor( screen_width/8.0,screen_height/2.4285714285714284, screen_width, screen_height, SHIPS[p3currentselect], PLAYERWEAPONS, 100, 3 )
                                    if p3ready == False:
                                        players.add(player3)
                                        player3.set_walls(impassable_barrier)
                                        p3ready = True
                                    else:
                                        player3.kill()
                                        p3ready = False
                                else:
                                    p3joined = True
                            if joy3.get_button(6):
                                if p3joined == True:
                                    player3.kill()
                                    p3joined = False
                                    p3ready = False
                        if fourjoystick == True:
                            if joy4.get_button(7):
                                if p4joined == True:
                                    player4 = Actor.Actor( screen_width/8.0,screen_height/2.4285714285714284, screen_width, screen_height, SHIPS[p4currentselect], PLAYERWEAPONS, 100, 4 )
                                    if p4ready == False:
                                        players.add(player4)
                                        player4.set_walls(impassable_barrier)
                                        p4ready = True
                                    else:
                                        player4.kill()
                                        p4ready = False
                                else:
                                    p4joined = True
                            if joy4.get_button(6):
                                if p4joined == True:
                                    player4.kill()
                                    p4joined = False
                                    p4ready = False
                    if event.type == JOYHATMOTION:
                        if onejoystick == True:
                            if p1joined == True:
                                if p1ready != True:
                                    if joy1.get_hat(0) == (0,1): #Going Up
                                        if p1currentselect > 1:
                                            p1currentselect-=1
                                        else:
                                            p1currentselect=menumax
                                    if joy1.get_hat(0) == (0,-1): #Going Down
                                        if p1currentselect < menumax:
                                            p1currentselect+=1
                                        else:
                                            p1currentselect=1
                        if twojoystick == True:
                            if p2joined == True:
                                if p2ready != True:
                                    if joy2.get_hat(0) == (0,1): #Going Up
                                        if p2currentselect > 1:
                                            p2currentselect-=1
                                        else:
                                            p2currentselect=menumax
                                    if joy2.get_hat(0) == (0,-1): #Going Down
                                        if p2currentselect < menumax:
                                            p2currentselect+=1
                                        else:
                                            p2currentselect=1
                        if threejoystick == True:
                            if p3joined == True:
                                if p3ready != True:
                                    if joy3.get_hat(0) == (0,1): #Going Up
                                        if p3currentselect > 1:
                                            p3currentselect-=1
                                        else:
                                            p3currentselect=menumax
                                    if joy3.get_hat(0) == (0,-1): #Going Down
                                        if p3currentselect < menumax:
                                            p3currentselect+=1
                                        else:
                                            p3currentselect=1
                        if fourjoystick == True:
                            if p4joined == True:
                                if p4ready != True:
                                    if joy4.get_hat(0) == (0,1): #Going Up
                                        if p4currentselect > 1:
                                            p4currentselect-=1
                                        else:
                                            p4currentselect=menumax
                                    if joy4.get_hat(0) == (0,-1): #Going Down
                                        if p4currentselect < menumax:
                                            p4currentselect+=1
                                        else:
                                            p4currentselect=1

                if event.type == MOUSEBUTTONDOWN: # Bonus Modes Screen
                    if event.button == 1: #--  Check to see if the Left Mouse Button is pressed
                        curX, curY = pygame.mouse.get_pos()  #-- Update curX and curY
                        if bmodes.rect.collidepoint(curX,curY): #Bonus Modes
                            if ACHIVEMENTS [5][3] == True:  # Set up the Bonus's and unlock screen
                                bonusplayselect.add(cat)
                            if ACHIVEMENTS [6][3] == True:
                                bonusplayselect.add(dog)
                            if ACHIVEMENTS[7][3] == True:
                                bonusplayselect.add(troll)
                            bmodes.setimg (screen_width/8.0, screen_height/3.6363636363636362, screen_width/4.040404040404041, screen_height/17.0, os.path.join('Resources', 'GUI', 'Go Back.png'))
                            bonus = True
                            while bonus == True:
                                screen.blit (playerselectionScreen, (0,0))
                                bonusplayselect.draw(screen)
                                pygame.display.update()
                                for event in pygame.event.get():
                                    if event.type == pygame.QUIT: # If user clicked close
                                        gameLoop = False
                                        playerselection = False # Flag that we are done so we exit this loop
                                        bonus = False
                                    if event.type == MOUSEBUTTONDOWN:
                                        if event.button == 1:
                                            curX, curY = pygame.mouse.get_pos()  #-- Update curX and curY
                                            if bmodes.rect.collidepoint(curX,curY):
                                                bmodes.setimg(screen_width/8.0, screen_height/3.6363636363636362, screen_width/4.040404040404041, screen_height/17.0, os.path.join('Resources', 'GUI', 'Bonus Modes.png'))
                                                bonus = False
                                                cat.kill()
                                                dog.kill()
                                                troll.kill()
                                            if ACHIVEMENTS [5][3] == True:
                                                if cat.rect.collidepoint(curX,curY):
                                                    aiseconds = 5
                                                    if joystick_count != 0:
                                                        if onejoystick == True:
                                                            player1 = Actor.Actor( screen_width/8.0,screen_height/2.4285714285714284, screen_width, screen_height, os.path.join('Resources', 'Bonus Modes', 'Nyan', 'Nyan Cat.png'), PLAYERWEAPONS, 100, 1 )
                                                            players.add(player1)
                                                            player1.set_walls(impassable_barrier)
                                                            p1ready,p1joined = True, True
                                                        if twojoystick == True:
                                                            player2 = Actor.Actor( screen_width/8.0,screen_height/2.4285714285714284, screen_width, screen_height, os.path.join('Resources', 'Bonus Modes', 'Nyan', 'Nyan Cat.png'), PLAYERWEAPONS, 100, 2 )
                                                            players.add(player2)
                                                            player2.set_walls(impassable_barrier)
                                                            p2ready, p2joined = True, True
                                                        if threejoystick == True:
                                                            player3 = Actor.Actor( screen_width/8.0,screen_height/2.4285714285714284, screen_width, screen_height, os.path.join('Resources', 'Bonus Modes', 'Nyan', 'Nyan Cat.png'), PLAYERWEAPONS, 100, 3 )
                                                            players.add(player3)
                                                            player3.set_walls(impassable_barrier)
                                                            p3ready, p3joined = True, True
                                                        if fourjoystick == True:
                                                            player4 = Actor.Actor( screen_width/8.0,screen_height/2.4285714285714284, screen_width, screen_height, os.path.join('Resources', 'Bonus Modes', 'Nyan', 'Nyan Cat.png'), PLAYERWEAPONS, 100, 4 )
                                                            players.add(player4)
                                                            player4.set_walls(impassable_barrier)
                                                            p4ready, p4joined = True, True
                                                    else:
                                                        player1 = Actor.Actor( screen_width/8.0,screen_height/2.4285714285714284, screen_width, screen_height, os.path.join('Resources', 'Bonus Modes', 'Nyan', 'Nyan Cat.png'), PLAYERWEAPONS, 100, 1 )
                                                        players.add(player1)
                                                        player1.set_walls(impassable_barrier)
                                                        p1ready = True

                                                    bonus = False
                                                    bmodes.setimg(screen_width/8.0, screen_height/3.6363636363636362, screen_width/4.040404040404041, screen_height/17.0, os.path.join('Resources', 'GUI', 'Bonus Modes.png'))
                                                    cat.kill()
                                                    dog.kill()
                                                    troll.kill()
                                                    nyancatmode = True #Bonus Mode Controll
                                            if ACHIVEMENTS [6][3] == True:
                                                if dog.rect.collidepoint(curX,curY):
                                                    aiseconds = 5
                                                    if joystick_count != 0:
                                                        if onejoystick == True:
                                                            player1 = Actor.Actor( screen_width/8.0,screen_height/2.4285714285714284, screen_width, screen_height, os.path.join('Resources', 'Bonus Modes', 'Nyan', 'Nyan Dog.png'), PLAYERWEAPONS, 100, 1 )
                                                            players.add(player1)
                                                            player1.set_walls(impassable_barrier)
                                                            p1ready = True
                                                        if twojoystick == True:
                                                            player2 = Actor.Actor( screen_width/8.0,screen_height/2.4285714285714284, screen_width, screen_height, os.path.join('Resources', 'Bonus Modes', 'Nyan', 'Nyan Dog.png'), PLAYERWEAPONS, 100, 2 )
                                                            players.add(player2)
                                                            player2.set_walls(impassable_barrier)
                                                            p2ready = True
                                                        if threejoystick == True:
                                                            player3 = Actor.Actor( screen_width/8.0,screen_height/2.4285714285714284, screen_width, screen_height, os.path.join('Resources', 'Bonus Modes', 'Nyan', 'Nyan Dog.png'), PLAYERWEAPONS, 100, 3 )
                                                            players.add(player3)
                                                            player3.set_walls(impassable_barrier)
                                                            p3ready = True
                                                        if fourjoystick == True:
                                                            player4 = Actor.Actor( screen_width/8.0,screen_height/2.4285714285714284, screen_width, screen_height, os.path.join('Resources', 'Bonus Modes', 'Nyan', 'Nyan Dog.png'), PLAYERWEAPONS, 100, 4 )
                                                            players.add(player4)
                                                            player4.set_walls(impassable_barrier)
                                                            p4ready = True
                                                    else:
                                                        player1 = Actor.Actor( screen_width/8.0,screen_height/2.4285714285714284, screen_width, screen_height, os.path.join('Resources', 'Bonus Modes', 'Nyan', 'Nyan Dog.png'), PLAYERWEAPONS, 100, 1 )
                                                        players.add(player1)
                                                        player1.set_walls(impassable_barrier)
                                                        p1ready = True
                                                    bonus = False
                                                    bmodes.setimg(screen_width/8.0, screen_height/3.6363636363636362, screen_width/4.040404040404041, screen_height/17.0, os.path.join('Resources', 'GUI', 'Bonus Modes.png'))
                                                    cat.kill()
                                                    dog.kill()
                                                    troll.kill()
                                                    nyandogmode = True #Bonus Mode Controll
                                            if ACHIVEMENTS [7][3] == True:
                                                if troll.rect.collidepoint(curX,curY):
                                                    aiseconds = 5
                                                    aiincrease = 10
                                                    if joystick_count != 0:
                                                        if onejoystick == True:
                                                            player1 = Actor.Actor( screen_width/8.0,screen_height/2.4285714285714284, screen_width, screen_height, os.path.join('Resources', 'Bonus Modes', 'Troll', 'Troll.png'), PLAYERWEAPONS, 100, 1 )
                                                            players.add(player1)
                                                            player1.set_walls(impassable_barrier)
                                                            p1ready = True
                                                        if twojoystick == True:
                                                            player2 = Actor.Actor( screen_width/8.0,screen_height/2.4285714285714284, screen_width, screen_height, os.path.join('Resources', 'Bonus Modes', 'Troll', 'Troll.png'), PLAYERWEAPONS, 100, 2 )
                                                            players.add(player2)
                                                            player2.set_walls(impassable_barrier)
                                                            p2ready = True
                                                        if threejoystick == True:
                                                            player3 = Actor.Actor( screen_width/8.0,screen_height/2.4285714285714284, screen_width, screen_height, os.path.join('Resources', 'Bonus Modes', 'Troll', 'Troll.png'), PLAYERWEAPONS, 100, 3 )
                                                            players.add(player3)
                                                            player3.set_walls(impassable_barrier)
                                                            p3ready = True
                                                        if fourjoystick == True:
                                                            player4 = Actor.Actor( screen_width/8.0,screen_height/2.4285714285714284, screen_width, screen_height, os.path.join('Resources', 'Bonus Modes', 'Troll', 'Troll.png'), PLAYERWEAPONS, 100, 4 )
                                                            players.add(player4)
                                                            player4.set_walls(impassable_barrier)
                                                            p4ready = True
                                                    else:
                                                        player1 = Actor.Actor( screen_width/8.0,screen_height/2.4285714285714284, screen_width, screen_height, os.path.join('Resources', 'Bonus Modes', 'Troll', 'Troll.png'), PLAYERWEAPONS, 100, 1 )
                                                        players.add(player1)
                                                        player1.set_walls(impassable_barrier)
                                                        p1ready = True
                                                    bonus = False
                                                    bmodes.setimg(screen_width/8.0, screen_height/3.6363636363636362, screen_width/4.040404040404041, screen_height/17.0, os.path.join('Resources', 'GUI', 'Bonus Modes.png'))
                                                    cat.kill()
                                                    dog.kill()
                                                    troll.kill()
                                                    trololmode = True #Bonus Mode Controll

            if joystick_count != 0:
                if onejoystick == True:
                    if p1joined == True:
                        drawtxt('Player 1', defaultfont, int(combscreen/102.5), WHITE, screen_width/1.935483870967742, screen_height/3.4, 0, 0, False)
                        pygame.draw.rect(screen, BLACK, (screen_width/1.6326530612244898, screen_height/3.8636363636363638, screen_width/19.35483870967742, screen_height/12.142857142857142))

                        screen.blit(LOADEDSHIPS[p1currentselect], (screen_width/1.610738255033557, screen_height/3.794642857142857))
                        if p1ready == True:
                            drawtxt('READY!', defaultfont, int(combscreen/102.5), RED, screen_width/1.4285714285714286, screen_height/3.4, 0, 0, False)
                        else:
                            drawtxt('Not Ready', defaultfont, int(combscreen/102.5), WHITE, screen_width/1.4285714285714286, screen_height/3.4, 0, 0, False)
                    else:
                        drawtxt('Press Start To Join', defaultfont, int(combscreen/102.5), WHITE, screen_width/1.935483870967742, screen_height/3.4, 0, 0, False)
                if twojoystick == True:
                    if p2joined == True:
                        drawtxt('Player 2', defaultfont, int(combscreen/102.5), WHITE, screen_width/1.935483870967742, screen_height/2.125, 0, 0, False)
                        pygame.draw.rect(screen, BLACK, (screen_width/1.6326530612244898, screen_height/2.2972972972972974,screen_width/19.35483870967742, screen_height/12.142857142857142))

                        screen.blit(LOADEDSHIPS[p2currentselect], (screen_width/1.610738255033557, screen_height/2.272727272727273))

                        if p2ready == True:
                            drawtxt('READY!', defaultfont, int(combscreen/102.5), RED, screen_width/1.4285714285714286, screen_height/2.125, 0, 0, False)
                        else:
                            drawtxt('Not Ready', defaultfont, int(combscreen/102.5), WHITE, screen_width/1.4285714285714286, screen_height/2.125, 0, 0, False)
                    else:
                        drawtxt('Press Start To Join', defaultfont, int(combscreen/102.5), WHITE, screen_width/1.935483870967742, screen_height/2.125, 0, 0, False)
                if threejoystick == True:
                    if p3joined == True:
                        drawtxt('Player 3', defaultfont, int(combscreen/102.5), WHITE, screen_width/1.935483870967742, screen_height/1.5454545454545454, 0, 0, False)
                        pygame.draw.rect(screen, BLACK, (screen_width/1.6326530612244898, screen_height/1.6346153846153846, screen_width/19.35483870967742, screen_height/12.142857142857142))

                        screen.blit(LOADEDSHIPS[p3currentselect], (screen_width/1.610738255033557, screen_height/1.6221374045801527))

                        if p3ready == True:
                            drawtxt('READY!', defaultfont, int(combscreen/102.5), RED, screen_width/1.4285714285714286, screen_height/1.5454545454545454, 0, 0, False)
                        else:
                            drawtxt('Not Ready', defaultfont, int(combscreen/102.5), WHITE, screen_width/1.4285714285714286, screen_height/1.5454545454545454, 0, 0, False)

                    else:
                        drawtxt('Press Start To Join', defaultfont, int(combscreen/102.5), WHITE, screen_width/1.935483870967742, screen_height/1.5454545454545454, 0, 0, False)
                if fourjoystick == True:
                    if p4joined == True:
                        drawtxt('Player 4', defaultfont, int(combscreen/102.5), WHITE, screen_width/1.935483870967742, screen_height/1.2142857142857142, 0, 0, False)
                        pygame.draw.rect(screen, BLACK, (screen_width/1.63265306122448986, screen_height/1.2686567164179106, screen_width/19.35483870967742, screen_height/12.142857142857142))

                        screen.blit(LOADEDSHIPS[p4currentselect], (screen_width/1.610738255033557, screen_height/1.261127596439169))

                        if p4ready == True:
                            drawtxt('READY!', defaultfont, int(combscreen/102.5), RED, screen_width/1.4285714285714286, screen_height/1.2142857142857142, 0, 0, False)
                        else:
                            drawtxt('Not Ready', defaultfont, int(combscreen/102.5), WHITE, screen_width/1.4285714285714286, screen_height/1.2142857142857142, 0, 0, False)
                    else:
                        drawtxt('Press Start To Join', defaultfont, int(combscreen/102.5), WHITE, screen_width/1.935483870967742, screen_height/1.2142857142857142, 0, 0, False)

                if joystick_count == 1:
                    if p1ready == True:
                        playerselection = False
                        game = True
                        musiccheck = True
                        pygame.time.set_timer(TIMECOUNTER, 1000) # After 1 Second
                elif joystick_count == 2:
                    if p1ready == True and p2ready == True:
                        playerselection = False
                        game = True
                        musiccheck = True
                        pygame.time.set_timer(TIMECOUNTER, 1000) # After 1 Second
                elif joystick_count == 3:
                    if p1ready == True and p2ready == True and p3ready == True:
                        playerselection = False
                        game = True
                        musiccheck = True
                        pygame.time.set_timer(TIMECOUNTER, 1000) # After 1 Second
                elif joystick_count == 4:
                    if p1ready == True and p2ready == True and p3ready == True and p4ready == True:
                        playerselection = False
                        game = True
                        musiccheck = True
                        pygame.time.set_timer(TIMECOUNTER, 1000) # After 1 Second
            else:
                p1joined = True
                drawtxt('Player 1', defaultfont, int(combscreen/102.5), WHITE, screen_width/1.935483870967742, screen_height/3.4, 0, 0, False)
                pygame.draw.rect(screen, BLACK, (screen_width/1.6326530612244898, screen_height/3.8636363636363638, screen_width/19.35483870967742, screen_height/12.142857142857142))

                screen.blit(LOADEDSHIPS[p1currentselect], (screen_width/1.610738255033557, screen_height/3.794642857142857))

                if p1ready == True:
                    drawtxt('READY!', defaultfont, int(combscreen/102.5), RED, screen_width/1.4285714285714286, screen_height/3.4, 0, 0, False)
                    playerselection = False
                    game = True
                    musiccheck = True
                    pygame.time.set_timer(TIMECOUNTER, 1000) # After 1 Second
                else:
                    drawtxt('Not Ready', defaultfont, int(combscreen/102.5), WHITE, screen_width/1.4285714285714286, screen_height/3.4, 0, 0, False)
            bonusplayselect.draw(screen)

            if debugmode == True:
                curX, curY = pygame.mouse.get_pos()
                drawtxt(("Mouse Pos: " + str(curX) + "," + str(curY)), defaultfont, 15, WHITE, 10, 10, 180, 24, True)
            pygame.display.update ()


                            #------------------------- Client and Host -------------------------#
        else:
            if client == True:
                # Check Joystick Inputs and Init as required
                if onejoystick == True and twojoystick == True and threejoystick == True and fourjoystick == True:
                    pass
                else:
                    joystick_count = pygame.joystick.get_count()
                    if joystick_count == 1:
                        if onejoystick == True:
                            pass
                        else:
                            # Use joystick #0 and initialize it
                            joy1 = pygame.joystick.Joystick(0)
                            joy1.init()
                            onejoystick = True
                for event in pygame.event.get(): # User did something
                    if event.type == pygame.QUIT: # If user clicked close
                        gameLoop = False
                        playerselection = False # Flag that we are done so we exit this loop
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            playerselection = False
                            clienthostselect = True
                            roomselection = True
                            menudrawOverride = True
                            musiccheck = True
                            client = False
                        if event.key == pygame.K_SPACE:
                            if multiplayerselect[1][1] == False:
                                client_actor = Actor.Actor( screen_width/8.0,screen_height/2.4285714285714284, screen_width, screen_height, SHIPS[multiplayerselect[0][0]], PLAYERWEAPONS, 100, 1, 'Client' )
                                players.add(client_actor)
                                client_actor.set_walls(impassable_barrier)
                                multiplayerselect[1][1] = True
                            else:
                                client_actor.kill()
                                multiplayerselect[1][1] = False
                        if event.key == pygame.K_UP:
                            if multiplayerselect[1][0] > 1:
                                multiplayerselect[1][0]-=1
                            else: multiplayerselect[1][0] = menumax
                        if event.key == pygame.K_DOWN:
                            if multiplayerselect[1][0] < menumax:
                                multiplayerselect[1][0]+=1
                            else: multiplayerselect[1][0] = 1
                    if event.type == JOYHATMOTION:
                        if multiplayerselect[1][1] != True:
                            if joy1.get_hat(0) == (0,1): #Going Up
                                if multiplayerselect[1][0] > 1:
                                    multiplayerselect[1][0]-=1
                                else:
                                    multiplayerselect[1][0]=menumax
                            if joy1.get_hat(0) == (0,-1): #Going Down
                                if multiplayerselect[1][0] < menumax:
                                    multiplayerselect[1][0]+=1
                                else:
                                    multiplayerselect[1][0]=1
                    if event.type == JOYBUTTONDOWN:
                            if joy1.get_button(6):
                                playerselection = False
                                clienthostselect = True
                                roomselection = True
                                menudrawOverride = True
                                musiccheck = True
                                client = False
                            if joy1.get_button(7):
                                if multiplayerselect[1][1] == False:
                                    client_actor = Actor.Actor( screen_width/8.0,screen_height/2.4285714285714284, screen_width, screen_height, SHIPS[multiplayerselect[1][0]], PLAYERWEAPONS, 100, 1, 'Client' )
                                    players.add(client_actor)
                                    client_actor.set_walls(impassable_barrier)
                                    multiplayerselect[1][1] = True
                                else:
                                    client_actor.kill()
                                    multiplayerselect[1][1] = False

                    #------------- Start Code ---------------#
                try:
                    clientdata = pickle.dumps(multiplayerselect[1],True)
                    tcpCliSock.send(clientdata)
                    hostdata = tcpCliSock.recv(1024)
                    multiplayerselect[0] = pickle.loads(hostdata)
                except:
                    playerselection = False
                    clienthostselect = True
                    roomselection = False
                    startMenu = True
                    menudrawOverride = True
                    musiccheck = True
                    client = False
                screen.blit (playerselectionScreen, (0,0))

                    #--Client Show--#
                drawtxt('Client', defaultfont, int(combscreen/102.5), WHITE, screen_width/1.935483870967742, screen_height/3.4, 0, 0, False)
                pygame.draw.rect(screen, BLACK, (screen_width/1.6326530612244898, screen_height/3.8636363636363638, screen_width/19.35483870967742, screen_height/12.142857142857142))
                screen.blit(LOADEDSHIPS[multiplayerselect[1][0]], (screen_width/1.610738255033557, screen_height/3.794642857142857))
                if multiplayerselect[1][1] == True:
                    drawtxt('READY!', defaultfont, int(combscreen/102.5), RED, screen_width/1.4285714285714286, screen_height/3.4, 0, 0, False)
                else:
                    drawtxt('Not Ready', defaultfont, int(combscreen/102.5), WHITE, screen_width/1.4285714285714286, screen_height/3.4, 0, 0, False)
                    #--Host Show--#
                drawtxt('Host', defaultfont, int(combscreen/102.5), WHITE, screen_width/1.935483870967742, screen_height/2.125, 0, 0, False)
                pygame.draw.rect(screen, BLACK, (screen_width/1.6326530612244898, screen_height/2.2972972972972974,screen_width/19.35483870967742, screen_height/12.142857142857142))
                screen.blit(LOADEDSHIPS[multiplayerselect[0][0]], (screen_width/1.610738255033557, screen_height/2.272727272727273))
                if multiplayerselect[0][1] == True:
                    drawtxt('READY!', defaultfont, int(combscreen/102.5), RED, screen_width/1.4285714285714286, screen_height/2.125, 0, 0, False)
                else:
                    drawtxt('Not Ready', defaultfont, int(combscreen/102.5), WHITE, screen_width/1.4285714285714286, screen_height/2.125, 0, 0, False)

                if multiplayerselect[0][1] == True and multiplayerselect[1][1] == True:
                    host_actor = Actor.Actor( screen_width/8.0,screen_height/2.4285714285714284, screen_width, screen_height, SHIPS[multiplayerselect[0][0]], PLAYERWEAPONS, 100, 1, 'Host' )
                    players.add(host_actor)
                    host_actor.set_walls(impassable_barrier)

                    playerselection = False
                    musiccheck = True
                    multiplayermode = True

                if debugmode == True:
                    curX, curY = pygame.mouse.get_pos()
                    drawtxt(("Mouse Pos: " + str(curX) + "," + str(curY)), defaultfont, 15, WHITE, 10, 10, 180, 24, True)
                pygame.display.update ()
                clock.tick(FPS) # Limit the Loop
            if host == True:
                # Check Joystick Inputs and Init as required
                if onejoystick == True and twojoystick == True and threejoystick == True and fourjoystick == True:
                    pass
                else:
                    joystick_count = pygame.joystick.get_count()
                    if joystick_count == 1:
                        if onejoystick == True:
                            pass
                        else:
                            # Use joystick #0 and initialize it
                            joy1 = pygame.joystick.Joystick(0)
                            joy1.init()
                            onejoystick = True
                for event in pygame.event.get(): # User did something
                    if event.type == pygame.QUIT: # If user clicked close
                        gameLoop = False
                        playerselection = False # Flag that we are done so we exit this loop
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            playerselection = False
                            clienthostselect = True
                            roomselection = True
                            menudrawOverride = True
                            musiccheck = True
                            host = False
                        if event.key == pygame.K_SPACE:
                            if multiplayerselect[0][1] == False:
                                host_actor = Actor.Actor( screen_width/8.0,screen_height/2.4285714285714284, screen_width, screen_height, SHIPS[multiplayerselect[0][0]], PLAYERWEAPONS, 100, 1, 'Host' )
                                players.add(host_actor)
                                host_actor.set_walls(impassable_barrier)
                                multiplayerselect[0][1] = True
                            else:
                                host_actor.kill()
                                multiplayerselect[0][1] = False
                        if event.key == pygame.K_UP:
                            if multiplayerselect[0][0] > 1:
                                multiplayerselect[0][0]-=1
                            else: multiplayerselect[0][0] = menumax
                        if event.key == pygame.K_DOWN:
                            if multiplayerselect[0][0] < menumax:
                                multiplayerselect[0][0]+=1
                            else: multiplayerselect[0][0] = 1
                    if event.type == JOYHATMOTION:
                        if multiplayerselect[0][1] != True:
                            if joy1.get_hat(0) == (0,1): #Going Up
                                if multiplayerselect[0][0] > 1:
                                    multiplayerselect[0][0]-=1
                                else:
                                    multiplayerselect[0][0]=menumax
                            if joy1.get_hat(0) == (0,-1): #Going Down
                                if multiplayerselect[0][0] < menumax:
                                    multiplayerselect[0][0]+=1
                                else:
                                    multiplayerselect[0][0]=1
                    if event.type == JOYBUTTONDOWN:
                        if joy1.get_button(6):
                            playerselection = False
                            clienthostselect = True
                            roomselection = True
                            menudrawOverride = True
                            musiccheck = True
                            host = False
                        if joy1.get_button(7):
                            if multiplayerselect[0][1] == False:
                                host_actor = Actor.Actor( screen_width/8.0,screen_height/2.4285714285714284, screen_width, screen_height, SHIPS[multiplayerselect[0][0]], PLAYERWEAPONS, 100, 1, 'Host' )
                                players.add(host_actor)
                                host_actor.set_walls(impassable_barrier)
                                multiplayerselect[0][1] = True
                            else:
                                host_actor.kill()
                                multiplayerselect[0][1] = False
                    #------------- Start Code ---------------#
                try:
                    hostdata = pickle.dumps(multiplayerselect[0],True)
                    clientsock.send(hostdata)
                    clientdata = clientsock.recv(1024)
                    multiplayerselect[1] = pickle.loads(clientdata)
                except:
                    playerselection = False
                    clienthostselect = True
                    roomselection = False
                    startMenu = True
                    menudrawOverride = True
                    musiccheck = True
                    host = False

                screen.blit (playerselectionScreen, (0,0))

                    #--Client Show--#
                drawtxt('Client', defaultfont, int(combscreen/102.5), WHITE, screen_width/1.935483870967742, screen_height/3.4, 0, 0, False)
                pygame.draw.rect(screen, BLACK, (screen_width/1.6326530612244898, screen_height/3.8636363636363638, screen_width/19.35483870967742, screen_height/12.142857142857142))
                screen.blit(LOADEDSHIPS[multiplayerselect[1][0]], (screen_width/1.610738255033557, screen_height/3.794642857142857))
                if multiplayerselect[1][1] == True:
                    drawtxt('READY!', defaultfont, int(combscreen/102.5), RED, screen_width/1.4285714285714286, screen_height/3.4, 0, 0, False)
                else:
                    drawtxt('Not Ready', defaultfont, int(combscreen/102.5), WHITE, screen_width/1.4285714285714286, screen_height/3.4, 0, 0, False)
                    #--Host Show--#
                drawtxt('Host', defaultfont, int(combscreen/102.5), WHITE, screen_width/1.935483870967742, screen_height/2.125, 0, 0, False)
                pygame.draw.rect(screen, BLACK, (screen_width/1.6326530612244898, screen_height/2.2972972972972974,screen_width/19.35483870967742, screen_height/12.142857142857142))
                screen.blit(LOADEDSHIPS[multiplayerselect[0][0]], (screen_width/1.610738255033557, screen_height/2.272727272727273))
                if multiplayerselect[0][1] == True:
                    drawtxt('READY!', defaultfont, int(combscreen/102.5), RED, screen_width/1.4285714285714286, screen_height/2.125, 0, 0, False)
                else:
                    drawtxt('Not Ready', defaultfont, int(combscreen/102.5), WHITE, screen_width/1.4285714285714286, screen_height/2.125, 0, 0, False)

                if multiplayerselect[0][1] == True and multiplayerselect[1][1] == True:
                    client_actor = Actor.Actor( screen_width/8.0,screen_height/2.4285714285714284, screen_width, screen_height, SHIPS[multiplayerselect[1][0]], PLAYERWEAPONS, 100, 1, 'Client' )
                    players.add(client_actor)
                    client_actor.set_walls(impassable_barrier)

                    playerselection = False
                    musiccheck = True
                    multiplayermode = True

                if debugmode == True:
                    curX, curY = pygame.mouse.get_pos()
                    drawtxt(("Mouse Pos: " + str(curX) + "," + str(curY)), defaultfont, 15, WHITE, 10, 10, 180, 24, True)
                pygame.display.update ()
                clock.tick(FPS) # Limit the Loop
    if gameLoop != True:
        break
    # ----------------------------------------------------------------------------------------------------------------------------------------------------------- #

    def GAME_LOOP():
        """ This is used to quickly jump to the Game Loop from the Code Explorer """
        pass

    if game == True or multiplayermode == True:
        loadstat = 0
        drawtxt('Loading...'+ str(loadstat)+'%', gamefont, int(combscreen/51.25), WHITE, screen_width/1.4285714285714286, screen_height/5.12, screen_width/1.0108588351431391, 50, True)
        pygame.display.update()
        if gameload == False:
            gameScreen = pygame.image.load(os.path.join('Resources', 'Backgrounds', 'Game.png')).convert()
            backup_GameScreen = gameScreen
            gameScreen = pygame.transform.scale(backup_GameScreen,(screen_width, screen_height))
            gameload = True
        loadstat = 50
        drawtxt('Loading...'+ str(loadstat)+'%', gamefont, int(combscreen/51.25), WHITE, screen_width/1.4285714285714286, screen_height/5.12, screen_width/1.0108588351431391, 50, True)

        if gameoverdeathload == False:
            gameoverDeathScreen = pygame.image.load(os.path.join('Resources', 'Backgrounds', 'Gameover_Death.png')).convert()
            backup_GameOverDeathScreen = gameoverDeathScreen
            gameoverDeathScreen = pygame.transform.scale(backup_GameOverDeathScreen,(screen_width, screen_height))
            gameoverdeathload = True

        loadstat = 100
        drawtxt('Loading...'+ str(loadstat)+'%', gamefont, int(combscreen/51.25), WHITE, screen_width/1.4285714285714286, screen_height/5.12, screen_width/1.0108588351431391, 50, True)

    while game == True:
        pygame.display.set_caption('Battle of Tyril     |     FPS: ' + str(clock.get_fps())) # Set the title of the window

        if musiccheck == True:
            if nyancatmode == True:
                pygame.mixer.music.load(os.path.join('Resources', 'Bonus Modes', 'Nyan', 'Nyan.mp3'))
                pygame.mixer.music.play(-1)
            elif nyandogmode == True:
                pygame.mixer.music.load(os.path.join('Resources', 'Bonus Modes', 'Nyan', 'Woof.mp3'))
                pygame.mixer.music.play(-1)
            elif trololmode == True:
                pygame.mixer.music.load(os.path.join('Resources', 'Bonus Modes', 'Troll', 'Troll.mp3'))
                pygame.mixer.music.play(-1)
            else:
                pygame.mixer.music.load(gameMusic)
                pygame.mixer.music.play(-1)
            musiccheck = False

        if len(players) == 0:
            ### If there are no Players, we will End the loop, and start up the Gameover Loop
            gameoverreason = 'Death'
            playdeathctr += 1
            gameover = True
            musiccheck = True
            game = False
        if minutes == maxmin and seconds == maxsec:
            gameoverreason = 'Time Up'
            gameover = True
            musiccheck = True
            game = False
            unlockAchivement(ACHIVEMENTS, 'You Actually Won!?!')

            #------------- Start Code ---------------#
        screen.blit (gameScreen, (0,0))

        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # If user clicked close
                gameLoop = False
                game = False # Flag that we are done so we exit this loop
            if event.type == pygame.KEYDOWN:
                #-- Unlocker Check --#
                if ACHIVEMENTS [5][3] != True or ACHIVEMENTS [6][3] != True:
                    if event.key == pygame.K_UP:
                        pastseconds = seconds
                        keycodelist.append('Up')
                    if event.key == pygame.K_DOWN:
                        pastseconds = seconds
                        keycodelist.append('Down')
                    if event.key == pygame.K_LEFT:
                        pastseconds = seconds
                        keycodelist.append('Left')
                    if event.key == pygame.K_RIGHT:
                        pastseconds = seconds
                        keycodelist.append('Right')
                    if event.key == pygame.K_b:
                        pastseconds = seconds
                        keycodelist.append('B')
                    if event.key == pygame.K_RETURN:
                        pastseconds = seconds
                        keycodelist.append('Enter')
                        if keycodelist == UNLOCKABLES[0]:
                            if ACHIVEMENTS [5][3] != True:
                                if pastseconds == seconds+4: keycodelist = []
                                else:
                                    unlockAchivement(ACHIVEMENTS, 'Nyanyanyanayn')
                                    nyancatmode = unlockAwards('NyanCatMode')
                                    for i in AIlist:
                                        i.kill()
                                    keycodelist = []
                        elif keycodelist == UNLOCKABLES[1]:
                            if ACHIVEMENTS [6][3] != True:
                                if pastseconds == seconds+4: keycodelist = []
                                else:
                                    unlockAchivement(ACHIVEMENTS, 'Woofoofoofoof')
                                    nyandogmode = unlockAwards('NyanDogMode')
                                    for i in AIlist:
                                        i.kill()
                                    keycodelist = []
                        elif keycodelist == UNLOCKABLES[2]:
                            if ACHIVEMENTS [7][3] != True:
                                if pastseconds == seconds+4: keycodelist = []
                                else:
                                    unlockAchivement(ACHIVEMENTS, 'Trolololol')
                                    trololmode = unlockAwards('Troll Mode')
                                    increase = 10
                        else: keycodelist = []
                    if pastseconds == seconds+2: keycodelist = []
                    #---------- Poll keys to see if they have been pressed -------------#
                if event.key == pygame.K_a:
                    player1.keyboardMovement(-charspeed,0, 180)
                if event.key == pygame.K_d:
                    player1.keyboardMovement(charspeed,0, 0)
                if event.key == pygame.K_w:
                    player1.keyboardMovement(0,-charspeed, 90)
                if event.key == pygame.K_s:
                    player1.keyboardMovement(0,charspeed, -90)
                if event.key == pygame.K_ESCAPE: #If User Pressed the Start Button Button
                    pause = True #Pause the Game
                    musiccheck = True
                    while pause == True:
                        if musiccheck == True:
                            pygame.mixer.music.load(pauseMusic)
                            pygame.mixer.music.play(-1)
                            musiccheck = False
                        drawtxt("A PLAYER HAS PAUSED THE GAME", defaultfont, int(combscreen/51.25), WHITE, screen_width/4.363636363636363,screen_height/2, 250, 50, False)
                        pygame.display.update()
                        for event in pygame.event.get(): # User did something
                            if event.type == pygame.QUIT: # If user clicked close
                                gameLoop = False
                                game = False
                                pause = False # Flag that we are done so we exit this loop
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_BACKSPACE: #If User Pressed the Back Button
                                    resetGame()
                                if event.key == pygame.K_ESCAPE: #If User Pressed the Start Button Button
                                    pause = False #Unpause the Game
                                    musiccheck = True


                    #-------------- Reset everything back to zero to stop movement
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    player1.keyboardMovement(charspeed, 0, -999)
                if event.key == pygame.K_d:
                    player1.keyboardMovement(-charspeed,0, -999)
                if event.key == pygame.K_w:
                    player1.keyboardMovement(0,charspeed, -999)
                if event.key == pygame.K_s:
                    player1.keyboardMovement(0,-charspeed, -999)


            if event.type == pygame.JOYBUTTONDOWN:
                if onejoystick == True:
                    if joy1.get_button(7): #If User Pressed the Start Button Button
                        pause = True #Pause the Game
                        musiccheck = True
                        while pause == True:
                            if musiccheck == True:
                                pygame.mixer.music.load(pauseMusic)
                                pygame.mixer.music.play(-1)
                                musiccheck = False
                            drawtxt("PLAYER 1 HAS PAUSED THE GAME", defaultfont, int(combscreen/51.25), WHITE, screen_width/4.363636363636363,screen_height/2, 250, 50, False)
                            pygame.display.update()
                            for event in pygame.event.get(): # User did something
                                if event.type == pygame.QUIT: # If user clicked close
                                    gameLoop = False
                                    game = False
                                    pause = False # Flag that we are done so we exit this loop
                                if event.type == pygame.JOYBUTTONDOWN:
                                    if joy1.get_button(6): #If User Pressed the Back Button
                                        resetGame()
                                    if joy1.get_button(7): #If User Pressed the Start Button Button
                                        pause = False #Unpause the Game
                                        musiccheck = True
                if twojoystick == True:
                    if joy2.get_button(7): #If User Pressed the Start Button Button
                        pause = True #Pause the Game
                        musiccheck = True
                        while pause == True:
                            if musiccheck == True:
                                pygame.mixer.music.load(pauseMusic)
                                pygame.mixer.music.play(-1)
                                musiccheck = False
                            drawtxt("PLAYER 2 HAS PAUSED THE GAME", defaultfont, int(combscreen/51.25), WHITE, screen_width/4.363636363636363,screen_height/2, 250, 50, False)
                            pygame.display.update()
                            for event in pygame.event.get(): # User did something
                                if event.type == pygame.QUIT: # If user clicked close
                                    gameLoop = False
                                    game = False
                                    pause = False # Flag that we are done so we exit this loop
                                if event.type == pygame.JOYBUTTONDOWN:
                                    if joy2.get_button(6): #If User Pressed the Back Button
                                        resetGame()
                                    if joy2.get_button(7): #If User Pressed the Start Button Button
                                        pause = False #Unpause the Game
                                        musiccheck = True
                if threejoystick == True:
                    if joy3.get_button(7): #If User Pressed the Start Button Button
                        pause = True #Pause the Game
                        musiccheck = True
                        while pause == True:
                            if musiccheck == True:
                                pygame.mixer.music.load(pauseMusic)
                                pygame.mixer.music.play(-1)
                                musiccheck = False
                            drawtxt("PLAYER 3 HAS PAUSED THE GAME", defaultfont, int(combscreen/51.25), WHITE, screen_width/4.363636363636363,screen_height/2, 250, 50, False)
                            pygame.display.update()
                            for event in pygame.event.get(): # User did something
                                if event.type == pygame.QUIT: # If user clicked close
                                    gameLoop = False
                                    game = False
                                    pause = False # Flag that we are done so we exit this loop
                                if event.type == pygame.JOYBUTTONDOWN:
                                    if joy3.get_button(6): #If User Pressed the Back Button
                                        resetGame()
                                    if joy3.get_button(7): #If User Pressed the Start Button Button
                                        pause = False #Unpause the Game
                                        musiccheck = True
                if fourjoystick == True:
                    if joy4.get_button(7): #If User Pressed the Start Button Button
                        pause = True #Pause the Game
                        musiccheck = True
                        while pause == True:
                            if musiccheck == True:
                                pygame.mixer.music.load(pauseMusic)
                                pygame.mixer.music.play(-1)
                                musiccheck = False
                            drawtxt("PLAYER 4 HAS PAUSED THE GAME", defaultfont, int(combscreen/51.25), WHITE, screen_width/4.363636363636363,screen_height/2, 250, 50, False)
                            pygame.display.update()
                            for event in pygame.event.get(): # User did something
                                if event.type == pygame.QUIT: # If user clicked close
                                    gameLoop = False
                                    game = False
                                    pause = False # Flag that we are done so we exit this loop
                                if event.type == pygame.JOYBUTTONDOWN:
                                    if joy4.get_button(6): #If User Pressed the Back Button
                                        resetGame()
                                    if joy4.get_button(7): #If User Pressed the Start Button Button
                                        pause = False #Unpause the Game
                                        musiccheck = True
                    #--- Time for the Custom Events ---#
            if event.type == TIMECOUNTER:
                seconds, minutes = time(seconds,minutes)
                aiseconds -=1
                if aiseconds <= 0:
                    aiIncrease, aiDecIncrease = spawnAI(aiIncrease, aiDecIncrease)
                    aiseconds = wavetime

        #------------ Achivement Tracking ------------#
        if aideaths == 50:
            unlockAchivement(ACHIVEMENTS, 'Star Shooter')
        if playdeathctr == 25:
            unlockAcivement(ACHIVEMENTS, 'Martrydom')
     # ------------------------------------------------ #
                #-- Final Calls --#
        bulletlist_Player,bulletlist_AI,aideaths = gameUpdate(p1joined,p2joined,p3joined,p4joined,bulletlist_Player,bulletlist_AI, aideaths)
        if debugmode == True:
            curX, curY = pygame.mouse.get_pos()
            drawtxt(("Mouse Pos: " + str(curX) + "," + str(curY)), defaultfont, 15, WHITE, 10, 150, 180, 24, True)
        pygame.display.update()
        clock.tick(FPS) # Limit the Loop


    # ----------------------------------------------------------------------------------------------------------------------------------------------------------- #

    def MULTIPLAYER_LOOP():
        """ This is used to quickly jump to the Multiplayer Loop from the Code Explorer """
        pass

    if multiplayermode == True:
        while multiwaittostart == False:
            pygame.display.set_caption('Battle of Tyril     |     FPS: ' + str(clock.get_fps())) # Set the title of the window
            if client == True:
                try:
                    multiwaittostart = True
                    clientdata = pickle.dumps(multiwaittostart,True)
                    tcpCliSock.send(clientdata)
                except: pass
            if host == True:
                try:
                    clientdata = clientsock.recv(1024)
                    multiwaittostart = pickle.loads(clientdata)
                    pygame.time.set_timer(TIMECOUNTER, 1000) # After 1 Second
                except: pass
            clock.tick(FPS) # Limit the Loop

    while multiplayermode == True:
        while client == True:
            pygame.display.set_caption('Battle of Tyril     |     FPS: ' + str(clock.get_fps())) # Set the title of the window
            if musiccheck == True:
                pygame.mixer.music.load(gameMusic)
                pygame.mixer.music.play(-1)
                musiccheck = False

##            if len(players) == 0:
##                ### If there are no Players, we will End the loop, and start up the Gameover Loop
##                gameoverreason = 'Death'
##                playdeathctr += 1
##                gameover = True
##                musiccheck = True
##                game = False
##            if minutes == maxmin and seconds == maxsec:
##                gameoverreason = 'Time Up'
##                gameover = True
##                musiccheck = True
##                game = False

                #------------- Start Code ---------------#

            screen.blit (gameScreen, (0,0))
            for event in pygame.event.get(): # User did something
                if event.type == pygame.QUIT: # If user clicked close
                    gameLoop = False
                    multiplayermode = False # Flag that we are done so we exit this loop
                    client = False
                    break
                if event.type == pygame.KEYDOWN:
                        #---------- Poll keys to see if they have been pressed -------------#
                    if event.key == pygame.K_a:
                        client_actor.keyboardMovement(-charspeed,0, 180)
                    if event.key == pygame.K_d:
                        client_actor.keyboardMovement(charspeed,0, 0)
                    if event.key == pygame.K_w:
                        client_actor.keyboardMovement(0,-charspeed, 90)
                    if event.key == pygame.K_s:
                        client_actor.keyboardMovement(0,charspeed, -90)
                        #-------------- Reset everything back to zero to stop movement
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        client_actor.keyboardMovement(charspeed, 0, -999)
                    if event.key == pygame.K_d:
                        client_actor.keyboardMovement(-charspeed,0, -999)
                    if event.key == pygame.K_w:
                        client_actor.keyboardMovement(0,charspeed, -999)
                    if event.key == pygame.K_s:
                        client_actor.keyboardMovement(0,-charspeed, -999)
                host_actor = sendPackets('Client')
                bulletlist_Player,bulletlist_AI = gameUpdate(p1joined,p2joined,p3joined,p4joined,bulletlist_Player,bulletlist_AI, aideaths, True)

                if debugmode == True:
                    curX, curY = pygame.mouse.get_pos()
                    drawtxt(("Mouse Pos: " + str(curX) + "," + str(curY)), defaultfont, 15, WHITE, 10, 150, 180, 24, True)
                pygame.display.update()
##                clock.tick(FPS) # Limit the Loop
        while host == True:
            pygame.display.set_caption('Battle of Tyril     |     FPS: ' + str(clock.get_fps())) # Set the title of the window
            if musiccheck == True:
                pygame.mixer.music.load(gameMusic)
                pygame.mixer.music.play(-1)
                musiccheck = False

##            if len(players) == 0:
##                ### If there are no Players, we will End the loop, and start up the Gameover Loop
##                gameoverreason = 'Death'
##                playdeathctr += 1
##                gameover = True
##                musiccheck = True
##                game = False
##            if minutes == maxmin and seconds == maxsec:
##                gameoverreason = 'Time Up'
##                gameover = True
##                musiccheck = True
##                game = False

                #------------- Start Code ---------------#
            screen.blit (gameScreen, (0,0))
            for event in pygame.event.get(): # User did something
                if event.type == pygame.QUIT: # If user clicked close
                    gameLoop = False
                    multiplayermode = False # Flag that we are done so we exit this loop
                    host = False
                    break
                if event.type == pygame.KEYDOWN:
                        #---------- Poll keys to see if they have been pressed -------------#
                    if event.key == pygame.K_a:
                        host_actor.keyboardMovement(-charspeed,0, 180)
                    if event.key == pygame.K_d:
                        host_actor.keyboardMovement(charspeed,0, 0)
                    if event.key == pygame.K_w:
                        host_actor.keyboardMovement(0,-charspeed, 90)
                    if event.key == pygame.K_s:
                        host_actor.keyboardMovement(0,charspeed, -90)
                        #-------------- Reset everything back to zero to stop movement
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        host_actor.keyboardMovement(charspeed, 0, -999)
                    if event.key == pygame.K_d:
                        host_actor.keyboardMovement(-charspeed,0, -999)
                    if event.key == pygame.K_w:
                        host_actor.keyboardMovement(0,charspeed, -999)
                    if event.key == pygame.K_s:
                        host_actor.keyboardMovement(0,-charspeed, -999)
                client_actor = sendPackets('Host')
                bulletlist_Player,bulletlist_AI = gameUpdate(p1joined,p2joined,p3joined,p4joined,bulletlist_Player,bulletlist_AI, aideaths, True)

                if debugmode == True:
                    curX, curY = pygame.mouse.get_pos()
                    drawtxt(("Mouse Pos: " + str(curX) + "," + str(curY)), defaultfont, 15, WHITE, 10, 150, 180, 24, True)
                pygame.display.update()
##                clock.tick(FPS) # Limit the Loop

    # ----------------------------------------------------------------------------------------------------------------------------------------------------------- #

    def GAMEOVER_LOOP():
        """ This is used to quickly jump to the GameOver Loop from the Code Explorer """
        pass

    while gameover == True:
        pygame.display.set_caption('Battle of Tyril     |     FPS: ' + str(clock.get_fps())) # Set the title of the window

##        pygame.time.set_timer(TIMECOUNTER, 0) #Turn off Timer
        if gameoverreason == 'Death':
            if musiccheck == True:
                pygame.mixer.music.load(gameoverDeathMusic)
                pygame.mixer.music.play(-1)
                musiccheck = False
            #------------- Start Code ---------------#
            screen.blit (gameoverDeathScreen, (0,0))

            if gameovereventtimer >= 45:
                for event in pygame.event.get(): # User did something
                    if event.type == pygame.QUIT: # If user clicked close
                        gameLoop = False
                        gameover = False # Flag that we are done so we exit this loop
                    if event.type == pygame.KEYDOWN:
                        resetGame()
                    if event.type == pygame.JOYBUTTONDOWN:
                        resetGame()
                    if event.type == MOUSEBUTTONDOWN:
                        resetGame()
            else:
                gameovereventtimer +=1



            drawtxt('GAME OVER', gamefont, int(combscreen/51.25), WHITE, screen_width/8.0,screen_height/3.4, 250, 50, False)
            if gameoverctr <= -1: gameoveraddi,gameoversubt = True, False
            elif gameoverctr >= 1: gameoversubt, gameoveraddi = True, False
            if gameoveraddi == True:
                if gameoverpausectr >= 100:
                    gameoverctr += 1
                    gameoverpausectr = 0
                else: gameoverpausectr += 1
                drawtxt('Press To Continue', gamefont, int(combscreen/51.25)+gameoverctr, WHITE, screen_width/24.0,screen_height/1.4166666666666667, 250, 50, False)
            elif gameoversubt == True:
                if gameoverpausectr >= 100:
                    gameoverctr -= 1
                    gameoverpausectr = 0
                else: gameoverpausectr += 1
                drawtxt('Press To Continue', gamefont, int(combscreen/51.25)+gameoverctr, WHITE, screen_width/24.0,screen_height/1.4166666666666667, 250, 50, False)


            if debugmode == True:
                curX, curY = pygame.mouse.get_pos()
                drawtxt(("Mouse Pos: " + str(curX) + "," + str(curY)), defaultfont, 15, WHITE, 10, 150, 180, 24, True)

            pygame.display.update()
            clock.tick(FPS) # Limit the Loop

        elif gameoverreason == 'Time Up':
            if gameoveraliveload == False:
                gameoverTimeUpScreen = pygame.image.load(os.path.join('Resources', 'Backgrounds', 'Gameover_Time Up.png')).convert()
                backup_GameOverTimeUpScreen = gameoverTimeUpScreen
                gameoverTimeUpScreen = pygame.transform.scale(backup_GameOverTimeUpScreen,(screen_width, screen_height))
                gameoveraliveload = True

            if musiccheck == True:
                pygame.mixer.music.load(gameoverTimeUpMusic)
                pygame.mixer.music.play(-1)
                musiccheck = False
            #------------- Start Code ---------------#
            screen.blit (gameoverTimeUpScreen, (0,0))

            for event in pygame.event.get(): # User did something
                if event.type == pygame.QUIT: # If user clicked close
                    gameLoop = False
                    gameover = False # Flag that we are done so we exit this loop
                if event.type == pygame.KEYDOWN:
                    resetGame()
                if event.type == pygame.JOYBUTTONDOWN:
                    resetGame()
                if event.type == MOUSEBUTTONDOWN:
                    resetGame()



            drawtxt('Congratulations!', gamefont, int(combscreen/51.25), WHITE, screen_width/13.333333333333334,screen_height/3.8636363636363638, 250, 50, False)
            drawtxt('You Have Saved Tyril!', gamefont, int(combscreen/51.25), WHITE, screen_width/20.0,screen_height/3.125, 250, 50, False)
            if gameoverctr <= -1: gameoveraddi,gameoversubt = True, False
            elif gameoverctr >= 1: gameoversubt, gameoveraddi = True, False
            if gameoveraddi == True:
                if gameoverpausectr >= 100:
                    gameoverctr += 1
                    gameoverpausectr = 0
                else: gameoverpausectr += 1
                drawtxt('Press To Continue', gamefont, int(combscreen/51.25)+gameoverctr, WHITE, screen_width/24.0,screen_height/1.4166666666666667, 250, 50, False)
            elif gameoversubt == True:
                if gameoverpausectr >= 100:
                    gameoverctr -= 1
                    gameoverpausectr = 0
                else: gameoverpausectr += 1
                drawtxt('Press To Continue', gamefont, int(combscreen/51.25)+gameoverctr, WHITE, screen_width/24.0,screen_height/1.4166666666666667, 250, 50, False)


            if debugmode == True:
                curX, curY = pygame.mouse.get_pos()
                drawtxt(("Mouse Pos: " + str(curX) + "," + str(curY)), defaultfont, 15, WHITE, 10, 150, 180, 24, True)

            pygame.display.update()
            clock.tick(FPS) # Limit the Loop

pygame.quit()