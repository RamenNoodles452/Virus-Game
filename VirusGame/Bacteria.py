#Nicholas Cesare (9/8/12)
#This game is sick
#Bacteria AI 
#basic converging enemies
#with timer (every 5 seconds it prints)
   
import pygame
import sys
import ChildBacteria
import math

class Bacteria:
    #Bacteria mother (basic converging enemies, calls children that swarm bacteria itself)
    def __init__(self, spawnX, spawnY):
        #super(Bacteria, self).__init__()
        self.img = pygame.image.load("Content/Enemy/BacteriaParent.png")
        self._reticule = pygame.image.load("Content/LockOn.png")
        self._hitBox = pygame.Rect(0, 0, 35, 35)
        self._hitBox.center = (spawnX, spawnY)
        self.x = self._hitBox.centerx
        self.y = self._hitBox.centery
        self._hitBox.topleft = (self.x, self.y)
        self.time_passed = 0
        self._playerPosition = 0
        self._childBacteriaList = []
        self._rotatedImage = self.img
        self._getAngle = [0, 0]
        self._angle = 0
        self._rotationAngle = 0
        self._xMag = 0
        self._yMag = 0
        self._speed = 1
        
        #health and damage stats
        self._bossType = 'none'
        self._lockedOn = False
        self._acidBurning = False
        self._acidTimer = 0.0
        self._acidDamageTimer = 0.0
        self._health = 10

    def Update(self, _playerPosition, clock, elapsedTime):
        self._playerPosition = _playerPosition
        self.HandleChildBacteria(clock, elapsedTime)
        
        '''find the angle between the bacteria and player.'''
        self._getAngle[0] = self._playerPosition[0] - self.x
        self._getAngle[1] = self._playerPosition[1] - self.y
        self._angle = math.atan2(self._getAngle[0] , self._getAngle[1])
        
        '''rotates the image '''
        #self._hitBox.topleft = (self.x, self.y)                 #might get commented out
        
        self._rotationAngle += .5   # controls rotation speed of Bacteria
        if self._rotationAngle >= 360:
            self._rotationAngle = 0
        self._rotatedImage = self.RotateCenter(self.img, self._rotationAngle) 
        
        '''controls movement of bacteria in the proper direction'''
        self._xMag = 1 * math.sin(self._angle)
        self._yMag = 1 * math.cos(self._angle)
        self.x += self._xMag * self._speed
        self.y += self._yMag * self._speed
        self._hitBox.center = (self.x, self.y)
    
    def RotateCenter(self, objectToRotate, rotationAngle):
        '''rotate an image while keeping its center and size'''
        orig_rect = objectToRotate.get_rect()
        rot_image = pygame.transform.rotate(objectToRotate, rotationAngle)
        rot_rect = orig_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy()
        return rot_image
    
    def HandleChildBacteria(self, clock, elapsedTime):
        recent_time = elapsedTime
        self.time_passed += recent_time
        if self.time_passed > 3000:  #keeps track of the time so you can spawn another child bacteria.
            self.time_passed = 0
            #print "New child bacteria created."
            tempchild = ChildBacteria.ChildBacteria(self._hitBox.centerx, self._hitBox.centery)
            self._childBacteriaList.append(tempchild)
            
        for i in self._childBacteriaList:
            i.Update(self._hitBox.center)
    
    def Draw(self, screen):
        screen.blit(self._rotatedImage, (self._hitBox.left - 40, self._hitBox.top - 40))
        if self._lockedOn == True:
            screen.blit(self._reticule, (self._hitBox.centerx - 20, self._hitBox.centery - 20))
        #self._screen.set_at(self._hitBox.midtop, (255, 0, 255))
        #self._screen.set_at(self._hitBox.midbottom, (255, 0, 255))
        #self._screen.set_at(self._hitBox.midright, (255, 0, 255))
        #self._screen.set_at(self._hitBox.midleft, (255, 0, 255))
        for e in self._childBacteriaList:
            e.Draw(screen)