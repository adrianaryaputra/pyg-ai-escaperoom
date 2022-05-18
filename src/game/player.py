import pygame

from .colorscheme import COLOR
from .object import BasicObject



class Player(BasicObject):
    def __init__(self, parent: pygame.sprite.Sprite, position, size, velocity):
        super().__init__(parent=parent, position=position, size=size, velocity=velocity)
        self.image.fill(COLOR.PLAYER)


    def handleEvent(self, event):
        if event.type == pygame.KEYDOWN:
            self.onKeyDown(event.key)
        if event.type == pygame.KEYUP:
            self.onKeyUp(event.key)


    def AI_injectMovement(self, w,a,s,d):
        if w>0:
            self.onKeyDown(pygame.K_UP)
        if a>0:
            self.onKeyDown(pygame.K_LEFT)
        if s>0:
            self.onKeyDown(pygame.K_DOWN)
        if d>0:
            self.onKeyDown(pygame.K_RIGHT)


    def onKeyDown(self, key):
        if key == pygame.K_LEFT:
            self.speed[0] = -self.velocity
        if key == pygame.K_RIGHT:
            self.speed[0] = self.velocity
        if key == pygame.K_UP:
            self.speed[1] = -self.velocity
        if key == pygame.K_DOWN:
            self.speed[1] = self.velocity
        
        # diagonal speed adjustment
        if self.speed[0] != 0 and self.speed[1] != 0:
            self.speed[0] *= 0.7
            self.speed[1] *= 0.7

    
    def onKeyUp(self, key):
        if key == pygame.K_LEFT:
            self.speed[0] = 0
            self.speed[1] = round(self.speed[1]/0.7)
        if key == pygame.K_RIGHT:
            self.speed[0] = 0
            self.speed[1] = round(self.speed[1]/0.7)
        if key == pygame.K_UP:
            self.speed[1] = 0
            self.speed[0] = round(self.speed[0]/0.7)
        if key == pygame.K_DOWN:
            self.speed[1] = 0
            self.speed[0] = round(self.speed[0]/0.7)


    def collisionHandler(self):
        super().collisionHandler()

        # check collision with all blocks
        collidableBlock = [block for block in self.parent.blocks if block.collidable]
        collisionListID = self.rect.collidelistall(collidableBlock)
        collisionList = [collidableBlock[i] for i in collisionListID]
        collisionClip = [self.rect.clip(coll) for coll in collisionList]

        for block in zip(collisionList, collisionClip):
            if block[0].rect.x == block[1].x and block[1].width < block[1].height:
                self.rect.right = block[0].rect.left
            elif block[0].rect.y == block[1].y and block[1].width > block[1].height:
                self.rect.bottom = block[0].rect.top
            elif block[1].width > block[1].height:
                self.rect.top = block[0].rect.bottom
            elif block[1].width < block[1].height:
                self.rect.left = block[0].rect.right