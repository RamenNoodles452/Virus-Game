#Nicholas Cesare (9/8/12)
#This game is sick
#Child Bacteria AI 
#enemies converge on parent bacteria and float around in a cloud

import pygame
import sys
import math
import random

class ChildBacteria:
    #baby bacteria that swarm near their parent bacteria
    def __init__(self, spawnX, spawnY):
        self.img = pygame.image.load("Content/Enemy/BacteriaChild.png")
        self._reticule = pygame.image.load("Content/LockOn.png")
        self._hitBox = pygame.Rect(0, 0, 20, 20)
        self._hitBox.center = (spawnX, spawnY)
        self.x = spawnX
        self.y = spawnY
        self.vel_x = random.choice([-2, -1, 1, 2])
        if self.vel_x > 0:
            self.movingRight = True
        elif self.vel_x < 0:
            self.movingRight = False
        self.vel_y = random.choice([-2, -1, 1, 2])
        if self.vel_y > 0:
            self.movingUp = False
        elif self.vel_y < 0:
            self.movingUp = True    
        self._hitBox.topleft = (self.x, self.y)
        self._bacteriaPosition = 0
        self._rotatedImage = self.img
        self._angle = 0
        
        #health and damage stats
        self._bossType = 'none'
        self._lockedOn = False
        self._acidBurning = False
        self._acidTimer = 0.0
        self._acidDamageTimer = 0.0
        self._health = 3
        
    def Update(self, _bacteriaPosition):
        '''controls child bacteria's movements'''
        self._bacteriaPosition = _bacteriaPosition
        future_rect = self._hitBox.move(self.vel_x, self.vel_y)

        if future_rect.centerx < (self._bacteriaPosition[0] - 150) and self.movingRight == False:
            self.vel_x = -self.vel_x
            self.movingRight = True
        if future_rect.centerx > (self._bacteriaPosition[0] + 150) and self.movingRight == True:
            self.vel_x = -self.vel_x
            self.movingRight = False
        if future_rect.centery < (self._bacteriaPosition[1] - 150) and self.movingUp == True:
            self.vel_y = -self.vel_y
            self.movingUp = False
        if future_rect.centery > (self._bacteriaPosition[1] + 150) and self.movingUp == False:
            self.vel_y = -self.vel_y
            self.movingUp = True
            
        self._hitBox.move_ip(self.vel_x, self.vel_y)
        self._angle -= .5   # controls rotation speed of Child Bacteria
        if self._angle >= 360:
            self._angle = 0
        
        #self._rotatedImage = self.RotateCenter(self.img, math.radians(self._angle))
        #print self._angle
        self._rotatedImage = self.RotateCenter(self.img, self._angle)

    def RotateCenter(self, objectToRotate, rotationAngle):
        '''rorate an image while keeping its center and size'''
        orig_rect = objectToRotate.get_rect()
        rot_image = pygame.transform.rotate(objectToRotate, rotationAngle)
        rot_rect = orig_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy() #normalizes image, but we want pulsating child bacteria
        return rot_image
    
    def Draw(self, screen):
        screen.blit(self._rotatedImage, (self._hitBox.left - 15, self._hitBox.top - 15))
        if self._lockedOn == True:
            screen.blit(self._reticule, (self._hitBox.centerx - 20, self._hitBox.centery - 20))
        #self._screen.set_at(self._hitBox.midtop, (255, 0, 255))
        #self._screen.set_at(self._hitBox.midbottom, (255, 0, 255))
        #self._screen.set_at(self._hitBox.midright, (255, 0, 255))
        #self._screen.set_at(self._hitBox.midleft, (255, 0, 255))