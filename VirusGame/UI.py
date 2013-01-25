'''
Created on Sep 18, 2012

@author: Robert Stewart
'''

import pygame
import Paused
import Level

class UI():
    
    def __init__(self):
        self._box = pygame.image.load("Content/rectangle.png")
        self._boxh = pygame.image.load("Content/rectangleh.png")
        self._size = ((1280, 720))
        self._screen = pygame.display.set_mode(self._size)
        self._bomb = pygame.image.load("Content/icon/Bomb.png")
        self._acid = pygame.image.load("Content/icon/acid icon.png")
        self._lockon = pygame.image.load("Content/icon/lockon.png")
        self._shield = pygame.image.load("Content/icon/shield icon.png")
        self._bombs = pygame.image.load("Content/icon/Bomb select.png")
        self._acids = pygame.image.load("Content/icon/acid icon select.png")
        self._lockons = pygame.image.load("Content/icon/lockon select.png")
        self._pod = pygame.image.load("Content/icon/pod icon.png")
        self._boss = pygame.image.load("Content/icon/boss icon.png")
        self._machine = pygame.image.load("Content/icon/machine.png")
        self._machines = pygame.image.load("Content/icon/machine select.png")
    def Draw(self):
        
        self._screen.blit(self._shield, (5,670))
        if Paused._bossspawn == 0:
            self._screen.blit(self._pod, (1235,670))
        if Paused._bossspawn == 1:
            self._screen.blit(self._boss, (1235,670))
        for i in range (100):
            if i < Paused._gameProgress:
                self._screen.blit(self._box, (1260,720-((i*6)+70)))
        for i in range (100):
            if i < Paused._playerHealth:
                self._screen.blit(self._box, (10,720-((i*6)+70)))
        for i in range (100):
            if i < Paused._homingAmmo:
                self._screen.blit(self._boxh, ((i*2)+350,695))
        for i in range (100):
            if i < Paused._bombAmmo:
                self._screen.blit(self._boxh, ((i*2)+650,695))
        for i in range (100):
            if i < Paused._sprayAmmo:
                self._screen.blit(self._boxh, ((i*2)+950,695))
        if Paused._bulletType == 0:
            self._screen.blit(self._machines, (220,690))
            self._screen.blit(self._bomb, (620,690))
            self._screen.blit(self._lockon, (320,690))
            self._screen.blit(self._acid, (920,690))
        if Paused._bulletType == 1:
            self._screen.blit(self._machine, (220,690))
            self._screen.blit(self._bomb, (620,690))
            self._screen.blit(self._lockon, (320,690))
            self._screen.blit(self._acids, (920,690))
        if Paused._bulletType == 2:
            self._screen.blit(self._machine, (220,690))
            self._screen.blit(self._bomb, (620,690))
            self._screen.blit(self._lockons, (320,690))
            self._screen.blit(self._acid, (920,690))
        if Paused._bulletType == 3:
            self._screen.blit(self._machine, (220,690))
            self._screen.blit(self._bombs, (620,690))
            self._screen.blit(self._lockon, (320,690))
            self._screen.blit(self._acid, (920,690))