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

class Actor(pygame.sprite.Sprite):
    debugmode = True

    shootctr = -999
    aiTargetctr = 0
        #--- Player ---#
    speed_x, speed_y = 0, 0
    joy_speed_x, joy_speed_y = 20, 20
    keyrotation = 0
    joystick_count = 0
    imagerotation = 0

        #--- AI ---#
    pathfindX, pathfindY = True, True
    targetplayer = False
    AIX, AIY = 8,8
    randMoveX, randMoveY = 0,0
    closest = 0
    target = 0

    # -- Functions -- #
    def __init__(self,x,y, sw, sh, filename, weapons, health, player, multiplayer=None):
        """ PlayerX, PlayerY, ScaleWidth, ScaleHeight, FileName, WeaponList, Player Number, *multiplayer"""
        pygame.sprite.Sprite.__init__(self)

        # Get the list for weapons
        self.weapons = weapons
        self.weaponindex = weapons [1]

        self.imagerotation = -90

        # Import the Player Image
        self.image = pygame.image.load(filename).convert()
        self.image.set_colorkey(BLACK)
        self.image = pygame.transform.scale(self.image, (int(sw/29.26829268292683),int(sh/13.492063492063492)))
        self.image = pygame.transform.rotate (self.image, self.imagerotation)
        self.oldimage = self.image

        # Make our top-left corners the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.topleft = [x,y]
        self.imagemask = pygame.mask.from_surface(self.image,127)

        # Get the scale and place it into the class variables
        self.scalewidth = sw
        self.scaleheight = sh
        self.combscreen = sw+sh

        # Self the X, Y Just in case
        self.x = x
        self.y = y

        # Store the Variable for Health
        self.health = health

        # Grab the variable for Player
        self.playerNum = player

        # Are We Multiplayer or Not?
        if multiplayer is None:
            self.multiplayer = False
        elif multiplayer == 'Client':
            self.multiplayer = 'Client'
        elif multiplayer == 'Host':
            self.multiplayer = 'Host'

        # Count the joysticks the computer has
        self.joystick_count=pygame.joystick.get_count()

        if self.multiplayer == False:
            if self.playerNum != 'AI':
                if self.joystick_count != 0:
                    self.joy_speed_x, self.joy_speed_y = int(self.combscreen/102.5), int(self.combscreen/102.5)
                    if self.playerNum == 1:
                        # Use joystick #0 and initialize it
                        self.my_joystick = pygame.joystick.Joystick(0)
                        self.my_joystick.init()
                    if self.playerNum == 2:
                        # Use joystick #1 and initialize them
                        self.p_joystick2 = pygame.joystick.Joystick(1)
                        self.p_joystick2.init()
                    if self.playerNum == 3:
                        # Use joystick #2 and initialize it
                        self.p_joystick3 = pygame.joystick.Joystick(2)
                        self.p_joystick3.init()
                    if self.playerNum == 4:
                        # Use joystick #3 and initialize it
                        self.p_joystick4 = pygame.joystick.Joystick(3)
                        self.p_joystick4.init()
                else:   # No joysticks!
                    pass
            else:
                self.AIX, self.AIY = int(self.combscreen/256.25), int(self.combscreen/256.25)
                self.AIRAD = int(self.combscreen/82.0) #25
                self.AIDIRECTIONHOMING = int(self.combscreen/17.083333333333332) #80 = 25.625 | 120 = 17.083333333333332
        elif self.multiplayer == 'Client':
            if self.joystick_count != 0:
                self.joy_speed_x, self.joy_speed_y = int(self.combscreen/102.5), int(self.combscreen/102.5)
                if self.playerNum == 1:
                    # Use joystick #0 and initialize it
                    self.client_joystick = pygame.joystick.Joystick(0)
                    self.client_joystick.init()
            else: pass
        elif self.multiplayer == 'Host':
            if self.joystick_count != 0:
                self.joy_speed_x, self.joy_speed_y = int(self.combscreen/102.5), int(self.combscreen/102.5)
                if self.playerNum == 1:
                    # Use joystick #0 and initialize it
                    self.server_joystick = pygame.joystick.Joystick(0)
                    self.server_joystick.init()
            else: pass

    def keyboardMovement(self, charspeedx,charspeedy, rotation):
        # Change the Speed of the character then move it
        """ MovementX, MovementY"""
        self.speed_x+=charspeedx
        self.speed_y+=charspeedy
        if rotation == -999:
            self.keyrotation = self.keyrotation
        else:
            self.keyrotation = rotation

    def shoot(self, playerlist, enemylist, bulletlist):
        self.curX, self.curY = pygame.mouse.get_pos()
        if self.shootctr == self.weaponindex[3] or self.shootctr == -999:
            self.shootctr = 0
            self.playerlist = playerlist
            self.enemylist = enemylist
            self.bulletlist_Player = bulletlist[0]
            self.bulletlist_AI = bulletlist[1]

            bullinitX =  self.rect.left + (self.rect.width/2)
            bullinitY = self.rect.top +(self.rect.height/2)

                    ### True == Player, False == AI
            if self.playerNum != 'AI': plAI = True
            else: plAI = False

            if plAI == True:
                if self.joystick_count != 0:
                    if self.playerNum == 1:
                        if self.multiplayer == False:
                            # This gets the position of the axis on the game controller
                            # It returns a number between -1.0 and +1.0
                            x_axis= self.my_joystick.get_axis(3) #x_axis is the position of the horizontal joystick
                            y_axis= self.my_joystick.get_axis(4) #y_axis is the position of the vertical joystick

                            if x_axis >= .2 or x_axis <= -.2 or y_axis >= .2 or y_axis <= -.2:
                                # Find the direction of the stick to use as our passed on Direction
                                shot = Bullet(bullinitX, bullinitY, [x_axis,y_axis],\
                                 [self.scalewidth, self.scaleheight], self.weaponindex, self.walls, plAI)
                                self.bulletlist_Player.add(shot)

                        elif self.multiplayer == 'Client':
                            # This gets the position of the axis on the game controller
                            # It returns a number between -1.0 and +1.0
                            x_axis= self.client_joystick.get_axis(3) #x_axis is the position of the horizontal joystick
                            y_axis= self.client_joystick.get_axis(4) #y_axis is the position of the vertical joystick

                            if x_axis >= .2 or x_axis <= -.2 or y_axis >= .2 or y_axis <= -.2:
                                # Find the direction of the stick to use as our passed on Direction
                                shot = Bullet(bullinitX, bullinitY, [x_axis,y_axis],\
                                 [self.scalewidth, self.scaleheight], self.weaponindex, self.walls, plAI)
                                self.bulletlist_Player.add(shot)

                        elif self.multiplayer == 'Host':
                            # This gets the position of the axis on the game controller
                            # It returns a number between -1.0 and +1.0
                            x_axis= self.server_joystick.get_axis(3) #x_axis is the position of the horizontal joystick
                            y_axis= self.server_joystick.get_axis(4) #y_axis is the position of the vertical joystick

                            if x_axis >= .2 or x_axis <= -.2 or y_axis >= .2 or y_axis <= -.2:
                                # Find the direction of the stick to use as our passed on Direction
                                shot = Bullet(bullinitX, bullinitY, [x_axis,y_axis],\
                                 [self.scalewidth, self.scaleheight], self.weaponindex, self.walls, plAI)
                                self.bulletlist_Player.add(shot)

                    if self.playerNum == 2:
                        # This gets the position of the axis on the game controller
                        # It returns a number between -1.0 and +1.0
                        x_axis= self.p_joystick2.get_axis(3) #x_axis is the position of the horizontal joystick
                        y_axis= self.p_joystick2.get_axis(4) #y_axis is the position of the vertical joystick

                        if x_axis >= .2 or x_axis <= -.2 or y_axis >= .2 or y_axis <= -.2:
                            # Find the direction of the stick to use as our passed on Direction
                            shot = Bullet(bullinitX, bullinitY, [x_axis,y_axis],\
                             [self.scalewidth, self.scaleheight], self.weaponindex, self.walls, plAI)
                            self.bulletlist_Player.add(shot)

                    if self.playerNum == 3:
                        # This gets the position of the axis on the game controller
                        # It returns a number between -1.0 and +1.0
                        x_axis= self.p_joystick3.get_axis(3) #x_axis is the position of the horizontal joystick
                        y_axis= self.p_joystick3.get_axis(4) #y_axis is the position of the vertical joystick

                        if x_axis >= .2 or x_axis <= -.2 or y_axis >= .2 or y_axis <= -.2:
                            # Find the direction of the stick to use as our passed on Direction
                            shot = Bullet(bullinitX, bullinitY, [x_axis,y_axis],\
                             [self.scalewidth, self.scaleheight], self.weaponindex, self.walls, plAI)
                            self.bulletlist_Player.add(shot)

                    if self.playerNum == 4:
                        # This gets the position of the axis on the game controller
                        # It returns a number between -1.0 and +1.0
                        x_axis= self.p_joystick4.get_axis(3) #x_axis is the position of the horizontal joystick
                        y_axis= self.p_joystick4.get_axis(4) #y_axis is the position of the vertical joystick

                        if x_axis >= .2 or x_axis <= -.2 or y_axis >= .2 or y_axis <= -.2:
                            # Find the direction of the stick to use as our passed on Direction
                            shot = Bullet(bullinitX, bullinitY, [x_axis,y_axis],\
                             [self.scalewidth, self.scaleheight], self.weaponindex, self.walls, plAI)
                            self.bulletlist_Player.add(shot)
                else: #Keyboard
                    shot = Bullet(bullinitX, bullinitY, [self.curX, self.curY],\
                     [self.scalewidth, self.scaleheight], self.weaponindex, self.walls, plAI)
                    self.bulletlist_Player.add(shot)

            else:
                shootcheck = randint (0,20)
                if shootcheck == 3 or shootcheck == 7:
                    if len(self.playerlist) == 0:
                        pass
                    else:
                        self.target = randint (0, (len(self.playerlist)-1))
                        for i in self.playerlist:
                            if self.aiTargetctr == self.target:
                                playLocX = i.get_location()[0]
                                playLocY = i.get_location()[1]
                                self.aiTargetctr = 0
                                break
                            self.aiTargetctr +=1

                        shot = Bullet(bullinitX, bullinitY, [playLocX, playLocY],\
                         [self.scalewidth, self.scaleheight], self.weaponindex, self.walls, plAI)
                        self.bulletlist_AI.add(shot)


        else: self.shootctr +=1
        return self.bulletlist_Player, self.bulletlist_AI

    def update(self,playerlist, enemylist, bulletlist, aidead, multiplayercheck = None): # Find, and Update the Actor
        self.bulletlist_Player = bulletlist[0]
        self.bulletlist_AI = bulletlist[1]

        playercollide = pygame.sprite.spritecollide(self, playerlist, False)
        enemycollide = pygame.sprite.spritecollide(self, enemylist, False)

        playerBulletCollide = pygame.sprite.spritecollide(self, self.bulletlist_Player, False)
        aiBulletCollide = pygame.sprite.spritecollide(self, self.bulletlist_AI, False)

        if multiplayercheck is None:
            self.multiplayercheck = False
        elif multiplayercheck == 'Client':
            self.multiplayercheck = 'Client'
        elif multiplayercheck == 'Host':
            self.multiplayercheck = 'Host'

        ctr = 0

        """ Walls """
        if self.playerNum != 'AI': # Check to see if the Actor is an AI or not.
            if self.joystick_count != 0: #  If the Actor isn't an AI, then it will update acording to the Player Input
                if self.playerNum == 1:
                    if self.multiplayercheck == False:
                         # This gets the position of the axis on the game controller
                        x_axis= self.my_joystick.get_axis(0) #x_axis is the position of the horizontal joystick
                        y_axis= self.my_joystick.get_axis(1) #y_axis is the position of the vertical joystick
                            # It returns a number between -1.0 and +1.0

                        if x_axis >= .2 or x_axis <= -.2 or y_axis >= .2 or y_axis <= -.2:
                            # Get the old position, in case we need to go back to it
                            old_x=self.rect.left
                            new_x=old_x+x_axis*self.joy_speed_x
                            self.rect.left = new_x

                            # Check to see if the player is in a wall
                            wallcollide = pygame.sprite.spritecollide(self, self.walls, False)
                            if wallcollide:
                                self.rect.left=old_x # If it hits a wall, we go back to before/wont update it.

                            old_y=self.rect.top
                            new_y=old_y+y_axis*self.joy_speed_y
                            self.rect.top = new_y

                            # Check to see if the player is in a wall
                            wallcollide = pygame.sprite.spritecollide(self, self.walls, False)
                            if wallcollide: # If it hits a wall, we go back to before/wont update it.
                                self.rect.top=old_y

                        # Get the Rotations and rotate the image to the direction that the Left Thumbstick is pointing
                        angle_radians = math.atan2(y_axis,x_axis)
                        angle_degrees = math.degrees(math.atan2(y_axis,x_axis))

                        self.image = pygame.transform.rotate (self.oldimage, -angle_degrees)
                        self.imagemask = pygame.mask.from_surface(self.image,127)

                            # --- Collisions --- #
                        if enemycollide:
                            for i in enemylist:
                                if pygame.sprite.collide_mask(self, i):
                                    self.health -= 25
                        if aiBulletCollide:
                            for i in self.bulletlist_AI:
                                if pygame.sprite.collide_mask(self, i):
                                    self.health -= self.weaponindex[2]
                        if self.health <= 0:
                            pygame.sprite.Sprite.kill(self)
                    elif self.multiplayercheck == 'Client':
                         # This gets the position of the axis on the game controller
                        x_axis= self.client_joystick.get_axis(0) #x_axis is the position of the horizontal joystick
                        y_axis= self.client_joystick.get_axis(1) #y_axis is the position of the vertical joystick
                            # It returns a number between -1.0 and +1.0

                        if x_axis >= .2 or x_axis <= -.2 or y_axis >= .2 or y_axis <= -.2:
                            # Get the old position, in case we need to go back to it
                            old_x=self.rect.left
                            new_x=old_x+x_axis*self.joy_speed_x
                            self.rect.left = new_x

                            # Check to see if the player is in a wall
                            wallcollide = pygame.sprite.spritecollide(self, self.walls, False)
                            if wallcollide:
                                self.rect.left=old_x # If it hits a wall, we go back to before/wont update it.

                            old_y=self.rect.top
                            new_y=old_y+y_axis*self.joy_speed_y
                            self.rect.top = new_y

                            # Check to see if the player is in a wall
                            wallcollide = pygame.sprite.spritecollide(self, self.walls, False)
                            if wallcollide: # If it hits a wall, we go back to before/wont update it.
                                self.rect.top=old_y

                        # Get the Rotations and rotate the image to the direction that the Left Thumbstick is pointing
                        angle_radians = math.atan2(y_axis,x_axis)
                        angle_degrees = math.degrees(math.atan2(y_axis,x_axis))
                        self.imagerotation = angle_degrees

                        self.image = pygame.transform.rotate (self.oldimage, -angle_degrees)
                        self.imagemask = pygame.mask.from_surface(self.image,127)

                            # --- Collisions --- #
                        if enemycollide:
                            for i in enemylist:
                                if pygame.sprite.collide_mask(self, i):
                                    self.health -= 25
                        if aiBulletCollide:
                            for i in self.bulletlist_AI:
                                if pygame.sprite.collide_mask(self, i):
                                    self.health -= self.weaponindex[2]
                        if self.health <= 0:
                            pygame.sprite.Sprite.kill(self)
                    elif self.multiplayercheck == 'Host':
                         # This gets the position of the axis on the game controller
                        x_axis= self.server_joystick.get_axis(0) #x_axis is the position of the horizontal joystick
                        y_axis= self.server_joystick.get_axis(1) #y_axis is the position of the vertical joystick
                            # It returns a number between -1.0 and +1.0

                        if x_axis >= .2 or x_axis <= -.2 or y_axis >= .2 or y_axis <= -.2:
                            # Get the old position, in case we need to go back to it
                            old_x=self.rect.left
                            new_x=old_x+x_axis*self.joy_speed_x
                            self.rect.left = new_x

                            # Check to see if the player is in a wall
                            wallcollide = pygame.sprite.spritecollide(self, self.walls, False)
                            if wallcollide:
                                self.rect.left=old_x # If it hits a wall, we go back to before/wont update it.

                            old_y=self.rect.top
                            new_y=old_y+y_axis*self.joy_speed_y
                            self.rect.top = new_y

                            # Check to see if the player is in a wall
                            wallcollide = pygame.sprite.spritecollide(self, self.walls, False)
                            if wallcollide: # If it hits a wall, we go back to before/wont update it.
                                self.rect.top=old_y

                        # Get the Rotations and rotate the image to the direction that the Left Thumbstick is pointing
                        angle_radians = math.atan2(y_axis,x_axis)
                        angle_degrees = math.degrees(math.atan2(y_axis,x_axis))
                        self.imagerotation = angle_degrees

                        self.image = pygame.transform.rotate (self.oldimage, -angle_degrees)
                        self.imagemask = pygame.mask.from_surface(self.image,127)

                            # --- Collisions --- #
                        if enemycollide:
                            for i in enemylist:
                                if pygame.sprite.collide_mask(self, i):
                                    self.health -= 25
                        if aiBulletCollide:
                            for i in self.bulletlist_AI:
                                if pygame.sprite.collide_mask(self, i):
                                    self.health -= self.weaponindex[2]
                        if self.health <= 0:
                            pygame.sprite.Sprite.kill(self)

                if self.playerNum == 2:
                    p2_x_axis= self.p_joystick2.get_axis(0)
                    p2_y_axis= self.p_joystick2.get_axis(1)

                    if p2_x_axis >= .2 or p2_x_axis <= -.2 or p2_y_axis >= .2 or p2_y_axis <= -.2:
                        # Get the old position, in case we need to go back to it
                        old_x=self.rect.left
                        new_x=old_x+p2_x_axis*self.joy_speed_x
                        self.rect.left = new_x

                        # Check to see if the player is in a wall
                        wallcollide = pygame.sprite.spritecollide(self, self.walls, False)
                        if wallcollide:
                            self.rect.left=old_x # If it hits a wall, we go back to before/wont update it.

                        old_y=self.rect.top
                        new_y=old_y+p2_y_axis*self.joy_speed_y
                        self.rect.top = new_y

                        # Check to see if the player is in a wall
                        wallcollide = pygame.sprite.spritecollide(self, self.walls, False)
                        if wallcollide: # If it hits a wall, we go back to before/wont update it.
                            self.rect.top=old_y

                    # Get the Rotations and rotate the image to the direction that the Left Thumbstick is pointing
                    angle_radians = math.atan2(p2_y_axis,p2_x_axis)
                    angle_degrees = math.degrees(math.atan2(p2_y_axis,p2_x_axis))

                    self.image = pygame.transform.rotate (self.oldimage, -angle_degrees)
                    self.imagemask = pygame.mask.from_surface(self.image,127)

                        # --- Collisions --- #
                    if enemycollide:
                        for i in enemylist:
                            if pygame.sprite.collide_mask(self, i):
                                self.health -= 25
                    if aiBulletCollide:
                        for i in self.bulletlist_AI:
                            if pygame.sprite.collide_mask(self, i):
                                self.health -= self.weaponindex[2]
                    if self.health <= 0:
                        pygame.sprite.Sprite.kill(self)

                if self.playerNum == 3:
                    p3_x_axis= self.p_joystick3.get_axis(0)
                    p3_y_axis= self.p_joystick3.get_axis(1)

                    if p3_x_axis >= .2 or p3_x_axis <= -.2 or p3_y_axis >= .2 or p3_y_axis <= -.2:
                        # Get the old position, in case we need to go back to it
                        old_x=self.rect.left
                        new_x=old_x+p3_x_axis*self.joy_speed_x
                        self.rect.left = new_x

                        # Check to see if the player is in a wall
                        wallcollide = pygame.sprite.spritecollide(self, self.walls, False)
                        if wallcollide:
                            self.rect.left=old_x # If it hits a wall, we go back to before/wont update it.

                        old_y=self.rect.top
                        new_y=old_y+p3_y_axis*self.joy_speed_y
                        self.rect.top = new_y

                        # Check to see if the player is in a wall
                        wallcollide = pygame.sprite.spritecollide(self, self.walls, False)
                        if wallcollide: # If it hits a wall, we go back to before/wont update it.
                            self.rect.top=old_y

                    # Get the Rotations and rotate the image to the direction that the Left Thumbstick is pointing
                    angle_radians = math.atan2(p3_y_axis,p3_x_axis)
                    angle_degrees = math.degrees(math.atan2(p3_y_axis,p3_x_axis))

                    self.image = pygame.transform.rotate (self.oldimage, -angle_degrees)
                    self.imagemask = pygame.mask.from_surface(self.image,127)

                        # --- Collisions --- #
                    if enemycollide:
                        for i in enemylist:
                            if pygame.sprite.collide_mask(self, i):
                                self.health -= 25
                    if aiBulletCollide:
                        for i in self.bulletlist_AI:
                            if pygame.sprite.collide_mask(self, i):
                                self.health -= self.weaponindex[2]
                    if self.health <= 0:
                        pygame.sprite.Sprite.kill(self)

                if self.playerNum == 4:
                    p4_x_axis= self.p_joystick4.get_axis(0)
                    p4_y_axis= self.p_joystick4.get_axis(1)

                    if p4_x_axis >= .2 or p4_x_axis <= -.2 or p4_y_axis >= .2 or p4_y_axis <= -.2:
                        # Get the old position, in case we need to go back to it
                        old_x=self.rect.left
                        new_x=old_x+p4_x_axis*self.joy_speed_x
                        self.rect.left = new_x

                        # Check to see if the player is in a wall
                        wallcollide = pygame.sprite.spritecollide(self, self.walls, False)
                        if wallcollide:
                            self.rect.left=old_x # If it hits a wall, we go back to before/wont update it.

                        old_y=self.rect.top
                        new_y=old_y+p4_y_axis*self.joy_speed_y
                        self.rect.top = new_y

                        # Check to see if the player is in a wall
                        if wallcollide: # If it hits a wall, we go back to before/wont update it.
                            self.rect.top=old_y

                    # Get the Rotations and rotate the image to the direction that the Left Thumbstick is pointing
                    angle_radians = math.atan2(p4_y_axis,p4_x_axis)
                    angle_degrees = math.degrees(math.atan2(p4_y_axis,p4_x_axis))

                    self.image = pygame.transform.rotate (self.oldimage, -angle_degrees)
                    self.imagemask = pygame.mask.from_surface(self.image,127)

                        # --- Collisions --- #
                    if enemycollide:
                        for i in enemylist:
                            if pygame.sprite.collide_mask(self, i):
                                self.health -= 25
                    if aiBulletCollide:
                        for i in self.bulletlist_AI:
                            if pygame.sprite.collide_mask(self, i):
                                self.health -= self.weaponindex[2]
                    if self.health <= 0:
                        pygame.sprite.Sprite.kill(self)


            else:
                #Default to Keyboard Shooting
                # Get the old position, in case we need to go back to it
                old_x=self.rect.left
                new_x=old_x+self.speed_x
                self.rect.left = new_x

                # Check to see if the player is in a wall
                wallcollide = pygame.sprite.spritecollide(self, self.walls, False)
                if wallcollide:
                    self.rect.left=old_x # If it hits a wall, we go back to before/wont update it.

                old_y=self.rect.top
                new_y=old_y+self.speed_y
                self.rect.top = new_y

                # Check to see if the player is in a wall
                wallcollide = pygame.sprite.spritecollide(self, self.walls, False)
                if wallcollide: # If it hits a wall, we go back to before/wont update it.
                    self.rect.top=old_y

                # Get the Rotations and rotate the image to the direction that the Left Thumbstick is pointing
                angle_radians = math.atan2(new_y,new_x)
                angle_degrees = math.degrees(math.atan2(new_y,new_x))
                self.imagerotation = self.keyrotation

                self.image = pygame.transform.rotate (self.oldimage, self.keyrotation)
                self.imagemask = pygame.mask.from_surface(self.image,127)

                    # --- Collisions --- #
                if enemycollide:
                        for i in enemylist:
                            if pygame.sprite.collide_mask(self, i):
                                self.health -= 25
                if aiBulletCollide:
                        for i in self.bulletlist_AI:
                            if pygame.sprite.collide_mask(self, i):
                                self.health -= self.weaponindex[2]
                if self.health <= 0:
                    pygame.sprite.Sprite.kill(self)

        else:  # If the Actor is an AI, then We will Update based on AI Pathcode
            loclist = [(-999,-999,-999,-999)]
            for i in playerlist:
                loclist.append((i.get_location()[0],i.get_location()[1],i.get_location()[2],i.get_location()[3]))
            loclist.reverse()

            for i in loclist:
                xDistCheck = i[0]
                yDistCheck = i[1]
                ctr += 1
                if xDistCheck == -999 or yDistCheck == -999:
                    ctr -= 1

                if ctr == 1:
                    if xDistCheck <= self.rect.right+self.AIDIRECTIONHOMING and xDistCheck >= self.rect.left-self.AIDIRECTIONHOMING:
                        if yDistCheck <= self.rect.top+self.AIDIRECTIONHOMING and yDistCheck >= self.rect.bottom-self.AIDIRECTIONHOMING:
                            self.targetplayer = True
                            self.closest = 0
                            break
                elif ctr == 2:
                    if xDistCheck <= self.rect.right+self.AIDIRECTIONHOMING and xDistCheck >= self.rect.left-self.AIDIRECTIONHOMING:
                        if yDistCheck <= self.rect.top+self.AIDIRECTIONHOMING and yDistCheck >= self.rect.bottom-self.AIDIRECTIONHOMING:
                            self.targetplayer = True
                            self.closest = 1
                            break
                elif ctr == 3:
                    if xDistCheck <= self.rect.right+self.AIDIRECTIONHOMING and xDistCheck >= self.rect.left-self.AIDIRECTIONHOMING:
                        if yDistCheck <= self.rect.top+self.AIDIRECTIONHOMING and yDistCheck >= self.rect.bottom-self.AIDIRECTIONHOMING:
                            self.targetplayer = True
                            self.closest = 2
                            break
                elif ctr == 4:
                    if xDistCheck <= self.rect.right+self.AIDIRECTIONHOMING and xDistCheck >= self.rect.left-self.AIDIRECTIONHOMING:
                        if yDistCheck <= self.rect.top+self.AIDIRECTIONHOMING and yDistCheck >= self.rect.bottom-self.AIDIRECTIONHOMING:
                            self.targetplayer = True
                            self.closest = 3
                            break


            """ We will begin checking to see if the AI is targeting the player or not.
            If the AI is targeting the player, it will skip the randomized movement step
            and target the player. When the target leaves the AIs range, the target will
            revert back to randomized movement again"""
            if self.targetplayer != True:
                    # AI Pathfind X
                if self.pathfindX == True:
                    self.randMoveX = randint(0, int(self.scalewidth))
                    self.pathfindX = False
                elif self.pathfindX == False:
                            # -- Move AI --#
                    old_x=self.rect.left
                    if self.rect.left <= self.randMoveX:
                        new_x = old_x+self.AIX
                    elif self.rect.left >= self.randMoveX:
                        new_x = old_x-self.AIX
                    self.rect.left = new_x

                    if self.rect.left <= self.randMoveX+self.AIRAD and self.rect.left >= self.randMoveX-self.AIRAD:
                        self.pathfindX = True

                    # AI Pathfind Y
                if self.pathfindY == True:
                    self.randMoveY = randint(int(self.scaleheight/5.862068965517241), int(self.scaleheight))
                    self.pathfindY = False
                elif self.pathfindY == False:
                            # -- Move AI --#
                    old_y = self.rect.top
                    if self.rect.top <= self.randMoveY:
                        new_y = old_y+self.AIY
                    elif self.rect.top >= self.randMoveY:
                        new_y = old_y-self.AIY
                    self.rect.top = new_y

                    if self.rect.left <= self.randMoveY+self.AIRAD and self.rect.left >= self.randMoveY-self.AIRAD:
                        self.pathfindY = True


            elif self.targetplayer == True:
                        # -- Move AI --#
                old_x=self.rect.left # AI Pathfind X
                if self.rect.left <= loclist[self.closest][0]:
                    new_x = old_x+self.AIX
                elif self.rect.left >= loclist[self.closest][0]:
                    new_x = old_x-self.AIX
                self.rect.left = new_x

                old_y = self.rect.top # AI Pathfind Y
                if self.rect.top <= loclist[self.closest][1]:
                    new_y = old_y+self.AIY
                elif self.rect.top >= loclist[self.closest][1]:
                    new_y = old_y-self.AIY
                self.rect.top = new_y

                # Check to see if the player has left the range of the AI
                if xDistCheck >= self.rect.right+self.AIDIRECTIONHOMING or xDistCheck <= self.rect.left-self.AIDIRECTIONHOMING:
                    if yDistCheck >= self.rect.bottom+self.AIDIRECTIONHOMING or yDistCheck <= self.rect.top-self.AIDIRECTIONHOMING:
                        self.targetplayer = False

            if playercollide:
                for i in playerlist:
                    if pygame.sprite.collide_mask(self, i):
                        pygame.sprite.Sprite.kill(self)
                        aidead += 1
                return aidead

            elif playerBulletCollide:
                for i in self.bulletlist_Player:
                    if pygame.sprite.collide_mask(self, i):
                        pygame.sprite.Sprite.kill(self)
                        aidead += 1
                return aidead
            return aidead


    def get_image(self):
        return self.image

    def get_rotation(self):
        return self.imagerotation

    def get_weapons(self):
        return self.weaponindex

    def get_location(self):
        return self.rect

    def get_health(self):
        return self.health

    def set_health(self, health):
        self.health = health

    def set_weapons(self, indexnum):
        self.weaponindex = self.weapons[indexnum]

    def set_walls(self, walls):
        self.walls = walls

    def set_image(self, x,y,filename):
        # Import the Player Image
        self.image = pygame.image.load(filename).convert()
        self.image.set_colorkey(BLACK)
        self.image = pygame.transform.scale(self.image, (int(self.scalewidth/29.26829268292683),int(self.scaleheight/13.492063492063492)))
        self.image = pygame.transform.rotate (self.image, -90)
        self.oldimage = self.image

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.topleft = [x,y]

    def multi_set_image(self, rectimg):
        self.image = pygame.transform.rotate (self.oldimage, rectimg[1])
        self.rect = rectimg[0]

    def set_scaling(self, sw,sh):
        self.scalewidth = sw
        self.scaleheight = sh
        self.combscreen = sw+sh

        if self.playerNum != 'AI':
            if self.joystick_count != 0:
                self.joy_speed_x, self.joy_speed_y = int(self.combscreen/102.5), int(self.combscreen/102.5)
        else:
            self.AIX, self.AIY = int(self.combscreen/256.25), int(self.combscreen/256.25)
            self.AIRAD = int(self.combscreen/82.0) #25
            self.AIDIRECTIONHOMING = int(self.combscreen/17.083333333333332) #80 = 25.625 | 120 = 17.083333333333332

    def recheck_controller(self):
        # Count the joysticks the computer has
        self.joystick_count=pygame.joystick.get_count()

        if self.playerNum != 'AI':
            if self.joystick_count != 0:
                    if self.playerNum == 1:
                        # Use joystick #0 and initialize it
                        self.my_joystick = pygame.joystick.Joystick(0)
                        self.my_joystick.init()
                    if self.playerNum == 2:
                        # Use joystick #1 and initialize them
                        self.p_joystick2 = pygame.joystick.Joystick(1)
                        self.p_joystick2.init()
                    if self.playerNum == 3:
                        # Use joystick #2 and initialize it
                        self.p_joystick3 = pygame.joystick.Joystick(2)
                        self.p_joystick3.init()
                    if self.playerNum == 4:
                        # Use joystick #3 and initialize it
                        self.p_joystick4 = pygame.joystick.Joystick(3)
                        self.p_joystick4.init()
            else:   # No joysticks!
                pass

