'''
Created on Sep 15, 2012

@author: Korea
'''
import pygame
import math

class AcidBullet:
    '''
    classdocs
    '''
    def __init__(self, projectileAngle, projectileStartPositionX, projectileStartPositionY):
        '''
        constructor
        '''
        self._projectileSprite1 = pygame.image.load("Content/Player/Acid/acid1.png").convert_alpha()
        self._projectileSprite2 = pygame.image.load("Content/Player/Acid/acid2.png").convert_alpha()
        self._projectileSprite3 = pygame.image.load("Content/Player/Acid/acid3.png").convert_alpha()
        self._projectileSprite4 = pygame.image.load("Content/Player/Acid/acid4.png").convert_alpha()
        self._projectileSprite5 = pygame.image.load("Content/Player/Acid/acid5.png").convert_alpha()
        self._projectileSprite6 = pygame.image.load("Content/Player/Acid/acid6.png").convert_alpha()
        self._projectileSprite7 = pygame.image.load("Content/Player/Acid/acid7.png").convert_alpha()

        self._bulletTimer = 0
        self._isActive = True
        self._rotatedProjectile = self._projectileSprite1
        self._projectileHitBox = self._rotatedProjectile.get_rect()
        self._projectileSpeed = 800.0
        self._projectileAngle = projectileAngle
        self._projectileHitBox.center = [projectileStartPositionX, projectileStartPositionY]
        
        #calculates the initial x and y magnitudes of the projectile
        self._xMag = 1 * math.sin(self._projectileAngle)
        self._yMag = 1 * math.cos(self._projectileAngle)
        self._rotatedProjectile = self.RotateCenter(self._projectileSprite1, math.degrees(self._projectileAngle))
        
    def Update(self, elapsedTime):
        '''this handles how bullets move'''
        recentTime = elapsedTime
        self._bulletTimer += recentTime
        if self._bulletTimer > 200:
            self._isActive = False
        
        self._projectileHitBox.left += self._xMag * (self._projectileSpeed * (elapsedTime / 1000.0))
        self._projectileHitBox.top += self._yMag * (self._projectileSpeed * (elapsedTime / 1000.0))
        
        
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