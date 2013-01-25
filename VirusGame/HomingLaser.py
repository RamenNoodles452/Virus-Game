'''
Created on Sep 15, 2012

@author: Korea
'''

import pygame
import math

class HomingLaser:
    '''
    classdocs
    '''


    def __init__(self, targetHitBox, startingPositionX, startingPositionY, laserAngle, turretAngle):
        '''
        Constructor
        '''
        self._targetHitBox = targetHitBox
        self._homingLaser = pygame.image.load("Content/Player/HomingLaser.png").convert_alpha()
        self._hitBox = self._homingLaser.get_rect()
        self._hitBox.centerx = startingPositionX
        self._hitBox.centery = startingPositionY
        self._fired = False
        self._projectileSpeed = 800.0
        self._angleOffest = laserAngle
        self._homingAngle = turretAngle + 180 + self._angleOffest
        self._target = [targetHitBox.centerx, targetHitBox.centery]
        self._targetHit = False
        
    def Update(self, elapsedTime, enemy, startingPositionX, startingPositionY, turretAngle):
        self._targetX = enemy._hitBox.centerx
        self._targetY = enemy._hitBox.centery
        self._targetHitBox = enemy._hitBox
        
        # updates the angle of the homing laser
        self._xMag = 1 * math.sin(self._homingAngle)
        self._yMag = 1 * math.cos(self._homingAngle)
        
        # moves the laser bullet with the player if the player hasn't fired yet
        if self._fired == False:
            self._hitBox.centerx = startingPositionX
            self._hitBox.centery = startingPositionY
            self._homingAngle = turretAngle + self._angleOffest + math.pi
        # updates the position of the homing laser if the player has fired
        elif self._fired == True:
            self._hitBox.left += self._xMag * (self._projectileSpeed * (elapsedTime / 1000.0))
            self._hitBox.top += self._yMag * (self._projectileSpeed * (elapsedTime / 1000.0))
        
        # updates the homing laser's angle
        self._target[0] = self._targetX - self._hitBox.centerx
        self._target[1] = self._targetY - self._hitBox.centery
        self._targetAngle = math.atan2(self._target[0], self._target[1])
        homingAngleD = math.degrees(self._homingAngle)
        targetAngleD = math.degrees(self._targetAngle)
        '''
        if self._hitBox.centery > self._targetY:
            if (homingAngleD % 360) >= (targetAngleD % 360):
                if ((homingAngleD % 360) >= (targetAngleD % 360)) and ((homingAngleD % 360) <= ((targetAngleD % 360) + 10)):
                    homingAngleD -= 1
                else:
                    homingAngleD -= 15
                
            elif (homingAngleD % 360) < (targetAngleD % 360):
                if ((homingAngleD % 360) < (targetAngleD % 360)) and ((homingAngleD % 360) > ((targetAngleD % 360) - 10)):
                    homingAngleD += 1
                else:
                    homingAngleD += 15
        else:'''
        if (homingAngleD) >= (targetAngleD):
            homingAngleD -= 15
            
        elif (homingAngleD) < (targetAngleD):
            homingAngleD += 15
        
            
        self._homingAngle = math.radians(homingAngleD)
        
        # checks to see if the homing laser has hit its target
        #if ((self._hitBox.centerx < self._targetX + 5) and (self._hitBox.centerx > self._targetX - 5)) and ((self._hitBox.centery < self._targetY + 5) and (self._hitBox.centery > self._targetY - 5)):
        #    self._targetHit = True

    def Draw(self, screen):
        '''draws the projectile'''
        screen.blit(self._homingLaser, self._hitBox.topleft)