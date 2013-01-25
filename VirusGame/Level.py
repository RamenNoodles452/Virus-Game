'''
Created on Sep 11, 2012

@author: Korea
'''

import pygame
import CollisionDetection
import Paused
import Player
import GameState
import Enemies
import EnemyDeathAnimations

class Level:
    '''
    classdocs
    '''
    def __init__(self):
        '''
        Constructor
        '''
        self._animationsList = []
        self._collisionDetection = CollisionDetection.CollisionDetection()
        self._playerStartPosition = [100, 100]
        self._playerCharacter = Player.Player(self._playerStartPosition)
        self._enemies = Enemies.Enemies()
        self._level = pygame.image.load("Content/Level/Walls.png").convert_alpha()
        self._background = pygame.image.load("Content/Level/Background.png").convert_alpha()
        self._levelBitMask = pygame.mask.from_surface(self._level, 127)
        #print self._levelBitMask.get_at((2, 10))
        
        self._gameState = GameState.GameState()
        self._regenTimer = 0
        
        #self._enemies.AddEnemy(200, 200, 'boss')
        #self._enemies.AddEnemy(300, 300, 'antibody')
        #self._enemies.AddEnemy(400, 300, 'bacteria')
        #self._enemies.AddEnemy(400, 300, 'virus')
        #self._enemies.AddEnemy(400, 300, 'tumor')

    def Update(self, elapsedTime, clock):
        '''
        updates everything within the level
        '''
        self._playerCharacter.Update(elapsedTime, clock, self._levelBitMask)
        playerCenterPosition = self._playerCharacter._playerHitBox.center
        self._enemies.Update(playerCenterPosition, clock, elapsedTime)
        
        self.HandleCollisions(elapsedTime, self._levelBitMask)
        self.HandleAcidDamage(elapsedTime)
        self.HandleBombDamage()
        self.HandleEnemyDeath()
        self.HandlePlayerCollisions()
        self.RegenSheilds(elapsedTime)
        self.PlayerDeath()
        
        for i in self._animationsList:
            i.Update(elapsedTime)
        self.AnimationsCleaner()
        
        self._gameState.Update(elapsedTime, self._enemies)
        
    def HandleCollisions(self, elapsedTime, bitMask):
        
        playerBullets = self._playerCharacter._bulletsList
        playerSpray = self._playerCharacter._sprayList
        playerTargeting = self._playerCharacter._targetingLaserList
        playerBomb = self._playerCharacter._bombList
        
        #handles the collisions for the basic bullets
        if len(playerBullets) > 0:
            for p in playerBullets:
                skipRest = False
                for a in self._enemies._antibodyList:
                    if skipRest == False:  
                        if self._collisionDetection.ObjectCollision(p._projectileHitBox, a._hitBox) == True:
                            playerBullets.pop(playerBullets.index(p))
                            a._health -= 1
                            skipRest = True
                            
                if skipRest == False:
                    for v in self._enemies._virusList:
                        if skipRest == False:  
                            if self._collisionDetection.ObjectCollision(p._projectileHitBox, v._hitBox) == True:
                                playerBullets.pop(playerBullets.index(p))
                                v._health -= 1
                                skipRest = True
                                
                if skipRest == False:
                    for t in self._enemies._tumorList:
                        if skipRest == False:
                            if self._collisionDetection.ObjectCollision(p._projectileHitBox, t._hitBox) == True:
                                playerBullets.pop(playerBullets.index(p))
                                t._hit = True
                                t._health -= 1
                                skipRest = True
                                
                if skipRest == False:
                    for x in self._enemies._bossList:
                        if skipRest == False:
                            if self._collisionDetection.ObjectCollision(p._projectileHitBox, x._hitBox) == True:
                                playerBullets.pop(playerBullets.index(p))
                                #x._health -= 2
                                Paused._gameProgress -= 2
                                skipRest = True
                        if skipRest == False:
                            for s in x._bodyList:
                                if skipRest == False: 
                                    if self._collisionDetection.ObjectCollision(p._projectileHitBox, s._hitBox) == True:
                                        playerBullets.pop(playerBullets.index(p))
                                        Paused._gameProgress -= 1
                                        skipRest = True
                        
                if skipRest == False:        
                    for b in self._enemies._bacteriaList:
                        if skipRest == False:
                            for c in b._childBacteriaList:
                                if skipRest == False:  
                                    if self._collisionDetection.ObjectCollision(p._projectileHitBox, c._hitBox) == True:
                                        playerBullets.pop(playerBullets.index(p))
                                        c._health -= 1
                                        skipRest = True
                        if skipRest == False:            
                            if self._collisionDetection.ObjectCollision(p._projectileHitBox, b._hitBox) == True:
                                playerBullets.pop(playerBullets.index(p))
                                b._health -= 1
                                skipRest = True
                                
                if skipRest == False:
                    if self._collisionDetection.GetPixelCollision(bitMask, p._projectileHitBox.centerx , p._projectileHitBox.centery):
                        playerBullets.pop(playerBullets.index(p))
                        skipRest = True
                        
                if skipRest == False:
                    if (p._projectileHitBox.centerx > 2000 or p._projectileHitBox.centerx < - 100) or (p._projectileHitBox.centery > 2000 or p._projectileHitBox.centerx < -10):
                        playerBullets.pop(playerBullets.index(p))

        # Handles the spray collision
        if len(playerSpray) > 0:
            for p in playerSpray:
                for a in self._enemies._antibodyList:
                    if self._collisionDetection.ObjectCollision(p._projectileHitBox, a._hitBox) == True:
                        a._acidBurning = True
                        a._acidTimer = 0.0
                
                for v in self._enemies._virusList:
                    if self._collisionDetection.ObjectCollision(p._projectileHitBox, v._hitBox) == True:
                        v._acidBurning = True
                        v._acidTimer = 0.0
                        
                for t in self._enemies._tumorList:
                    if self._collisionDetection.ObjectCollision(p._projectileHitBox, t._hitBox) == True:
                        t._acidBurning = True
                        t._acidTimer = 0.0
                
                for x in self._enemies._bossList:
                    for s in x._bodyList:
                        if self._collisionDetection.ObjectCollision(p._projectileHitBox, s._hitBox) == True:
                            s._acidBurning = True
                            s._acidTimer = 0.0
                    if self._collisionDetection.ObjectCollision(p._projectileHitBox, x._hitBox) == True:
                        x._acidBurning = True
                        x._acidTimer = 0.0
                
                for b in self._enemies._bacteriaList:
                    for c in b._childBacteriaList:
                        if self._collisionDetection.ObjectCollision(p._projectileHitBox, c._hitBox) == True:
                            c._acidBurning = True
                            c._acidTimer = 0.0
                    if self._collisionDetection.ObjectCollision(p._projectileHitBox, b._hitBox) == True:
                        b._acidBurning = True
                        b._acidTimer = 0.0
                        
                if self._collisionDetection.GetPixelCollision(bitMask, p._projectileHitBox.centerx, p._projectileHitBox.centery):
                    playerSpray.pop(playerSpray.index(p))
                    
        #handles collisions for the targeting laser
        if len(playerTargeting) > 0:
            for p in playerTargeting:
                for a in self._enemies._antibodyList:
                    if self._collisionDetection.ObjectCollision(p._projectileHitBox, a._hitBox) == True:
                        if a._lockedOn == False:
                            a._lockedOn = True
                            if len(self._playerCharacter._homingLaserList) < 12 and Paused._homingAmmo > 6: 
                                Paused._homingAmmo -= 6
                                l = self._playerCharacter.CreateHomingLaser(a._hitBox)
                                self._playerCharacter._homingLaserList.append(l)
                                self._playerCharacter._homingTargetsList.append(a)
                                if self._playerCharacter._laserAngle > 0:
                                    self._playerCharacter._laserAngle += 0.1
                                elif self._playerCharacter._laserAngle < 0:
                                    self._playerCharacter._laserAngle -= 0.1
                                self._playerCharacter._laserAngle *= -1.0
                                
                for v in self._enemies._virusList:
                    if self._collisionDetection.ObjectCollision(p._projectileHitBox, v._hitBox) == True:
                        if v._lockedOn == False:
                            v._lockedOn = True
                            if len(self._playerCharacter._homingLaserList) < 12 and Paused._homingAmmo > 6: 
                                Paused._homingAmmo -= 6
                                l = self._playerCharacter.CreateHomingLaser(v._hitBox)
                                self._playerCharacter._homingLaserList.append(l)
                                self._playerCharacter._homingTargetsList.append(v)
                                if self._playerCharacter._laserAngle > 0:
                                    self._playerCharacter._laserAngle += 0.1
                                elif self._playerCharacter._laserAngle < 0:
                                    self._playerCharacter._laserAngle -= 0.1
                                self._playerCharacter._laserAngle *= -1.0
                                
                for t in self._enemies._tumorList:
                    if self._collisionDetection.ObjectCollision(p._projectileHitBox, t._hitBox):
                        if t._lockedOn == False:
                            t._lockedOn = True
                            if len(self._playerCharacter._homingLaserList) < 12 and Paused._homingAmmo > 6: 
                                Paused._homingAmmo -= 6
                                l = self._playerCharacter.CreateHomingLaser(t._hitBox)
                                self._playerCharacter._homingLaserList.append(l)
                                self._playerCharacter._homingTargetsList.append(t)
                                if self._playerCharacter._laserAngle > 0:
                                    self._playerCharacter._laserAngle += 0.1
                                elif self._playerCharacter._laserAngle < 0:
                                    self._playerCharacter._laserAngle -= 0.1
                                self._playerCharacter._laserAngle *= -1.0
                                
                for x in self._enemies._bossList:
                    if self._collisionDetection.ObjectCollision(p._projectileHitBox, x._hitBox) == True:
                        if x._lockedOn == False:
                            x._lockedOn = True
                            if len(self._playerCharacter._homingLaserList) < 12 and Paused._homingAmmo > 6:
                                Paused._homingAmmo -= 6
                                l = self._playerCharacter.CreateHomingLaser(x._hitBox)
                                self._playerCharacter._homingLaserList.append(l)
                                self._playerCharacter._homingTargetsList.append(x)
                                if self._playerCharacter._laserAngle > 0:
                                    self._playerCharacter._laserAngle += 0.1
                                elif self._playerCharacter._laserAngle < 0:
                                    self._playerCharacter._laserAngle -= 0.1
                                self._playerCharacter._laserAngle *= -1.0
                    for s in x._bodyList:
                        if self._collisionDetection.ObjectCollision(p._projectileHitBox, s._hitBox) == True:
                            if s._lockedOn == False:
                                s._lockedOn = True
                                if len(self._playerCharacter._homingLaserList) < 12 and Paused._homingAmmo > 6:
                                    Paused._homingAmmo -= 6
                                    l = self._playerCharacter.CreateHomingLaser(s._hitBox)
                                    self._playerCharacter._homingLaserList.append(l)
                                    self._playerCharacter._homingTargetsList.append(s)
                                    if self._playerCharacter._laserAngle > 0:
                                        self._playerCharacter._laserAngle += 0.1
                                    elif self._playerCharacter._laserAngle < 0:
                                        self._playerCharacter._laserAngle -= 0.1
                                    self._playerCharacter._laserAngle *= -1.0
                       
                for b in self._enemies._bacteriaList:
                    if self._collisionDetection.ObjectCollision(p._projectileHitBox, b._hitBox) == True:
                        if b._lockedOn == False:
                            b._lockedOn = True
                            if len(self._playerCharacter._homingLaserList) < 12 and Paused._homingAmmo > 6:
                                Paused._homingAmmo -= 6
                                l = self._playerCharacter.CreateHomingLaser(b._hitBox)
                                self._playerCharacter._homingLaserList.append(l)
                                self._playerCharacter._homingTargetsList.append(b)
                                if self._playerCharacter._laserAngle > 0:
                                    self._playerCharacter._laserAngle += 0.1
                                elif self._playerCharacter._laserAngle < 0:
                                    self._playerCharacter._laserAngle -= 0.1
                                self._playerCharacter._laserAngle *= -1.0
                    for c in b._childBacteriaList:
                        if self._collisionDetection.ObjectCollision(p._projectileHitBox, c._hitBox) == True:
                            if c._lockedOn == False:
                                c._lockedOn = True
                                if len(self._playerCharacter._homingLaserList) < 12 and Paused._homingAmmo > 6:
                                    Paused._homingAmmo -= 6
                                    l = self._playerCharacter.CreateHomingLaser(c._hitBox)
                                    self._playerCharacter._homingLaserList.append(l)
                                    self._playerCharacter._homingTargetsList.append(c)
                                    if self._playerCharacter._laserAngle > 0:
                                        self._playerCharacter._laserAngle += 0.1
                                    elif self._playerCharacter._laserAngle < 0:
                                        self._playerCharacter._laserAngle -= 0.1
                                    self._playerCharacter._laserAngle *= -1.0
                            
                if (p._projectileHitBox.centerx > 2000 or p._projectileHitBox.centerx < - 500) or (p._projectileHitBox.centery > 2000 or p._projectileHitBox.centerx < -500):
                    playerTargeting.pop(playerTargeting.index(p))
        
        #handles collision for bomb
        for p in playerBomb:
            p.Update(elapsedTime, bitMask)
            
        #when not firing, you're not locked onto anything
        if self._playerCharacter._laserState == False:
            for a in self._enemies._antibodyList:
                a._lockedOn = False
            for v in self._enemies._virusList:
                v._lockedOn = False    
            for t in self._enemies._tumorList:
                t._lockedOn = False
            for x in self._enemies._bossList:
                x._lockedOn = False
                for s in x._bodyList:
                    s._lockedOn = False
            for b in self._enemies._bacteriaList:
                b._lockedOn = False
                for c in b._childBacteriaList:
                    c._lockedOn = False
            
    def HandleAcidDamage(self, elapsedTime):
        for a in self._enemies._antibodyList:
            if a._acidBurning == True:
                damageTick = elapsedTime
                a._acidTimer += damageTick
                a._acidDamageTimer += damageTick
                if a._acidDamageTimer > 120:
                    a._acidDamageTimer = 0.0
                    a._health -= 1
                if a._acidTimer > 360:
                    a._acidBurning = False
                    
        for v in self._enemies._virusList:
            if v._acidBurning == True:
                damageTick = elapsedTime
                v._acidTimer += damageTick
                v._acidDamageTimer += damageTick
                if v._acidDamageTimer > 120:
                    v._acidDamageTimer = 0.0
                    v._health -= 1
                if v._acidTimer > 360:
                    v._acidBurning = False
        
        for t in self._enemies._tumorList:
            if t._acidBurning == True:
                damageTick = elapsedTime
                t._acidTimer += damageTick
                t._acidDamageTimer += damageTick
                if t._acidDamageTimer > 120:
                    t._acidDamageTimer = 0.0
                    t._health -= 1
                    t._hit = True
                if t._acidTimer > 360:
                    t._acidBurning = False
                    
        for x in self._enemies._bossList:
            if x._acidBurning == True:
                damageTick = elapsedTime
                x._acidTimer += damageTick
                x._acidDamageTimer += damageTick
                if x._acidDamageTimer > 360:
                    x._acidDamageTimer = 0.0
                    #x._health -= 1
                    Paused._gameProgress -= 1
                if x._acidTimer > 720:
                    x._acidBurning = False
            for s in x._bodyList:
                if s._acidBurning == True:
                    damageTick = elapsedTime
                    s._acidTimer += damageTick
                    s._acidDamageTimer += damageTick
                    if s._acidDamageTimer > 360:
                        s._acidDamageTimer = 0.0
                        #s._health -= 1
                        Paused._gameProgress -= 1
                    if s._acidTimer > 720:
                        s._acidBurning = False
                    
        for b in self._enemies._bacteriaList:
            if b._acidBurning == True:
                damageTick = elapsedTime
                b._acidTimer += damageTick
                b._acidDamageTimer += damageTick
                if b._acidDamageTimer > 120:
                    b._acidDamageTimer = 0.0
                    b._health -= 1
                if b._acidTimer > 360:
                    b._acidBurning = False
            for c in b._childBacteriaList:
                if c._acidBurning == True:
                    damageTick = elapsedTime
                    c._acidTimer += damageTick
                    c._acidDamageTimer += damageTick
                    if c._acidDamageTimer > 120:
                        c._acidDamageTimer = 0.0
                        c._health -= 1
                    if c._acidTimer > 360:
                        c._acidBurning = False
    
    def HandleBombDamage(self):
        for m in self._playerCharacter._bombList: 
            if m._explode == True:
                for a in self._enemies._antibodyList:
                    if m._explodeState == 3 and self._collisionDetection.ObjectCollision(m._explosionsHitBox, a._hitBox) == True:
                        a._health -= 10
                for t in self._enemies._tumorList:
                    if self._collisionDetection.ObjectCollision(m._explosionsHitBox, t._hitBox) == True:
                        t._health -= 10
                        t._hit = True
                for v in self._enemies._virusList:
                    if m._explodeState == 3 and self._collisionDetection.ObjectCollision(m._explosionsHitBox, v._hitBox) == True:
                        v._health -= 10
                for b in self._enemies._bacteriaList:
                    if m._explodeState == 3 and self._collisionDetection.ObjectCollision(m._explosionsHitBox, b._hitBox) == True:
                        b._health -= 10
                    for c in b._childBacteriaList:
                        if m._explodeState == 3 and self._collisionDetection.ObjectCollision(m._explosionsHitBox, c._hitBox) == True:
                            c._health -= 10
                for x in self._enemies._bossList:
                    if m._explodeState == 3 and self._collisionDetection.ObjectCollision(m._explosionsHitBox, x._hitBox) == True:
                        #x._health -= 10
                        Paused._gameProgress -= 2
                    for s in x._bodyList:
                        if m._explodeState == 3 and self._collisionDetection.ObjectCollision(m._explosionsHitBox, s._hitBox) == True:
                            #s._health -= 1
                            Paused._gameProgress -= 1
                         
    def HandleEnemyDeath(self):
        for a in self._enemies._antibodyList:
            if a._health <= 0:
                tempchild = EnemyDeathAnimations.EnemyDeathAnimations(a._hitBox.center, 1)
                self._animationsList.append(tempchild)
                self._enemies._antibodyList.pop(self._enemies._antibodyList.index(a))
                
        for v in self._enemies._virusList:
            if v._health <= 0:
                tempchild = EnemyDeathAnimations.EnemyDeathAnimations(v._hitBox.center, 4)
                self._animationsList.append(tempchild)
                self._enemies._virusList.pop(self._enemies._virusList.index(v))
                
        for t in self._enemies._tumorList:
            if t._health <= 0:
                tempchild = EnemyDeathAnimations.EnemyDeathAnimations(t._hitBox.center, 5)
                self._animationsList.append(tempchild)
                self._enemies._tumorList.pop(self._enemies._tumorList.index(t))
                Paused._gameProgress -= 5
        
        if Paused._bossspawn == 1 and Paused._gameProgress <= 0:
            for x in self._enemies._bossList:
                self._enemies._bossList.pop(self._enemies._bossList.index(x))
            Paused._PauseState = 3
        
        for b in self._enemies._bacteriaList:
            if b._health <= 0:
                tempchild = EnemyDeathAnimations.EnemyDeathAnimations(b._hitBox.center, 2)
                self._animationsList.append(tempchild)
                self._enemies._bacteriaList.pop(self._enemies._bacteriaList.index(b))
            for c in b._childBacteriaList:
                if c._health <= 0:
                    tempchild = EnemyDeathAnimations.EnemyDeathAnimations(c._hitBox.center, 3)
                    self._animationsList.append(tempchild)
                    b._childBacteriaList.pop(b._childBacteriaList.index(c))
                    
    def AnimationsCleaner(self):
        for i in self._animationsList:
            if i._finished == True:
                self._animationsList.pop(self._animationsList.index(i))
                    
    def HandlePlayerCollisions(self):
        for a in self._enemies._antibodyList:
            if self._collisionDetection.ObjectCollision(a._hitBox, self._playerCharacter._playerHitBox):
                Paused._playerHealth -= 5
                self._enemies._antibodyList.pop(self._enemies._antibodyList.index(a))
        
        for j in self._enemies._dnaList:
            if self._collisionDetection.ObjectCollision(j._projectileHitBox, self._playerCharacter._playerHitBox):
                Paused._playerHealth -= 5
                self._enemies._dnaList.pop(self._enemies._dnaList.index(j))
                
        for z in self._enemies._bossList:
            for q in z._bossProjectileList:
                if self._collisionDetection.ObjectCollision(q._projectileHitBox, self._playerCharacter._playerHitBox):
                    Paused._playerHealth -= 10
                    z._bossProjectileList.pop(z._bossProjectileList.index(q))
                
        for b in self._enemies._bacteriaList:
            for c in b._childBacteriaList:
                if self._collisionDetection.ObjectCollision(c._hitBox, self._playerCharacter._playerHitBox):
                    Paused._playerHealth -= 2
                    b._childBacteriaList.pop(b._childBacteriaList.index(c))
            if self._collisionDetection.ObjectCollision(b._hitBox, self._playerCharacter._playerHitBox):
                Paused._playerHealth -= 0.1
                
        for z in self._enemies._bossList:
            for q in z._bodyList:
                if self._collisionDetection.ObjectCollision(q._hitBox, self._playerCharacter._playerHitBox):
                    Paused._playerHealth -= 0.1
            if self._collisionDetection.ObjectCollision(z._hitBox, self._playerCharacter._playerHitBox):
                Paused._playerHealth -= 0.1
    
    def RegenSheilds(self, elapsedTime):
        regenTick = elapsedTime
        self._regenTimer += regenTick
        if self._regenTimer > 2000:
            self._regenTimer = 0.0
            Paused._playerHealth += 1

    def PlayerDeath(self):
        if Paused._playerHealth <= 0:
            Paused._PauseState = 4

    def Draw(self, screen):
        screen.blit(self._background, (0, 0))
        screen.blit(self._level, (0, 0))
        self._enemies.Draw(screen)
        if self._playerCharacter._drawHomingLasers == True:
            for l in self._playerCharacter._homingLaserList:
                l.Draw(screen)
                
        self._playerCharacter.Draw(screen)
        for b in self._playerCharacter._bulletsList:
            b.Draw(screen)
            
        for b in self._playerCharacter._targetingLaserList:
            b.Draw(screen)    
            
        for b in self._playerCharacter._bombList:
            b.Draw(screen)
        
        for b in self._playerCharacter._sprayList:
            b.Draw(screen)
            
        for b in self._animationsList:
            b.Draw(screen)
            