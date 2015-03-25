#-------------------------------------------------------------------------------
# Name:         Classes.Py
# Purpose:      ICS4U Programming FSE: Battle of Tyril
#
# Author:      Andrew Godfroy (Killer Rin)
#
# Created:     12/03/2011
# Copyright:   (c) killer rin 2011
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python
import pygame
import math
import os
from random import *

WHITE = (255,255,255)
BLACK = (0,0,0)

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

class GUI(pygame.sprite.Sprite):
    # -- Functions -- #
    def __init__(self,x,y, sw,sh, filename):
        """ X, Y, ScaleWidth, ScaleHeight, Filename"""
        pygame.sprite.Sprite.__init__(self)

        # Grab the Scale Variables
        self.scalewidth = sw
        self.scaleheight = sh

        # Import the Player Image
        self.image = pygame.image.load(filename)
        self.image = pygame.transform.scale(self.image,(int(self.scalewidth), int(self.scaleheight)))
        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.topleft = [x,y]
        self.imagemask = pygame.mask.from_surface(self.image,127)

    def move_GUI(self, x,y):
        self.rect.left += x
        self.rect.top += y

    def setimg(self, x, y, sw, sh, filename):
        # Grab the Scale Variables
        self.scalewidth = sw
        self.scaleheight = sh

        # Import the Player Image
        self.image = pygame.image.load(filename)
        self.image = pygame.transform.scale(self.image,(int(self.scalewidth), int(self.scaleheight)))
        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.topleft = [x,y]
        self.imagemask = pygame.mask.from_surface(self.image,127)

    def changeimg(self, x, y, filename):
        # Import the Player Image
        self.image = pygame.image.load(filename)
        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.topleft = [x,y]
        self.imagemask = pygame.mask.from_surface(self.image,127)

if __name__ == '__main__':
    screen_width, screen_height = 200,200
    pygame.init()
    guilist = pygame.sprite.RenderPlain()
    gui = GUI(0,0,screen_width, screen_height/5.94, os.path.join('Resources', 'GUI', 'HUD.png'))
    guilist.add(gui)
    pygame.quit()