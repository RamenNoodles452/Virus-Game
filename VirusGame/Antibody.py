#Nicholas Cesare (9/8/12)
#This game is sick
#Antibody AI 
#basic converging enemies that go to where the player used to be
#with timer (every 5 seconds it prints)
   
import pygame
import sys
import math

class Antibody:
    #Antibodies (basic converging enemies)
    #read where player is, go there, read where player is, go there, repeat
    def __init__(self, spawnX, spawnY):
        #super(Antibody, self).__init__()
        self.img = pygame.image.load("Content/Enemy/Antibody.png")
        self._reticule = pygame.image.load("Content/LockOn.png")
        self._hitBox = self.img.get_rect()
        self._hitBox.topleft = (spawnX, spawnY)
        self.x = self._hitBox.centerx
        self.y = self._hitBox.centery
        self._playerPosition = 0
        self._rotatedImage = self.img
        self._getAngle = [0, 0]
        self._angle = 0
        self._xMag = 0
        self._yMag = 0
        self._speed = 3
        self._timePassed = 0
        self._getAngleToMove = [0, 0]
        self._angleToMove = 0
        
        '''variables used to find the distance the antibody is from the next position'''
        self._distanceNext = 0    #distance the virus is from the next position.  Will be calculated in the update loop
        self._xDistanceSquared = 0
        self._yDistanceSquared = 0
        
        #controls next position of the antibody
        self._nextX = 0
        self._nextY = 0
        self._firstTime = 0
        
        #health and damage stats
        self._bossType = 'none'
        self._lockedOn = False
        self._acidBurning = False
        self._acidTimer = 0.0
        self._acidDamageTimer = 0.0
        self._health = 5        
        
    def Update(self, _playerPosition, elapsedTime):
        self._playerPosition = _playerPosition
        
        '''find the angle between the virus and it's next coordinates, so it knows where to move'''
        self._getAngleToMove[0] = self._nextX - self.x
        self._getAngleToMove[1] = self._nextY - self.y
        self._angleToMove = math.atan2(self._getAngleToMove[0] , self._getAngleToMove[1])
        
        '''Finds the distance between the virus and the player'''
        self._xDistanceSquared = math.pow((self._nextX - self.x), 2)
        self._yDistanceSquared = math.pow((self._nextY - self.y), 2)
        self._distanceNext = math.sqrt(self._xDistanceSquared + self._yDistanceSquared)
        
        '''controls movement of antibody in the proper direction'''
        self._xMag = 1 * math.sin(self._angle)
        self._yMag = 1 * math.cos(self._angle)
        self.x += self._xMag * self._speed
        self.y += self._yMag * self._speed
        self._hitBox.center = (self.x, self.y)
        
        if self._distanceNext < 5 or self._firstTime == 0:
            #find the angle between the antibody and player, as to fix orientation
            self._getAngle[0] = self._playerPosition[0] - self.x
            self._getAngle[1] = self._playerPosition[1] - self.y
            self._angle = math.atan2(self._getAngle[0] , self._getAngle[1])
            self._firstTime = 1
            self._nextX = self._playerPosition[0]
            self._nextY = self._playerPosition[1]
        self._rotatedImage = self.RotateCenter(self.img, math.degrees(self._angle))
        
        '''controls the animation of the antibody'''
        recent_time = elapsedTime
        self._timePassed += recent_time
        if self._timePassed > 250:
            self.img = pygame.image.load("Content/Enemy/Antibody2.png")
        if self._timePassed > 500:
            self.img = pygame.image.load("Content/Enemy/Antibody.png")
            self._timePassed = 0
        
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
        #self._screen.set_at(self._hitBox.midtop, (255, 0, 255))
        #self._screen.set_at(self._hitBox.midbottom, (255, 0, 255))
        #self._screen.set_at(self._hitBox.midright, (255, 0, 255))
        #self._screen.set_at(self._hitBox.midleft, (255, 0, 255))