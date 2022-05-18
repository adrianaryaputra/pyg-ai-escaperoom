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
                # self.speed = [-1*self.velocity, 0]
            elif block[0].rect.y == block[1].y and block[1].width > block[1].height:
                self.rect.bottom = block[0].rect.top
                # self.speed = [0, -1*self.velocity]
            elif block[1].width > block[1].height:
                self.rect.top = block[0].rect.bottom
                # self.speed = [0, self.velocity]
            elif block[1].width < block[1].height:
                self.rect.left = block[0].rect.right
                # self.speed = [self.velocity, 0]


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
        self.base_image = pygame.Surface(size=(9*size, 9*size))
        self.base_rect = self.base_image.get_rect(center=position)
        self.base_image.fill(COLOR.BG)
        self.base_image.set_colorkey(COLOR.BG)
        self.image = self.base_image.copy()
        self.rect = self.image.get_rect(center=position)
        self.velocity = velocity
        self.direction = direction

        self.FLAG_play = False

        self.speed = 0
        self.curDegree = 0

        self.subelem = []
        for i in range(5):
            si = pygame.Surface(size=(size, size))
            sr = si.get_rect(centerx=self.rect.width/2, top=2*i*size)
            si.fill(COLOR.OBSTACLE)
            self.subelem.append((si, sr))

        for i in range(5):
            si = pygame.Surface(size=(size, size))
            sr = si.get_rect(left=2*i*size, centery=self.rect.height/2)
            si.fill(COLOR.OBSTACLE)
            if i != 2:
                self.subelem.append((si, sr))

        self.base_image.blits(self.subelem)
        self.rotate(0)
        self.draw()


    def rotate(self, degree):
        self.curDegree += degree * self.direction
        self.curDegree %= 360
        self.image = self.base_image.copy()
        self.image = pygame.transform.rotate(self.image, self.curDegree)
        self.rect = self.image.get_rect(center=self.rect.center)


    def play(self):
        self.FLAG_play = True
        self.speed = self.velocity

    
    def stop(self):
        self.FLAG_play = False
        self.speed = 0

    
    def update(self):
        if self.FLAG_play:
            self.rotate(self.speed)
        pass


    def draw(self):
        self.parent.image.blit(self.image, self.rect)


    def handleEvent(self, event):
        pass


    def dataSave(self):
        return {
            'position': self.rect.center,
            'velocity': self.velocity,
            'direction': self.direction,
            'type': 'RotatingObstacle'
        }

    
    def dataLoad(self, data):
        pass