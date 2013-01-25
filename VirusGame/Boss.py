#Nicholas Cesare (9/16/12)
#This game is sick
#Boss Enemy AI
#Bounces off walls and the head shoots at the player
   
import pygame
import sys
import math
import Boss_Body
import BossProjectile

class Boss:
    def __init__(self, spawnX, spawnY):
        self.img = pygame.image.load("Content/Enemy/boss_H.png")
        self._reticule = pygame.image.load("Content/LockOn.png")
        self._hitBox = self.img.get_rect()
        self._hitBox.topleft = (spawnX, spawnY)
        self.x = self._hitBox.centerx
        self.y = self._hitBox.centery
        self._playerPosition = 0
        self.vel_x = 7
        self.vel_y = 6
        self._rotatedImage = self.img
        self._bodyList = []
        
        #angle between boss head and player, used to fire projectiles
        self._angleToPlayer = 0 
        self._getAngleToPlayer = [0, 0]
        
         #variables used to find the distance the boss head is from the player
        self._distancePlayer = 0    #distance the boss head is from the player.  Will be calculated in the update loop
        self._xDistanceSquared = 0
        self._yDistanceSquared = 0
        
        #variables used to handle boss projectiles
        self._time = 0
        self.time_passed = 0
        self.recent_time = 0
        self._bossProjectileList = []
        
        #variables used to find proper orientation of images
        self._rotatedImage = self.img
        self._getAngle = [0, 0]
        self._angle = 0
        
        #creates the boss body
        self._bodyLength = 10  #change this number to change the length of the body
        for i in range(1, self._bodyLength):
            #the following if then statement distinguishes between the body and tail, and passes a 0 or 1
            if i != self._bodyLength - 1:
                tempchild = Boss_Body.Boss_Body(self._hitBox.centerx - (i*100 + 40), self._hitBox.centery - (i*100 + 40), i, 0)
            else:
                tempchild = Boss_Body.Boss_Body(self._hitBox.centerx - (i*100 + 40), self._hitBox.centery - (i*100 + 40), i, 1)
            self._bodyList.append(tempchild)
            
        #health and damage stats
        self._bossType = 'head'
        self._lockedOn = False
        self._acidBurning = False
        self._acidTimer = 0.0
        self._acidDamageTimer = 0.0
        self._health = 10
        
    def Update(self, _playerPosition, elapsedTime):
        future__hitBox = self._hitBox.move(self.vel_x, self.vel_y)
        self._playerPosition = _playerPosition
    
        '''find the angle between the virus and future _hitBox, as to fix orientation'''
        self._getAngle[0] = future__hitBox.centerx - self.x
        self._getAngle[1] = future__hitBox.centery - self.y
        self._angle = math.atan2(self._getAngle[0] , self._getAngle[1])
        #print math.degrees(self._angle)
        self._rotatedImage = self.RotateCenter(self.img, math.degrees(self._angle))
        
        '''updates boss position'''
        if future__hitBox.left < 0 or future__hitBox.right > 1280:
            self.vel_x = -self.vel_x
        if future__hitBox.top < 0 or future__hitBox.bottom > 720:
            self.vel_y = -self.vel_y
        self._hitBox.move_ip(self.vel_x, self.vel_y)
        
        self.x = self._hitBox.centerx
        self.y = self._hitBox.centery
        
        '''update boss body'''
        for i in self._bodyList:
            i.Update(self._hitBox.center)
        
        '''find the angle between the antibody and player, as to fix orientation'''
        self._getAngleToPlayer[0] = self._playerPosition[0] - self.x
        self._getAngleToPlayer[1] = self._playerPosition[1] - self.y
        self._angleToPlayer = math.atan2(self._getAngleToPlayer[0] , self._getAngleToPlayer[1])
        
        #update the boss projectiles
        self.HandleBossProjectile(elapsedTime, self._distancePlayer)
        
    def RotateCenter(self, objectToRotate, rotationAngle):
        '''rorate an image while keeping its center and size'''
        orig_rect = objectToRotate.get_rect()
        rot_image = pygame.transform.rotate(objectToRotate, rotationAngle)
        rot_rect = orig_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy()
        return rot_image
        
    def HandleBossProjectile(self, elapsedTime, distancePlayer):
        self.recent_time = elapsedTime
        self.time_passed  += self.recent_time
        if self.time_passed > 500:  #keeps track of the time so you can spawn another Boss Projectile.
            self.time_passed = 0
            #print "New Boss Projectile created."
            tempchild = BossProjectile.BossProjectile(self._angleToPlayer, self._hitBox.centerx, self._hitBox.centery)
            self._bossProjectileList.append(tempchild)
        
        for i in self._bossProjectileList:
            i.Update()
    
    def Draw(self, screen):
        '''draws boss to screen'''
        screen.blit(self._rotatedImage, self._hitBox.topleft)
        for e in self._bodyList:
            e.Draw(screen)
        for f in self._bossProjectileList:
            f.Draw(screen)
        
        if self._lockedOn == True:
            screen.blit(self._reticule, (self._hitBox.centerx - 20, self._hitBox.centery - 20))