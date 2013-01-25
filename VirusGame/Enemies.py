'''
Created on Sep 10, 2012

@author: Korea
'''
import pygame
import Antibody
import Bacteria
import Virus
import Tumor
import Boss
import DnaProjectile
import random

class Enemies:
    '''
    classdocs
    '''
    def __init__(self):
        '''
        Constructor
        '''
        self._bacteriaList = []
        self._antibodyList = []  
        self._virusList = []
        self._tumorList = []
        self._bossList = []
        self._dnaList = []
                
    def GetAntiBodyList(self):
        self._antibodyList
        
    def GetBacteriaList(self):
        self._bacteriaList
        
    def Update(self, playerCenterPosition, clock, elapsedTime):
        '''
        this thing updates all the enemies
        '''
        for b in self._bacteriaList:
            b.Update(playerCenterPosition, clock, elapsedTime)
        for a in self._antibodyList:
            a.Update(playerCenterPosition, elapsedTime)
        for c in self._virusList:
            c.Update(playerCenterPosition, elapsedTime, self._dnaList)
        for t in self._tumorList:
            t.Update(elapsedTime)    
        for d in self._bossList:
            d.Update(playerCenterPosition, elapsedTime)
        for j in self._dnaList:
            j.Update(elapsedTime)
        
    def AddEnemy(self, spawnX, spawnY, type, elapsedTime):
        if type == 'bacteria':
            tempBac = Bacteria.Bacteria(spawnX, spawnY)
            self._bacteriaList.append(tempBac)
        elif type == 'antibody':
            tempAnti = Antibody.Antibody(spawnX, spawnY)
            self._antibodyList.append(tempAnti)
        elif type == 'virus':
            tempVir = Virus.Virus(spawnX, spawnY)
            self._virusList.append(tempVir)
        elif type == 'tumor':
            tempTum = Tumor.Tumor(spawnX, spawnY, elapsedTime)
            self._tumorList.append(tempTum)
        elif type == 'boss':
            tempBoss = Boss.Boss(spawnX, spawnY)
            self._bossList.append(tempBoss)
            
    def Draw(self, screen):
        '''
        this will draw all the enemies
        '''
        for b in self._bacteriaList:
            b.Draw(screen)
        for a in self._antibodyList:
            a.Draw(screen)
        for c in self._virusList:
            c.Draw(screen)
        for t in self._tumorList:
            t.Draw(screen)
        for d in self._bossList:
            d.Draw(screen)
        for j in self._dnaList:
            j.Draw(screen)
