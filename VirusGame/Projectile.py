import pygame
import sys
import math

class Projectile:
    def __init__(self, projectileSprite, screen, projectileSpeed, projectileAngle, projectileStartPositionX, projectileStartPositionY, projectileType):
        '''
        constructor
        '''
        self._projectileSprite = pygame.image.load(projectileSprite).convert_alpha()
        self._screen = screen
        self._rotatedProjectile = self._projectileSprite
        self._projectileHitBox = self._rotatedProjectile.get_rect()
        self._projectileSpeed = projectileSpeed
        self._projectileAngle = projectileAngle
        self._projectilePosition = [projectileStartPositionX, projectileStartPositionY]
        # the projectile types are "bullet", "bounce", "homing", "spray"
        self._projectileType = projectileType
        
        #calculates the initial x and y magnitudes of the projectile
        if self._projectileType != 'homing':
            self._xMag = 1 * math.sin(self._projectileAngle)
            self._yMag = 1 * math.cos(self._projectileAngle)
            self._rotatedProjectile = self.RotateCenter(self._projectileSprite, self._projectileAngle)
            
    def Update(self):
        if self._projectileType == 'bullet':
            self.UpdateBullet()
        if self._projectileType == 'bounce':
            self.UpdateBounce()
        if self._projectileType == 'homing':
            self.UpdateHoming()
        if self._projectileType == 'spray':
            self.UpdateSpray()
            
    def RotateCenter(self, objectToRotate, rotationAngle):
        '''rorate an image while keeping its center and size'''
        orig_rect = objectToRotate.get_rect()
        rot_image = pygame.transform.rotate(objectToRotate, rotationAngle)
        rot_rect = orig_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy()
        return rot_image
            
    def UpdateBullet(self):
        '''this handles how bullets move'''
        self._projectilePosition[0] += self._xMag * self._projectileSpeed
        self._projectilePosition[1] += self._yMag * self._projectileSpeed
        
        
    def UpdateBounce(self):
        '''this handles how bouncers move'''
    
    def UpdateHoming(self):
        '''this handles how homing bullets move'''
        #is is going to require a parameter called "TargetPosition" where the homing bullet is going to
        
    def UpdateSpray(self):
        '''this handles how spray attacks work'''
    
    def Draw(self):
        '''draws the projectile'''
        self._screen.blit(self._rotatedProjectile, self._projectilePosition)