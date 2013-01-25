#Nicholas Cesare (9/18/12)
#This game is sick
#Enemy death animations
'''This file runs all of the enemy death animations, given coordinates and a number signifying which enemy it is'''
   
import pygame
import sys
import math

class EnemyDeathAnimations:
    def __init__(self, _deathPosition, _enemyType):
        
        self._antibody1 = pygame.image.load("Content/EnemyAnimations/AntibodyDeath1.png").convert_alpha()
        self._antibody2 = pygame.image.load("Content/EnemyAnimations/AntibodyDeath2.png").convert_alpha()
        self._antibody3 = pygame.image.load("Content/EnemyAnimations/AntibodyDeath3.png").convert_alpha()
        self._bacteria1 = pygame.image.load("Content/EnemyAnimations/BacteriaDeath1.png").convert_alpha()
        self._bacteria2 = pygame.image.load("Content/EnemyAnimations/BacteriaDeath2.png").convert_alpha()
        self._bacteria3 = pygame.image.load("Content/EnemyAnimations/BacteriaDeath3.png").convert_alpha()
        self._childBacteria1 = pygame.image.load("Content/EnemyAnimations/ChildBacteriaDeath1.png").convert_alpha()
        self._childBacteria2 = pygame.image.load("Content/EnemyAnimations/ChildBacteriaDeath2.png").convert_alpha()
        self._childBacteria3 = pygame.image.load("Content/EnemyAnimations/ChildBacteriaDeath3.png").convert_alpha()
        self._virus1 = pygame.image.load("Content/EnemyAnimations/VirusDeath1.png").convert_alpha()
        self._virus2 = pygame.image.load("Content/EnemyAnimations/VirusDeath2.png").convert_alpha()
        self._virus3 = pygame.image.load("Content/EnemyAnimations/VirusDeath3.png").convert_alpha()
        self._growth0 = pygame.image.load("Content/Enemy/Growth/growth0.png").convert_alpha()
        self._growth1 = pygame.image.load("Content/Enemy/Growth/growth1.png").convert_alpha()
        self._growth2 = pygame.image.load("Content/Enemy/Growth/growth2.png").convert_alpha()
        self._growth3 = pygame.image.load("Content/Enemy/Growth/growth3.png").convert_alpha()
        self._growth4 = pygame.image.load("Content/Enemy/Growth/growth4.png").convert_alpha()
        self._growth5 = pygame.image.load("Content/Enemy/Growth/growth5.png").convert_alpha()
        self._growth6 = pygame.image.load("Content/Enemy/Growth/growth6.png").convert_alpha()
        self._growth7 = pygame.image.load("Content/Enemy/Growth/growth7.png").convert_alpha()
        
        self._deathState = 0
        
        self._hitBox = self._antibody1.get_rect()
        self._hitBox.center = _deathPosition
        self._enemyType = _enemyType
        self._timePassed = 0
        self._finished = False
    
    def Update(self, _elapsedTime):
        recent_time = _elapsedTime
        self._timePassed += recent_time
        
        if self._enemyType != 5:
            if self._timePassed > 100:
                self._timePassed = 0
                self._deathState += 1
            if self._deathState == 3:
                self._finished = True
        elif self._enemyType == 5:
            if self._timePassed > 100:
                self._timePassed = 0
                self._deathState += 1
            if self._deathState == 8:
                self._finished = True

    def Draw(self, screen):
        if self._deathState == 1 and self._enemyType == 1:
            screen.blit(self._antibody1, self._hitBox.topleft)
        if self._deathState == 2 and self._enemyType == 1:
            screen.blit(self._antibody2, self._hitBox.topleft)
        if self._deathState == 3 and self._enemyType == 1:
            screen.blit(self._antibody3, self._hitBox.topleft)
        if self._deathState == 1 and self._enemyType == 2:
            screen.blit(self._bacteria1, self._hitBox.topleft)
        if self._deathState == 2 and self._enemyType == 2:
            screen.blit(self._bacteria2, self._hitBox.topleft)
        if self._deathState == 3 and self._enemyType == 2:
            screen.blit(self._bacteria3, self._hitBox.topleft)
        if self._deathState == 1 and self._enemyType == 3:
            screen.blit(self._childBacteria1, self._hitBox.topleft)
        if self._deathState == 2 and self._enemyType == 3:
            screen.blit(self._childBacteria2, self._hitBox.topleft)
        if self._deathState == 3 and self._enemyType == 3:
            screen.blit(self._childBacteria3, self._hitBox.topleft)
        if self._deathState == 1 and self._enemyType == 4:
            screen.blit(self._virus1, self._hitBox.topleft)
        if self._deathState == 2 and self._enemyType == 4:
            screen.blit(self._virus2, self._hitBox.topleft)
        if self._deathState == 3 and self._enemyType == 4:
            screen.blit(self._virus3, self._hitBox.topleft)
        if self._deathState == 1 and self._enemyType == 5:
            screen.blit(self._growth0, self._hitBox.topleft)
        if self._deathState == 2 and self._enemyType == 5:
            screen.blit(self._growth1, self._hitBox.topleft)
        if self._deathState == 3 and self._enemyType == 5:
            screen.blit(self._growth2, self._hitBox.topleft)
        if self._deathState == 4 and self._enemyType == 5:
            screen.blit(self._growth3, self._hitBox.topleft)    
        if self._deathState == 5 and self._enemyType == 5:
            screen.blit(self._growth4, self._hitBox.topleft)
        if self._deathState == 6 and self._enemyType == 5:
            screen.blit(self._growth5, self._hitBox.topleft)
        if self._deathState == 7 and self._enemyType == 5:
            screen.blit(self._growth6, self._hitBox.topleft)
        if self._deathState == 8 and self._enemyType == 5:
            screen.blit(self._growth7, self._hitBox.topleft)
        