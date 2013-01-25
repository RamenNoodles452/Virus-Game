'''
Created on Sep 17, 2012

@author: Korea
'''

import math
import pygame
import CollisionDetection
import operator

class Bomb:
    '''
    classdocs
    '''
    def __init__(self, projectileAngle, projectileStartPositionX, projectileStartPositionY):
        '''
        Constructor
        '''
        self._projectileSprite = pygame.image.load("Content/Player/Bomb.png").convert_alpha()
        self._explosion1 = pygame.image.load("Content/Player/Explosion/explosion1.png").convert_alpha()
        self._explosion2 = pygame.image.load("Content/Player/Explosion/explosion2.png").convert_alpha()
        self._explosion3 = pygame.image.load("Content/Player/Explosion/explosion3.png").convert_alpha()
        self._explosion4 = pygame.image.load("Content/Player/Explosion/explosion4.png").convert_alpha()
        self._explosion5 = pygame.image.load("Content/Player/Explosion/explosion5.png").convert_alpha()
        self._explosion6 = pygame.image.load("Content/Player/Explosion/explosion6.png").convert_alpha()
        self._explosion7 = pygame.image.load("Content/Player/Explosion/explosion7.png").convert_alpha()
        self._explosion8 = pygame.image.load("Content/Player/Explosion/explosion8.png").convert_alpha()
        self._explosion9 = pygame.image.load("Content/Player/Explosion/explosion9.png").convert_alpha()
        
        self._explosionsHitBox = self._explosion1.get_rect()
        self._rotatedProjectile = self._projectileSprite
        self._projectileHitBox = self._rotatedProjectile.get_rect()
        self._projectileSpeed = 300.0
        self._projectileSlowDown = 1.0
        self._projectileSpeedMin = 150.0
        self._projectileAngle = projectileAngle
        self._projectileHitBox.center = [projectileStartPositionX, projectileStartPositionY]
        self._collisions = CollisionDetection.CollisionDetection()
        self._clock = pygame.time.Clock()
        
        self._explode = False
        self._explodeState = 0
        self._explosionTimer = 0
        self._explosionFinished = False
        
        #calculates the initial x and y magnitudes of the projectile
        self._xMag = 1 * math.sin(self._projectileAngle)
        self._yMag = 1 * math.cos(self._projectileAngle)
        self._rotatedProjectile = self.RotateCenter(self._projectileSprite, math.degrees(self._projectileAngle))
        
    def Update(self, elapsedTime, bitMask):
        
        #updates the speed
        if self._explode == False:
            if self._projectileSpeed > 100:
                self._projectileSpeed -= 1.5
            elif self._projectileSpeed > 0:
                self._projectileSpeed -= 0.5
            else:
                self._projectileSpeed = 0
        elif self._explode == True:
            self._projectileSpeed = 0
        
        self.xSpeed = self._xMag * self._projectileSpeed
        self.ySpeed = self._yMag * self._projectileSpeed
        
        self._projectileHitBox = self._collisions.CollisionMovement(self._projectileHitBox, bitMask, self.xSpeed, self.ySpeed, elapsedTime)
        
        #print self._collisions._collidedHorizontal, self._collisions._collidedVertical
        
        if self._collisions._collidedHorizontal == True:
            self._xMag = -self._xMag
            self._collisions._collidedHorizontal = False
            
        if self._collisions._collidedVertical == True:
            self._yMag = -self._yMag
            self._collisions._collidedVertical = False
            
        self._explosionsHitBox.center = self._projectileHitBox.center
        if self._explode == True:
            self.ExplosionAnimation(elapsedTime)

         
    def RotateCenter(self, objectToRotate, rotationAngle):
        '''rorate an image while keeping its center and size'''
        orig_rect = objectToRotate.get_rect()
        rot_image = pygame.transform.rotate(objectToRotate, rotationAngle)
        rot_rect = orig_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy()
        return rot_image
    
    def ExplosionAnimation(self, elapsedTime):
        explosionTimer = elapsedTime
        self._explosionTimer += explosionTimer
        if self._explosionTimer > 20:
            self._explodeState += 1
            self._explosionTimer = 0
        if self._explodeState == 10:
            self._explosionFinished = True
        
    def Draw(self, screen):
        '''draws the projectile'''
        if self._explodeState == 0:
            screen.blit(self._rotatedProjectile, self._projectileHitBox.topleft)
        elif self._explodeState == 1:
            screen.blit(self._explosion1, self._explosionsHitBox.topleft)
        elif self._explodeState == 2:
            screen.blit(self._explosion2, self._explosionsHitBox.topleft)
        elif self._explodeState == 3:
            screen.blit(self._explosion3, self._explosionsHitBox.topleft)
        elif self._explodeState == 4:
            screen.blit(self._explosion4, self._explosionsHitBox.topleft)
        elif self._explodeState == 5:
            screen.blit(self._explosion5, self._explosionsHitBox.topleft)
        elif self._explodeState == 6:
            screen.blit(self._explosion6, self._explosionsHitBox.topleft)
        elif self._explodeState == 7:
            screen.blit(self._explosion7, self._explosionsHitBox.topleft)
        elif self._explodeState == 8:
            screen.blit(self._explosion8, self._explosionsHitBox.topleft)
        elif self._explodeState == 9:
            screen.blit(self._explosion9, self._explosionsHitBox.topleft)
        #self._screen.set_at(self._projectileHitBox.midtop, (0,255,255))
        #self._screen.set_at(self._projectileHitBox.midleft, (0,255,255))
        #self._screen.set_at(self._projectileHitBox.midright, (0,255,255))
        #self._screen.set_at(self._projectileHitBox.midbottom, (0,255,255))