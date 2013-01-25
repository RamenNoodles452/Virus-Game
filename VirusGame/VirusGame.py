'''
Created on Sep 6, 2012

@author: Korea
'''


import pygame
import Menu
import Level
import sys
import Paused
import UI

class VirusGame:
    '''
    classdocs
    '''
    
    def __init__(self):
        '''
        Constructor
        initializes the game
        '''
        pygame.init()
        pygame.display.init()
        self._clock = pygame.time.Clock()
        self._size = ((1280, 720))
        self._screen = pygame.display.set_mode(self._size)
        self._level = Level.Level()
        self._menu = Menu.Menu()
        Paused._PauseState = 2
        self._gamepad = pygame.joystick.Joystick(0)
        self._UI = UI.UI()       
        Paused._musicPlay = 1
        #music stuff
        #self._music = pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=4096)
        #self.sound = pygame.mixer.Sound('Content/music/game_music.wav').play(loops = -1)
        
    def Update(self):
        '''
        Function that updates the game
        '''
        self.MusicChange()
        
        if Paused._PauseState == 0:
            self._elapsedTime = self._clock.get_time()
            self._level.Update(self._elapsedTime, self._clock)
            self._clock.tick(60)
            aprev = 0

        else:
            #self.sound = pygame.mixer.Sound('Content/music/title_music.wav').play(loops = -1)
            self._menu.Update()
            
    def MusicChange(self):
        if Paused._musicPlay == 1:
            pygame.mixer.music.load('Content/music/title_music.wav')
            pygame.mixer.music.play(-1, 0.0)
            Paused._musicPlay = 0
        if Paused._musicPlay == 2:
            pygame.mixer.music.load('Content/music/game_music.wav')
            pygame.mixer.music.play(-1, 0.0)
            Paused._musicPlay = 0
        if Paused._musicPlay == 3:
            pygame.mixer.music.load('Content/music/boss_music.wav')
            pygame.mixer.music.play(-1, 0.0)
            Paused._musicPlay = 0

    def Draw(self):
        '''
        Draws the damn game.
        '''
        self._screen.fill((0,0,0))
        if Paused._PauseState !=0:
            self._level.Draw(self._screen)
            self._UI.Draw()
            self._menu.Draw(self._screen)
            
        else:
            self._level.Draw(self._screen)
            self._UI.Draw()
        '''
        self._screen.fill((0,0,0))
        self._level.Draw(self._screen)
        if self._paused != 0:
            self._menu.Draw(self._clock,self._screen)
        '''
        pygame.display.update()
        #pygame.display.flip()
        
_gameInstance = VirusGame()
while True:
    
    _gameInstance.Update()
    _gameInstance.Draw()

    