class Bullet(pygame.sprite.Sprite):
    deathctr = 0

    # -- Functions -- #
    def __init__(self, x, y, direction, scale, weapons, walls, playerorAI):
        """ X, Y, [DirectionX, DirectionY], [ScaleWidth, ScaleHeight], Weapons, Walls, PLayer or AI"""
        pygame.sprite.Sprite.__init__(self)

        # Self the X, Y Just in case
        self.x = x
        self.y = y

        # Get the Direction
        self.dirx = direction[0]
        self.diry = direction[1]

        # Grab the Scale Variables
        self.scalewidth = scale[0]
        self.scaleheight = scale[1]

        # Get the Sound, Damange and Speed
        self.weaponname = weapons[0]
        self.weaponspeed = weapons[1]
        self.weapondamage = weapons[2]
        self.weaponcounter = weapons[3]
        self.weaponimage = weapons[4]
        self.weaponsound = weapons[5]

        # Import the Player Image
        self.image = self.weaponimage ###pygame.image.load(self.weaponimage).convert()
        self.image = pygame.transform.scale(self.image,(int(self.scalewidth/48.0), int(self.scaleheight/34.0))) #
        self.image.set_colorkey(BLACK)
        self.oldimage = self.image

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.topleft = [x,y]
        self.imagemask = pygame.mask.from_surface(self.image,127)

        # Count the joysticks the computer has
        self.joystick_count=pygame.joystick.get_count()

        # Get the Lists which will be used for collision detection
        self.walls = walls

        # Get who shot the bullet
        self.playerorAI = playerorAI ### playerorAI True == Player, False == AI

        # Create True and False for both X,Y. True == Greater, False == Lower
        if x > self.dirx: self.X_GrLo = True
        else: self.X_GrLo = False
        if y > self.diry: self.Y_GrLo = True
        else: self.Y_GrLo = False

    def update(self, playerlist, enemylist):
        playercollide = pygame.sprite.spritecollide(self, playerlist, False)
        enemycollide = pygame.sprite.spritecollide(self, enemylist, False)
        wallcollide = pygame.sprite.spritecollide(self, self.walls, False)


        if self.deathctr >= 1:
            pygame.sprite.Sprite.kill(self)
        else:
            if self.playerorAI != True:
                if self.X_GrLo == True:
                    old_x=self.rect.left
                    new_x=old_x+(-1)*self.weaponspeed
                else:
                    old_x=self.rect.left
                    new_x=old_x+(1)*self.weaponspeed
                self.rect.left = new_x

                if self.Y_GrLo == True:
                    old_y=self.rect.top
                    new_y=old_y+(-1)*self.weaponspeed
                else:
                    old_y=self.rect.top
                    new_y=old_y+(1)*self.weaponspeed
                self.rect.top = new_y

                self.imagemask = pygame.mask.from_surface(self.image,127)

                if playercollide:
                    for i in playerlist:
                        if pygame.sprite.collide_mask(self, i):
                            i.set_health(i.get_health()-25)
                            self.deathctr +=1
            else: # Player Bullet
                if self.joystick_count != 0: # Joystick Input
                    # Get the old position, in case we need to go back to it
                    old_x=self.rect.left
                    new_x=old_x+self.diry*self.weaponspeed
                    self.rect.left = new_x

                    old_y=self.rect.top
                    new_y=old_y+self.dirx*self.weaponspeed
                    self.rect.top = new_y

                    self.imagemask = pygame.mask.from_surface(self.image,127)

                    if enemycollide:
                        for i in enemylist:
                            if pygame.sprite.collide_mask(self, i):
                                i.set_health(i.get_health()-25)
                                self.deathctr +=1
                else: # Keyboard Input
                    if self.X_GrLo == True:
                        old_x=self.rect.left
                        new_x=old_x+(-1)*self.weaponspeed
                    else:
                        old_x=self.rect.left
                        new_x=old_x+(1)*self.weaponspeed
                    self.rect.left = new_x

                    if self.Y_GrLo == True:
                        old_y=self.rect.top
                        new_y=old_y+(-1)*self.weaponspeed
                    else:
                        old_y=self.rect.top
                        new_y=old_y+(1)*self.weaponspeed
                    self.rect.top = new_y

                    self.imagemask = pygame.mask.from_surface(self.image,127)

                    if enemycollide:
                        for i in enemylist:
                            if pygame.sprite.collide_mask(self, i):
                                i.set_health(i.get_health()-25)
                                self.deathctr +=1

            if wallcollide: # Time to Check Collisions to see if the Bullet hit comething
                for i in self.walls:
                    if pygame.sprite.collide_mask(self, i):
                        pygame.sprite.Sprite.kill(self)

    def get_rect(self):
        return self.rect

    def set_rect(self, rect):
        self.rect = rect

if __name__ == '__main__':
    screen_width, screen_height = 200,200
    p1currentselect = 1
    pygame.init()
    screen = pygame.display.set_mode([screen_width,screen_height])

    ship01 = os.path.join('Resources', 'Actor', 'PlayerShip01.png')
    ship02 = os.path.join('Resources', 'Actor', 'PlayerShip02.png')
    player_plasmabolt = pygame.image.load(os.path.join('Resources', 'Weapons', 'PlasmaBolt', 'plasmabolt.png')).convert()

    SHIPS = ['', ship01, ship02]
    PLAYERWEAPONS = [('Weapon Name', 'Weapon Speed', 'Weapon Damage', 'Weapon Counter', 'Weapon Image', 'Weapon Sound'),\
     ('Plasma Bolt',  15, 2, 2, player_plasmabolt, 'Resources/Weapons/PlasmaBolt/')]


    players = pygame.sprite.RenderPlain()
    player1 = Actor( screen_width/8.0,screen_height/2.4285714285714284, screen_width, screen_height, SHIPS[p1currentselect], PLAYERWEAPONS, 100, 1 )
    players.add(player1)
    pygame.quit()