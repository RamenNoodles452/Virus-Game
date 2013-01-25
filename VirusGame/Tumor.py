'''
Created on Sep 18, 2012

@author: Korea
'''

import pygame

class Tumor:
    '''
    classdocs
    '''
    def __init__(self, spawnX, spawnY, elapsedTime):
        '''
        Constructor
        '''
        self._tumorGrow0 = pygame.image.load("Content/Enemy/Growth/growth_grow0.png")
        self._tumorGrow1 = pygame.image.load("Content/Enemy/Growth/growth_grow1.png")
        self._tumorGrow2 = pygame.image.load("Content/Enemy/Growth/growth_grow2.png")
        self._tumorGrow3 = pygame.image.load("Content/Enemy/Growth/growth_grow3.png")
        self._tumor = pygame.image.load("Content/Enemy/Growth/Growth0.png")
        self._tumorBlink = pygame.image.load("Content/Enemy/Growth/Growth_hit.png")
        self._reticule = pygame.image.load("Content/LockOn.png")
        self._hitBox = self._tumor.get_rect()
        self._hitBox.center = (spawnX, spawnY)
        self._growFinished = False
        self._growTimer = 0
        self._growState = 0
        
        #health and damage stats
        self._hit = False
        self._bossType = 'nope'
        self._lockedOn = False
        self._acidBurning = False
        self._acidTimer = 0.0
        self._acidDamageTimer = 0.0
        self._health = 30
        self._healthRegenTimer = 0
        
    def Update(self, elapsedTime):
        self.Grow(elapsedTime)
        
        if self._health < 30:
            regenTick = elapsedTime
            self._healthRegenTimer += regenTick
            if self._healthRegenTimer > 1500:
                self._healthRegenTimer = 0
                self._health += 1
                
    def Grow(self, elapsedTime):
        growTimer = elapsedTime
        self._growTimer += growTimer
        if self._growTimer > 20:
            self._growState += 1
            self._growTimer = 0
        if self._growState == 3:
            self._growFinished = True
                
    def Draw(self, screen):
        if self._growFinished == False:
            if self._growState == 0:
                screen.blit(self._tumorGrow0, self._hitBox.topleft)
            elif self._growState == 1:
                screen.blit(self._tumorGrow1, self._hitBox.topleft)
            elif self._growState == 2:
                screen.blit(self._tumorGrow2, self._hitBox.topleft)
            elif self._growState == 3:
                screen.blit(self._tumorGrow3, self._hitBox.topleft)
        elif self._growFinished == True:
            if self._hit == False:
                screen.blit(self._tumor, self._hitBox.topleft)
            elif self._hit == True:
                screen.blit(self._tumorBlink, self._hitBox.topleft)
                self._hit = False
        
        if self._lockedOn == True:
            screen.blit(self._reticule, (self._hitBox.centerx - 20, self._hitBox.centery - 20))