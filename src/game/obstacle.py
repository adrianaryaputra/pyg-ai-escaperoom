import pygame

from .colorscheme import COLOR
from .object import BasicObject



class BouncingObstacle(BasicObject):
    def __init__(self, parent: pygame.sprite.Sprite, position, size, velocity, direction):
        super().__init__(parent, position, size, velocity)
        self.image.fill(COLOR.OBSTACLE)
        self.direction = direction
        self.FLAG_mouse3down = False
        self.FLAG_play = False

    
    def collisionHandler(self):
        super().collisionHandler()

        # similar to player
        # check collision with all blocks
        collidableBlock = [block for block in self.parent.blocks if block.collidable]
        collisionListID = self.rect.collidelistall(collidableBlock)
        collisionList = [collidableBlock[i] for i in collisionListID]
        collisionClip = [self.rect.clip(coll) for coll in collisionList]

        for block in zip(collisionList, collisionClip):
            if block[0].rect.x == block[1].x and block[1].width < block[1].height:
                self.rect.right = block[0].rect.left
                self.speed = [-self.velocity, 0]
            elif block[0].rect.y == block[1].y and block[1].width > block[1].height:
                self.rect.bottom = block[0].rect.top
                self.speed = [0, -self.velocity]
            elif block[1].width > block[1].height:
                self.rect.top = block[0].rect.bottom
                self.speed = [0, self.velocity]
            elif block[1].width < block[1].height:
                self.rect.left = block[0].rect.right
                self.speed = [self.velocity, 0]


    def handleEvent(self, event):
        # if right mouse click
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            #  if mouse position is in the obstacle
            if self.rect.collidepoint(self.getRelativePosition(event.pos)):
                self.FLAG_mouse3down = True
        if event.type == pygame.MOUSEBUTTONUP and event.button == 3:
            self.FLAG_mouse3down = False


    def update(self):
        self.onMouse3()
        super().update()


    def onMouse3(self):
        if self.FLAG_mouse3down:
            self.rect.center = self.getRelativePosition(pygame.mouse.get_pos())


    def play(self):
        self.FLAG_play = True
        self.speed[self.direction] = self.velocity

    
    def stop(self):
        self.FLAG_play = False
        self.speed[self.direction] = 0


    def dataSave(self):
        ds = super().dataSave()
        ds["direction"] = self.direction
        return ds