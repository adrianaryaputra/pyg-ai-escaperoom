import math
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

        if len(collisionListID) > 0:
            self.speed = [self.speed[0]*-1, self.speed[1]*-1]

        for block in zip(collisionList, collisionClip):
            if block[0].rect.x == block[1].x and block[1].width < block[1].height:
                self.rect.right = block[0].rect.left
            elif block[0].rect.y == block[1].y and block[1].width > block[1].height:
                self.rect.bottom = block[0].rect.top
            elif block[1].width > block[1].height:
                self.rect.top = block[0].rect.bottom
            elif block[1].width < block[1].height:
                self.rect.left = block[0].rect.right


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
        ds["type"] = "BouncingObstacle"
        return ds



class RotatingObstacle(pygame.sprite.Sprite):
    def __init__(self, parent: pygame.sprite.Sprite, position, size, velocity, direction):
        super().__init__()
        self.parent = parent
        self.image = pygame.Surface(size=(9*size, 9*size))
        self.rect = self.image.get_rect(center=position)
        self.image.fill(COLOR.BG)
        # self.image.set_colorkey(COLOR.BG)
        self.velocity = velocity
        self.direction = direction

        self.FLAG_play = False
        self.FLAG_mouse3down = False

        self.speed = 0
        self.curDegree = 0

        self.subelem = []

        for defaultAngle in [0, 90, 180, 270]:
            for defaultDistance in [2*size, 4*size]:
                self.subelem.append(self.createSubElement(size, defaultDistance, defaultAngle))
        self.subelem.append(self.createSubElement(size, 0, 0))
        self.draw()


    def createSubElement(self, size, distance, angle):
        si = pygame.Surface(size=(size, size))
        si.fill(COLOR.BG)
        si.set_colorkey(COLOR.BG)
        pygame.draw.circle(si, COLOR.OBSTACLE, (size//2, size//2), size//2)
        sd = self.calculateRelativePosition(distance, angle)
        sr = si.get_rect(
            centerx=self.rect.centerx + sd[0], 
            centery=self.rect.centery + sd[1],
        )
        return (si, sr, distance, angle)


    def calculateRelativePosition(self, distance, angle):
        rd = (distance*math.cos(angle*math.pi/180), distance*math.sin(angle*math.pi/180))
        # print(rd)
        return rd


    def rotate(self, degree):
        self.curDegree += degree * self.direction
        self.curDegree %= 360
        for sub in self.subelem:
            newRelPos = self.calculateRelativePosition(sub[2], sub[3] + self.curDegree)
            sub[1].center = (self.rect.centerx + newRelPos[0], self.rect.centery + newRelPos[1])


    def play(self):
        self.FLAG_play = True
        self.speed = self.velocity

    
    def stop(self):
        self.FLAG_play = False
        self.speed = 0

    
    def update(self):
        self.onMouse3()
        if self.FLAG_play:
            self.rotate(self.speed)
        pass


    def draw(self):
        # self.parent.image.blit(self.image, self.rect)
        self.parent.image.blits([s[:2] for s in self.subelem])


    def handleEvent(self, event):
        # if right mouse click
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            #  if mouse position is in the obstacle
            if self.rect.collidepoint(self.getRelativePosition(event.pos)):
                self.FLAG_mouse3down = True
        if event.type == pygame.MOUSEBUTTONUP and event.button == 3:
            self.FLAG_mouse3down = False


    def onMouse3(self):
        if self.FLAG_mouse3down:
            self.rect.center = self.getRelativePosition(pygame.mouse.get_pos())
            self.rotate(0)


    def getRelativePosition(self, position):
        rp = (position[0] - self.parent.rect.left, position[1] - self.parent.rect.top)
        print(self.rect.center, position, rp)
        return rp


    def dataSave(self):
        return {
            'position': self.rect.center,
            'velocity': self.velocity,
            'direction': self.direction,
            'type': 'RotatingObstacle'
        }

    
    def dataLoad(self, data):
        pass