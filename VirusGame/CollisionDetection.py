'''
Created on Sep 10, 2012

@author: Korea
'''

import pygame


class CollisionDetection:
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self._collidedHorizontal = False
        self._collidedVertical = False
        
    def ObjectCollision(self, hitbox1, hitbox2):
        '''
        returns true if two objects have collided
        '''
        if hitbox1.colliderect(hitbox2):
            return True
        else:
            return False
        
    def CollisionMovement(self, objectHitBox, bitMask, xSpeed, ySpeed, elapsedTime):
        self.objectHitBox = objectHitBox
        
        self.StepHorizontal(bitMask, xSpeed, elapsedTime)
        self.StepVertical(bitMask, ySpeed, elapsedTime)
        
        #print self.objectHitBox.topleft
        return self.objectHitBox
        
    
    def StepHorizontal(self, bitMask, xSpeed, elapsedTime):
        '''
        handles horizontal collision calculation
        moves the player as far horizontally as it can move, or up to the wall
        '''
        elapsed = elapsedTime
        
        if xSpeed > 0.0:
            x = self.objectHitBox.right
            xBuffer = x + 6
            
            topPixel = self.objectHitBox.top
            botPixel = self.objectHitBox.bottom
            foundCollision = False
            while(foundCollision == False):
                for y in range(topPixel, botPixel):
                    collision = self.GetPixelCollision(bitMask, x, y)
                    if collision == True:
                        distanceToObject = x - self.objectHitBox.right
                        self.objectHitBox.left += min([(xSpeed * (elapsed / 1000.0)), distanceToObject])
                        if distanceToObject <= 1 and self._collidedHorizontal == False:
                            self._collidedHorizontal = True
                        foundCollision = True
                        break 
                    elif x == xBuffer:
                        self.objectHitBox.left += (xSpeed * (elapsed / 1000.0))
                        foundCollision = True
                        break
                x = x + 1
                
        elif xSpeed < 0.0:
            x = self.objectHitBox.left
            xBuffer = x - 6
            
            topPixel = self.objectHitBox.top
            botPixel = self.objectHitBox.bottom
            foundCollision = False
            while(foundCollision == False):
                for y in range(topPixel, botPixel):
                    collision = self.GetPixelCollision(bitMask, x, y)
                    if collision == True:
                        distanceToObject = self.objectHitBox.left - x - 1
                        self.objectHitBox.left -= min([(-xSpeed * (elapsed / 1000.0)), distanceToObject])
                        if distanceToObject <= 1 and self._collidedHorizontal == False:
                            self._collidedHorizontal = True
                        foundCollision = True
                        break
                    elif x == xBuffer:
                        self.objectHitBox.left -= (-xSpeed * (elapsed / 1000.0))
                        foundCollision = True
                        break
                x = x - 1            
                         
    def StepVertical(self, bitMask, ySpeed, elapsedTime):
        '''
        handles vertical collision calculation
        moves the player as far vertically as it can move, or up to the wall
        '''
        elapsed = elapsedTime
        
        if ySpeed > 0.0:
            y = self.objectHitBox.bottom
            yBuffer = y + 6
            
            leftPixel = self.objectHitBox.left
            rightPixel = self.objectHitBox.right
            foundCollision = False
            while(foundCollision == False):
                for x in range(leftPixel, rightPixel):
                    collision = self.GetPixelCollision(bitMask, x, y)
                    if collision == True:
                        distanceToObject = y - self.objectHitBox.bottom
                        self.objectHitBox.top += min([(ySpeed * (elapsed / 1000.0)), distanceToObject])
                        if distanceToObject <= 1 and self._collidedVertical == False:
                            self._collidedVertical = True
                        foundCollision = True
                        break
                    elif y == yBuffer:
                        self.objectHitBox.top += (ySpeed * (elapsed / 1000.0))
                        foundCollision = True
                        break
                    
                y = y + 1
                
        elif ySpeed < 0.0:
            y = self.objectHitBox.top
            yBuffer = y - 6
            
            leftPixel = self.objectHitBox.left
            rightPixel = self.objectHitBox.right
            foundCollision = False
            while(foundCollision == False):
                for x in range(leftPixel, rightPixel):
                    collision = self.GetPixelCollision(bitMask, x, y)
                    if collision == True:
                        distanceToObject = self.objectHitBox.top - y - 1
                        self.objectHitBox.top -= min([(-ySpeed * (elapsed / 1000.0)), distanceToObject])
                        if distanceToObject <= 1 and self._collidedVertical == False:
                            self._collidedVertical = True
                        foundCollision = True
                        break
                    
                    elif y == yBuffer:
                        self.objectHitBox.top -= (-ySpeed * (elapsed / 1000.0))
                        foundCollision = True
                        break
                    
                y = y - 1
                
    def GetPixelCollision(self, bitMask, x, y):
        if bitMask.get_at((x, y)) == 1:
            return True
        elif bitMask.get_at((x, y)) == 0:
            return False
        
    
        