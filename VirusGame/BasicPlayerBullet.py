'''
Created on Sep 10, 2012

@author: Korea
'''
import pygame
import math

class BasicPlayerBullet:
    '''
    classdocs
    '''
    def __init__(self, projectileAngle, projectileStartPositionX, projectileStartPositionY):
        '''
        constructor
        '''
        self._projectileSprite = pygame.image.load("Content/Player/Bullet.png").convert_alpha()
        self._rotatedProjectile = self._projectileSprite
        self._projectileHitBox = self._rotatedProjectile.get_rect()
        self._projectileSpeed = 800.0
        self._projectileAngle = projectileAngle
        self._projectileHitBox.center = [projectileStartPositionX, projectileStartPositionY]
        
        #calculates the initial x and y magnitudes of the projectile
        self._xMag = 1 * math.sin(self._projectileAngle)
        self._yMag = 1 * math.cos(self._projectileAngle)
        self._rotatedProjectile = self.RotateCenter(self._projectileSprite, math.degrees(self._projectileAngle))
        
    def Update(self, elapsedTime):
        '''this handles how bullets move'''
        self._projectileHitBox.left += self._xMag * (self._projectileSpeed * (elapsedTime / 1000.0))
        self._projectileHitBox.top += self._yMag * (self._projectileSpeed * (elapsedTime / 1000.0))
        
        #self._projectilePosition[0] += self._xMag * self._projectileSpeed
        #self._projectilePosition[1] += self._yMag * self._projectileSpeed
        
    def RotateCenter(self, objectToRotate, rotationAngle):
        '''rorate an image while keeping its center and size'''
        orig_rect = objectToRotate.get_rect()
        rot_image = pygame.transform.rotate(objectToRotate, rotationAngle)
        rot_rect = orig_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy()
        return rot_image
            
    def Draw(self, screen):
        '''draws the projectile'''
        screen.blit(self._rotatedProjectile, self._projectileHitBox.topleft)
        #self._screen.set_at(self._projectileHitBox.midtop, (0,255,255))
        #self._screen.set_at(self._projectileHitBox.midleft, (0,255,255))
        #self._screen.set_at(self._projectileHitBox.midright, (0,255,255))
        #self._screen.set_at(self._projectileHitBox.midbottom, (0,255,255))
        