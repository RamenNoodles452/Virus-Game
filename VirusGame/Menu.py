'''
Menus for 'This Game is Sick'
by Robert Stewart
Sept 9th
'''

import pygame
import Paused
import sys

class Menu:
    
    def __init__(self):
        pygame.init()
        self._gamepad = pygame.joystick.Joystick(0)
        self._cursor = 1
        self._xprev = 0
        self._aprev = 0
        self._gamepad.init()
        self._start = pygame.image.load("Content/Menu/start.png")
        self._starts = pygame.image.load("Content/Menu/start2.png")
        self._end = pygame.image.load("Content/Menu/End.png")
        self._ends = pygame.image.load("Content/Menu/End2.png")
        self._resume = pygame.image.load("Content/Menu/resume.png")
        self._resumes = pygame.image.load("Content/Menu/resume2.png")
        self._paused = pygame.image.load("Content/Menu/Paused.png")
        self._title = pygame.image.load("Content/Menu/Invader.png")
        self._control = pygame.image.load("Content/Menu/Controller.png")
        self._victory = pygame.image.load("Content/Menu/victory.png")
        
    def Update(self):
        '''
        This is the update loop
        '''
        
        if Paused._PauseState == 1 or Paused._PauseState == 2:
            for e in pygame.event.get():
                x = 0
                a = 0
                if e.type == pygame.JOYAXISMOTION:
                    x = self._gamepad.get_axis(1)
                    if x >= .8 and self._xprev < .8 and self._cursor != 0:
                        self._cursor = self._cursor - 1
                        
                    elif x <= -.8 and self._xprev > -.8 and self._cursor != 1:
                        self._cursor = self._cursor + 1
                        
                if e.type == pygame.JOYBUTTONDOWN:
                    a = self._gamepad.get_button(0)
                    if a == 1 and self._aprev == 0:
                        if self._cursor == 0:
                            sys.exit()
                        elif self._cursor == 1:
                            Paused._PauseState = 0
                            if Paused._bossspawn == 0:
                                Paused._musicPlay = 2
                            if Paused._bossspawn == 1:
                                Paused._musicPlay = 3
                            
                xprev = x
                aprev = a
        else:
            for e in pygame.event.get():
                x = 0
                a = 0
                
                        
                if e.type == pygame.JOYBUTTONDOWN:
                    a = self._gamepad.get_button(0)
                    if self._aprev == 0:
                        sys.exit()
                            
                xprev = x
                aprev = a
                
            
    def Draw(self, screen):
        '''
        This is the render loop
        '''
        
        if Paused._PauseState == 2:
            screen.fill ((255,160,122))
            screen.blit(self._title, (640-300,0))
            screen.blit(self._control, (0, 300))
            if self._cursor == 1:
                    screen.blit(self._starts,(1040-200, 300))
                    screen.blit(self._end, (1040-112,500))
            else:
                    screen.blit(self._start,(1040-195, 300))
                    screen.blit(self._ends, (1040-108, 500))
            
        
        elif Paused._PauseState == 1:
            screen.blit (self._paused, (640-250,-100))
            if self._cursor == 1:
                    screen.blit(self._resumes,(640-250, 300))
                    screen.blit(self._end, (640-112,500))
            else:
                    screen.blit(self._resume,(640-250, 300))
                    screen.blit(self._ends, (640-108, 500))
                    
        elif Paused._PauseState == 3:
            screen.blit(self._victory, (640-300,200))
            screen.blit(self._ends, (640-108, 500))
        
        elif Paused._PauseState == 4:
            screen.blit(self._ends, (640-108, 400))
            
            