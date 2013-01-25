#Nicholas Cesare (9/12/12)
#This game is sick
#Virus Enemy AI
#Swarms near the player and fires a projectile periodically
   
import pygame
import DnaProjectile
import sys
import math
import random

class Virus:
    #Virus (converge near enemy and fire projectile periodically)
    #virus needs to have its own clock, otherwise the clock.tick function won't work
    def __init__(self, spawnX, spawnY):
        self.img = pygame.image.load("Content/Enemy/Virus.png")
        self._reticule = pygame.image.load("Content/LockOn.png")
        self._hitBox = self.img.get_rect()
        self._hitBox.topleft = (spawnX, spawnY)
        self.x = self._hitBox.centerx
        self.y = self._hitBox.centery
        self._playerPosition = 0
        self._rotatedImage = self.img
        self._getAngle = [0, 0]
        self._angle = 0
        self._getAngleToMove = [0, 0]
        self._angleToMove = 0
        self._xMag = 0
        self._yMag = 0
        self._speed = 1
        self._time = 0
        self.time_passed = 0
        self.recent_time = 0
        self._getOut = 0
        
        self._nextX = random.randrange(1,1279)
        self._nextY = random.randrange(1,719)
        '''variables used to find the distance the virus is from the player'''
        self._distanceNext = 0    #distance the virus is from the player.  Will be calculated in the update loop
        self._xDistanceSquared = 0
        self._yDistanceSquared = 0
        
        #health and damage stats
        self._bossType = 'none'
        self._lockedOn = False
        self._acidBurning = False
        self._acidTimer = 0.0
        self._acidDamageTimer = 0.0
        self._health = 3
        
    def Update(self, _playerPosition, elapsedTime, dnaList):
        self._playerPosition = _playerPosition
        #print self._nextX
        #print self._nextY
        
        '''find the angle between the virus and player, as to fix orientation'''
        self._getAngle[0] = self._playerPosition[0] - self.x
        self._getAngle[1] = self._playerPosition[1] - self.y
        self._angle = math.atan2(self._getAngle[0] , self._getAngle[1])
        self._rotatedImage = self.RotateCenter(self.img, math.degrees(self._angle))
        
        '''find the angle between the virus and it's next coordinates, so it knows where to move'''
        self._getAngleToMove[0] = self._nextX - self.x
        self._getAngleToMove[1] = self._nextY - self.y
        self._angleToMove = math.atan2(self._getAngleToMove[0] , self._getAngleToMove[1])
        
        
        '''controls movement of virus in the proper direction'''
        self._xMag = 1 * math.sin(self._angleToMove)
        self._yMag = 1 * math.cos(self._angleToMove)
        self.x += self._xMag * self._speed
        self.y += self._yMag * self._speed
        self._hitBox.center = (self.x, self.y)
        
        '''Finds the distance between the virus and the player'''
        self._xDistanceSquared = math.pow((self._nextX - self.x), 2)
        self._yDistanceSquared = math.pow((self._nextY - self.y), 2)
        self._distanceNext = math.sqrt(self._xDistanceSquared + self._yDistanceSquared)
        
        #jitteryness in the x and y directions can never be the same.  Try .01 and .02 for refference
        self._hitBox.y += 7 * math.sin(self._time * .008)   #controlls "Jitteryness" in the y direction
        self._hitBox.x -= 7 * math.sin(self._time * .005)   #controlls "Jitteryness" in the x direction
        
        if self._distanceNext > 500:
            self._speed = 9
        if self._distanceNext < 500 and self._distanceNext > 400:
            self._speed = 8
        if self._distanceNext < 400 and self._distanceNext > 300:
            self._speed = 7
        if self._distanceNext <= 300 and self._distanceNext >= 200:
            self._speed = 6
        if self._distanceNext < 200:
            self._speed = 5
        if self._distanceNext < 100:
            self._speed = 4
        if self._distanceNext < 50:
            self._speed = 3
        if self._distanceNext < 5: 
            self._nextX = random.randrange(1,1279)    
            self._nextY = random.randrange(1,719)
            
        self.HandleDnaProjectile(elapsedTime, dnaList)
        
    def RotateCenter(self, objectToRotate, rotationAngle):
        '''rotate an image while keeping its center and size'''
        orig_rect = objectToRotate.get_rect()
        rot_image = pygame.transform.rotate(objectToRotate, rotationAngle)
        rot_rect = orig_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy()
        return rot_image
        
    def HandleDnaProjectile(self, elapsedTime, dnaList):
        self.recent_time = elapsedTime
        self.time_passed  += self.recent_time
        if self.time_passed > 2000:  #keeps track of the time so you can spawn another Dna Projectile.
            self.time_passed = 0
            #print "New child Dna Projectile created."
            tempchild = DnaProjectile.DnaProjectile( self._angle, self._hitBox.centerx, self._hitBox.centery)
            dnaList.append(tempchild)

    def Draw(self, screen):
        screen.blit(self._rotatedImage, self._hitBox.topleft)
        if self._lockedOn == True:
            screen.blit(self._reticule, (self._hitBox.centerx - 20, self._hitBox.centery - 20))
        #self._screen.set_at(self._hitBox.midtop, (255, 0, 255))
        #self._screen.set_at(self._hitBox.midbottom, (255, 0, 255))
        #self._screen.set_at(self._hitBox.midright, (255, 0, 255))
        #self._screen.set_at(self._hitBox.midleft, (255, 0, 255))