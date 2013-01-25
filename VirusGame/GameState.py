'''
Created on Sep 18, 2012

@author: Korea
'''

import Paused
import random

class GameState:
    '''
    classdocs
    '''
    def __init__(self):
        '''
        Constructor
        '''
        self._gameTimer = 0
        self._antibodySpawnTimer = 0
        self._bacteriaSpawnTimer = 0
        self._virusSpawnTimer = 0
        self._spawnBoss = False
        Paused._gameProgress = 100
        
    def Update(self, elapsedTime, enemies):
        
        if Paused._bossspawn == 0:
            timeTick = elapsedTime
            #THIS SHIT SPAWNS ANTIBODIES
            if len(enemies._antibodyList) < 15:
                self._antibodySpawnTimer += timeTick
                if self._antibodySpawnTimer > 3000:
                    self._antibodySpawnTimer = 0
                    startspot = random.choice([0,1])
                    if startspot == 0:
                        enemies.AddEnemy(random.choice([ 1300, -50]), random.randint(-30, 750), 'antibody', elapsedTime)
                    elif startspot == 1:
                        enemies.AddEnemy(random.randint(-50, 1300), random.choice([-30, 750]), 'antibody', elapsedTime)
            
            #HORY SHEEEEEIT BACTERIUH!
            if len(enemies._bacteriaList) < 5:
                self._bacteriaSpawnTimer += timeTick
                if self._bacteriaSpawnTimer > 10000:
                    self._bacteriaSpawnTimer = 0
                    startspot = random.choice([0,1])
                    if startspot == 0:
                        enemies.AddEnemy(random.choice([ 1300, -50]), random.randint(-30, 750), 'bacteria', elapsedTime)
                    elif startspot == 1:
                        enemies.AddEnemy(random.randint(-50, 1300), random.choice([-30, 750]), 'bacteria', elapsedTime)
                    
            #AHHHHHHHHHHHHHHHHH VIRUSESSSSSSSSSSSSS
            if len(enemies._virusList) < 5:
                self._virusSpawnTimer += timeTick
                if self._virusSpawnTimer > 5000:
                    self._virusSpawnTimer = 0
                    startspot = random.choice([0,1])
                    if startspot == 0:
                        enemies.AddEnemy(random.choice([ 1300, -50]), random.randint(-30, 750), 'virus', elapsedTime)
                    elif startspot == 1:
                        enemies.AddEnemy(random.randint(-50, 1300), random.choice([-30, 750]), 'virus', elapsedTime)
                    
            #creating tumors!
            if Paused._gameProgress == 100 and len(enemies._tumorList) == 0:
                for i in range(4):
                    enemies.AddEnemy(random.randint(100, 1200), random.randint(100, 650), 'tumor', elapsedTime)
            if Paused._gameProgress == 80 and len(enemies._tumorList) == 0:
                for i in range(4):
                    enemies.AddEnemy(random.randint(100, 1200), random.randint(100, 650), 'tumor', elapsedTime)
            if Paused._gameProgress == 60 and len(enemies._tumorList) == 0:
                for i in range(4):
                    enemies.AddEnemy(random.randint(100, 1200), random.randint(100, 650), 'tumor', elapsedTime)
            if Paused._gameProgress == 40 and len(enemies._tumorList) == 0:
                for i in range(4):
                    enemies.AddEnemy(random.randint(100, 1200), random.randint(100, 650), 'tumor', elapsedTime)
            if Paused._gameProgress == 20 and len(enemies._tumorList) == 0:
                for i in range(4):
                    enemies.AddEnemy(random.randint(100, 1200), random.randint(100, 650), 'tumor', elapsedTime)
            if Paused._gameProgress == 0 and len(enemies._tumorList) == 0:
                Paused._gameProgress = 100
                Paused._bossspawn = 1
                enemies.AddEnemy(200, 200, 'boss', elapsedTime)
                Paused._musicPlay = 3
        
