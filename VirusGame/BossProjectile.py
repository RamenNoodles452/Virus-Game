#Nicholas Cesare (9/18/12)
#This game is sick
#Boss Projectile
#Fired from the Boss' head and towards the player

import pygame
import math

class BossProjectile:
    '''
    classdocs
    '''
    def __init__(self, projectileAngle, projectileStartPositionX, projectileStartPositionY):
        '''
        constructor
        '''
        self._projectileSprite = pygame.image.load("Content/Enemy/bosslaser.png").convert_alpha()
        self._rotatedProjectile = self._projectileSprite
        self._projectileHitBox = self._rotatedProjectile.get_rect()
        self._projectileSpeed = 4
        self._projectileAngle = projectileAngle
        self._projectileHitBox.center = [projectileStartPositionX, projectileStartPositionY]
        
        #calculates the initial x and y magnitudes of the projectile
        self._xMag = 1 * math.sin(self._projectileAngle)
        self._yMag = 1 * math.cos(self._projectileAngle)
        self._rotatedProjectile = self.RotateCenter(self._projectileSprite, math.degrees(self._projectileAngle))
        
    def RotateCenter(self, objectToRotate, rotationAngle):
        #rotate an image while keeping its center and size
        orig_rect = objectToRotate.get_rect()
        rot_image = pygame.transform.rotate(objectToRotate, rotationAngle)
        rot_rect = orig_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy()
        return rot_image
        
    def Update(self):
        '''this handles how bullets move'''
        self._projectileHitBox.left += self._xMag * self._projectileSpeed
        self._projectileHitBox.top += self._yMag * self._projectileSpeed
            
    def Draw(self, screen):
        '''draws the projectile'''
        screen.blit(self._rotatedProjectile, self._projectileHitBox.topleft)
        