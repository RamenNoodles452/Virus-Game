'''
Created on Sep 6, 2012

@author: Korea
'''

import pygame
import BasicPlayerBullet
import AcidBullet
import LockOnLaser
import HomingLaser
import Bomb
import CollisionDetection
import Paused
import sys
import os
import math
import random

class Player():
    '''
    classdocs
    '''
    def __init__(self, playerStartPosition):
        '''
        Constructor
        '''
        self._collisionDetection = CollisionDetection.CollisionDetection()
        self._gamepad = pygame.joystick.Joystick(0)
        self._gamepad.init()
        
        self._mantaBody = pygame.image.load("Content/Player/MantaBody.png").convert_alpha()
        self._mantaTurret = pygame.image.load("Content/Player/MantaTurret.png").convert_alpha()
        self._rotatedMantaBody = self._mantaBody
        self._rotatedMantaTurret = self._mantaTurret
        self._playerHitBox = pygame.Rect(0, 0, 40, 40)
        self._playerTurretBox = self._rotatedMantaTurret.get_rect()
        self._playerTurretBox.topleft = self._playerPosition = playerStartPosition
        self._playerHitBox.center = self._playerTurretBox.center
        
        self._playerSpeed = 400.0
        self._xspeed = 0
        self._yspeed = 0
        
        #variables dealing with the angle direction of the ship and turret
        self._xShipAngle = 0
        self._yShipAngle = 0
        self._shipAngle = 0
        self._xTurretAngle = 0
        self._yTurretAngle = 0
        self._turretAngle = 0
        self._turretAngle = 0
        self._turretAngleR = 0.0

        #variables dealing with the ship's projectiles
        self._isFiring = False
        self._laserState = False
        self._bulletsList = []
        self._targetingLaserList = []
        self._homingLaserList = []
        self._homingTargetsList = []
        self._sprayList = []
        self._bombList = []
        self._drawHomingLasers = False
        self._laserAngle = math.pi/8
        self._recentTime = 0
        self._elapsedTime = 0
        self._sprayReloadTime = 0
        self._homingReloadTime = 0
        self._bombReloadTime = 0
        #what kind of bullet is the player using?
        # 0 = regular
        # 1 = acid
        # 2 = laser
        # 3 = Bomb
        Paused._bulletType = 0
        
        #ammo counters for the special attacks. these recharge over time
        Paused._sprayAmmo = 100
        self._sprayMaxAmmo = 100
        Paused._homingAmmo = 100
        self._homingMaxAmmo = 100
        Paused._bombAmmo = 100
        self._bombMaxAmmo = 100
        
        Paused._playerHealth = 100
        
    def CreateHomingLaser(self, targetHitBox):
        return HomingLaser.HomingLaser(targetHitBox, self._playerHitBox.centerx, self._playerHitBox.centery, self._laserAngle, self._turretAngle)
        
    def Update(self, elapsedTime, clock, bitMask):
        '''
        updates the player
        '''
        
        self.HandleInput()
        #print self._xspeed
        
        # update the player's position
        #print self._playerHitBox.topleft
        HitBox = self._collisionDetection.CollisionMovement(self._playerHitBox, bitMask, self._xspeed, self._yspeed, elapsedTime)
        #print HitBox.topleft
        self._playerPosition = HitBox.topleft
        #self._playerPosition = self._playerHitBox.topleft = self._playerTurretBox.topleft
        
        #update player's rotation
        self._rotatedMantaBody = self.RotateCenter(self._mantaBody, self._shipAngle)
        self._rotatedMantaTurret = self.RotateCenter(self._mantaTurret, self._turretAngle)
        
        self.HandleBullets(elapsedTime, clock, bitMask)
        
        self.ReplenishAmmo(elapsedTime, clock)
        
    def RotateCenter(self, objectToRotate, rotationAngle):
        '''rorate an image while keeping its center and size'''
        orig_rect = objectToRotate.get_rect()
        rot_image = pygame.transform.rotate(objectToRotate, rotationAngle)
        rot_rect = orig_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy()
        return rot_image
    
    def HandleInput(self):
        for e in pygame.event.get(): # iterate over event stack
            #print 'event : ' + str(e.type)
            if e.type == pygame.JOYAXISMOTION:
                
                x , y = self._gamepad.get_axis(0), self._gamepad.get_axis(1)
                x2, y2 = self._gamepad.get_axis(4), self._gamepad.get_axis(3)
                
                if abs(x) < 0.3:
                    x = 0
                if abs(y) < 0.3:
                    y = 0            
                if abs(x) > 0 or abs(y) > 0:
                    self._xShipAngle = x
                    self._yShipAngle = y   
                self._shipAngle = math.atan2(self._xShipAngle, self._yShipAngle)
                self._shipAngle = math.degrees(self._shipAngle)    
                    
                self._xspeed = x * self._playerSpeed
                self._yspeed = y * self._playerSpeed
                
                
                if abs(x2) > 0.3 or abs(y2) > 0.3:
                    self._isFiring = True
                
                if abs(x2) < 0.3 and abs(y2) < 0.3:
                    x2 = x
                    y2 = y
                    self._isFiring = False 
                    
                if abs(x2) > 0.3 or abs(y2) > 0.3:
                    self._xTurretAngle = x2
                    self._yTurretAngle = y2     
     
                self._turretAngleR = math.atan2(self._xTurretAngle, self._yTurretAngle)
                self._turretAngle = math.degrees(self._turretAngleR)
                
            elif e.type == pygame.JOYBUTTONDOWN: # 10
                #print 'button down: ' , e.button   
                '''something'''
                if e.button == 0:
                    Paused._bulletType = 0
                if e.button == 1:
                    Paused._bulletType = 1
                if e.button == 2:
                    Paused._bulletType = 2
                if e.button == 3:
                    Paused._bulletType = 3
                if e.button == 9:
                    if len(self._bombList) > 0:
                        self._bombList[0]._explode = True
                if e.button == 7:
                    Paused._PauseState = 1
                    Paused._musicPlay = 1
            
            elif e.type == pygame.JOYBUTTONUP: # 11
                #print 'button up: ' , e.button
                '''something'''
            elif e.type == pygame.QUIT:
                exit()
                
    def HandleBullets(self, elapsedTime, clock, bitMask):
        '''
        this function handles updating the bullets as well as removing them from the list once they collide with something
        '''
        
        if self._isFiring == True:
            if Paused._bulletType == 0:
                self._recentTime = elapsedTime / 10.0
                self._elapsedTime  += self._recentTime
                if self._elapsedTime > 10:
                    self._elapsedTime = 0
                    p = BasicPlayerBullet.BasicPlayerBullet(self._turretAngleR, self._playerHitBox.centerx, self._playerHitBox.centery)
                    self._bulletsList.append(p)
            if Paused._bulletType == 1:
                if Paused._sprayAmmo > 2:
                    self._recentTime = elapsedTime / 2.0
                    self._elapsedTime += self._recentTime
                    if self._elapsedTime > 10:
                        self._elapsedTime = 0
                        Paused._sprayAmmo -= 1
                        p = AcidBullet.AcidBullet(random.uniform( (self._turretAngleR - (math.pi / 7)) , (self._turretAngleR + (math.pi / 7)) ), self._playerHitBox.centerx, self._playerHitBox.centery)
                        self._sprayList.append(p)
            if Paused._bulletType == 2:
                self._laserState = True
                p = LockOnLaser.LockOnLaser(self._turretAngleR, self._playerHitBox.centerx, self._playerHitBox.centery)
                self._targetingLaserList.append(p)
            if Paused._bulletType == 3:
                if len(self._bombList) == 0 and Paused._bombAmmo == 100:
                    Paused._bombAmmo -= 100
                    b = Bomb.Bomb(self._turretAngleR, self._playerHitBox.centerx, self._playerHitBox.centery)
                    self._bombList.append(b)
                    
        elif self._isFiring == False:
            if Paused._bulletType == 2:
                self._laserState = False
                del self._targetingLaserList[:]

        #update the bullets
        for b in self._bulletsList:
            b.Update(elapsedTime)
        #update the spray
        for b in self._sprayList:
            b.Update(elapsedTime)
            if b._isActive == False:
                self._sprayList.pop(self._sprayList.index(b))
        
        #update the homing lasers
        for b in self._targetingLaserList:
            b.Update(elapsedTime)
        if self._laserState == False and len(self._homingLaserList) > 0:
            self._drawHomingLasers = True
            self._laserAngle = 0.1
            for h in self._homingLaserList:
                h._fired = True                
        if self._homingLaserList > 0:
            for h in self._homingLaserList:
                laserIndex = self._homingLaserList.index(h)
                #this handles if the target dies before the laser gets there. MIGHT NOT WORK
                if self._homingTargetsList[laserIndex] == None:
                    self._homingLaserList.pop(laserIndex)

                h.Update(elapsedTime, self._homingTargetsList[laserIndex], self._playerHitBox.centerx, self._playerHitBox.centery, self._turretAngleR)
                
                if self._collisionDetection.ObjectCollision(h._hitBox, h._targetHitBox) == True:
                    self._homingTargetsList[laserIndex]._health -= 3
                    #only for hitting the boss
                    if self._homingTargetsList[laserIndex]._bossType == 'head':
                        Paused._gameProgress -= 0.5
                    if self._homingTargetsList[laserIndex]._bossType == 'body':
                        Paused._gameProgress -= 0.5
                    self._homingLaserList.pop(laserIndex)
                    self._homingTargetsList.pop(laserIndex)
                    
        if len(self._homingLaserList) == 0:
            self._drawHomingLasers = False
        
        for b in self._bombList:
            if b._explosionFinished == True:
                self._bombList.pop(self._bombList.index(b))
    
    def ReplenishAmmo(self, elapsedTime, clock):
        if self._isFiring == False and Paused._sprayAmmo < self._sprayMaxAmmo:
            ammoTick = elapsedTime
            self._sprayReloadTime += ammoTick
            if self._sprayReloadTime > 2:
                self._sprayReloadTime = 0
                Paused._sprayAmmo += 1
        if Paused._sprayAmmo > self._sprayMaxAmmo:
            Paused._sprayAmmo = self._sprayMaxAmmo
            
        if self._isFiring == False and Paused._homingAmmo < self._homingMaxAmmo:
            ammoTick = elapsedTime
            self._homingReloadTime += ammoTick
            if self._homingReloadTime > 20:
                self._homingReloadTime = 0
                Paused._homingAmmo += 1
            
        if len(self._bombList) == 0 and Paused._bombAmmo < self._bombMaxAmmo:
            ammoTick = elapsedTime
            self._bombReloadTime += ammoTick
            if self._bombReloadTime > 10:
                self._bombReloadTime = 0
                Paused._bombAmmo += 1
        
    def Draw(self, screen):
        '''
        draws the player
        '''
        screen.blit(self._rotatedMantaBody, (self._playerHitBox.left - 7, self._playerHitBox.top - 7))
        screen.blit(self._rotatedMantaTurret, (self._playerHitBox.left - 7, self._playerHitBox.top - 7))
        #self._screen.set_at(self._playerHitBox.midtop, (255,255,255))
        #self._screen.set_at(self._playerHitBox.midleft, (255,255,255))
        #self._screen.set_at(self._playerHitBox.midright, (255,255,255))
        #self._screen.set_at(self._playerHitBox.midbottom, (255,255,255))
        
        #for b in self._bulletsList:
        #    b.Draw()
        
        