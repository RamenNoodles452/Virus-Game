#Nicholas Cesare (9/12/12)
#This game is sick
#DNA Projectile
#Fired from the Virus and towards the player

import pygame
import math

class DnaProjectile:
    '''
    classdocs
    '''
    def __init__(self, projectileAngle, projectileStartPositionX, projectileStartPositionY):
        '''
        constructor
        '''
        self._projectileSprite = pygame.image.load("Content/Enemy/DNA1.png").convert_alpha()
        self._projectileSprite2 = pygame.image.load("Content/Enemy/DNA2.png").convert_alpha()
        
        self._rotatedProjectile = self._projectileSprite
        self._projectileHitBox = self._rotatedProjectile.get_rect()
        self._projectileSpeed = 7
        self._projectileAngle = projectileAngle
        self._projectileHitBox.topleft = [projectileStartPositionX, projectileStartPositionY]
        
        #calculates the initial x and y magnitudes of the projectile
        self._xMag = 1 * math.sin(self._projectileAngle)
        self._yMag = 1 * math.cos(self._projectileAngle)
        self._rotatedProjectile = self.RotateCenter(self._projectileSprite, math.degrees(self._projectileAngle))
        self._timePassed = 0
        
    def Update(self, _elapsedTime):
        
        #calculates the initial x and y magnitudes of the projectile
        self._xMag = 1 * math.sin(self._projectileAngle)
        self._yMag = 1 * math.cos(self._projectileAngle)
        
        
        '''handles dna projectile animation'''
        recent_time = _elapsedTime
        self._timePassed += recent_time
        if self._timePassed > 100:
            self._rotatedProjectile = self.RotateCenter(self._projectileSprite2, math.degrees(self._projectileAngle))
        if self._timePassed > 200:
            self._rotatedProjectile = self.RotateCenter(self._projectileSprite, math.degrees(self._projectileAngle))
            self._timePassed = 0
        
        '''this handles how bullets move'''
        self._projectileHitBox.left += self._xMag * self._projectileSpeed
        self._projectileHitBox.top += self._yMag * self._projectileSpeed
        
    def RotateCenter(self, objectToRotate, rotationAngle):
        '''rotate an image while keeping its center and size'''
        orig_rect = objectToRotate.get_rect()
        rot_image = pygame.transform.rotate(objectToRotate, rotationAngle)
        rot_rect = orig_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy()
        return rot_image
            
    def Draw(self, screen):
        '''draws the projectile'''
        screen.blit(self._rotatedProjectile, self._projectileHitBox.topleft)