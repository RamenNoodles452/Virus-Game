#Nicholas Cesare (9/12/12)
#This game is sick
#Boss Body AI
#Follows the boss head
   
import pygame
import sys
import math

class Boss_Body:
    def __init__(self, spawnX, spawnY, _bodyPartNumber, _isTail):
        self._bodyPartNumber = _bodyPartNumber * 40
        if _isTail == 0:
            self.img = pygame.image.load("Content/Enemy/boss_B.png")
        else:
            self.img = pygame.image.load("Content/Enemy/boss_T.png")
        self._reticule = pygame.image.load("Content/LockOn.png")
        self._hitBox = self.img.get_rect()
        self._hitBox.topleft = (spawnX, spawnY)
        self.x = self._hitBox.centerx
        self.y = self._hitBox.centery
        self._HeadPosition = 0
        self._rotatedImage = self.img
        self._getAngle = [0, 0]
        self._angle = 0
        self._xMag = 0
        self._yMag = 0
        self._speed = 1
        self._time = 0
        self.time_passed = 0
        self.recent_time = 0
        '''variables used to find the distance the virus is from the head'''
        self._distanceHead = 0    #distance the virus is from the head.  Will be calculated in the update loop
        self._xDistanceSquared = 0
        self._yDistanceSquared = 0
        
        #health and damage stats
        self._bossType = 'body'
        self._lockedOn = False
        self._acidBurning = False
        self._acidTimer = 0.0
        self._acidDamageTimer = 0.0
        self._health = 10
        
    def Update(self, _headPosition):
        self._headPosition = _headPosition
            
        '''find the angle between the virus and head, as to fix orientation'''
        self._getAngle[0] = self._headPosition[0] - self.x
        self._getAngle[1] = self._headPosition[1] - self.y
        self._angle = math.atan2(self._getAngle[0] , self._getAngle[1])
        self._rotatedImage = self.RotateCenter(self.img, math.degrees(self._angle))
        
        '''controls movement of virus in the proper direction'''
        self._xMag = 1 * math.sin(self._angle)
        self._yMag = 1 * math.cos(self._angle)
        self.x += self._xMag * self._speed
        self.y += self._yMag * self._speed
        self._hitBox.center = (self.x, self.y)
        
        '''Finds the distance between the virus and the head'''
        self._xDistanceSquared = math.pow((self._headPosition[0] - self.x), 2)
        self._yDistanceSquared = math.pow((self._headPosition[1] - self.y), 2)
        self._distanceHead = math.sqrt(self._xDistanceSquared + self._yDistanceSquared)
        
        #jitteryness in the x and y directions can never be the same.  Try .01 and .02 for refference
        self._hitBox.y += 7 * math.sin(self._time * .008)   #controlls "Jitteryness" in the y direction
        self._hitBox.x -= 7 * math.sin(self._time * .005)   #controlls "Jitteryness" in the x direction
        
        if self._distanceHead <= self._bodyPartNumber:
            self._speed = 0
        else:
            self._speed = 12
        '''if self._distanceHead > (500 + self._bodyPartNumber):
            self._speed = 4
        if self._distanceHead < (500 + self._bodyPartNumber) and self._distanceHead > (400 + self._bodyPartNumber):
            self._speed = 4
        if self._distanceHead < (400 + self._bodyPartNumber) and self._distanceHead > (300 + self._bodyPartNumber):
            self._speed = 4
        if self._distanceHead <= (300 + self._bodyPartNumber) and self._distanceHead >= (100 + self._bodyPartNumber):
            self._speed = 4'''
        
            
        
    def RotateCenter(self, objectToRotate, rotationAngle):
        '''rotate an image while keeping its center and size'''
        orig_rect = objectToRotate.get_rect()
        rot_image = pygame.transform.rotate(objectToRotate, rotationAngle)
        rot_rect = orig_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy()
        return rot_image
        

    def Draw(self, screen):
        screen.blit(self._rotatedImage, self._hitBox.topleft)
        
        if self._lockedOn == True:
            screen.blit(self._reticule, (self._hitBox.centerx - 20, self._hitBox.centery - 20))
        #self._screen.set_at(self._hitBox.center, (255, 0, 255))