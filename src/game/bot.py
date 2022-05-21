from turtle import goto
import pygame
import numpy as np
import math

from .colorscheme import COLOR


class Instructions:
    def __init__(self, size: int, max_speed: int = 5) -> None:
        self.size = size
        self.max_speed = max_speed
        self.step = 0
        self.directions = np.zeros((self.size, 2))
        # self._randomize()
        self._randomangle()
        # print(self.directions)

    def _randomize(self, seed: int = None) -> None:
        if seed is not None:
            np.random.seed(seed)
        self.directions = np.random.randint(0, high=self.max_speed*2, size=self.directions.shape) - self.max_speed

    def _randomangle(self, seed: int = None) -> None:
        if seed is not None:
            np.random.seed(seed)
        val = np.random.rand(self.size) * 2 * math.pi
        self.directions = np.stack((np.cos(val)*self.max_speed, np.sin(val)*self.max_speed), axis=1)
        self.directions = self.directions.astype(int)


class Individual(pygame.sprite.Sprite):
    def __init__(self, parent: pygame.sprite.Sprite, position, size, speed, instructions: Instructions = None):
        super().__init__()
        self.parent = parent
        # create an object for representing image
        self.image = pygame.Surface(size=(size, size))
        # set the location of the object
        self.rect = self.image.get_rect(center=position)
        # position
        # self.position = position
        # scalar speed
        self.speed = speed
        # vector velocity in xy axis
        self.velocity = np.array([0, 0])
        # instructions: list of accelerations
        self.instructions = instructions
        self.image.fill(COLOR.PLAYER)
        self.FLAG_alive = True

    def update(self):
        if self.instructions is not None:
            if len(self.instructions.directions) > self.instructions.step:
                instruction = self.instructions.directions[self.instructions.step]
                self.instructions.step += 1
                self.velocity += instruction
                self.velocity.clip(-self.speed, self.speed)
            else:
                self.velocity = np.array([0, 0])
        # self.position += self.velocity
        self.rect.move_ip(self.velocity)
        self.collisionHandler()

    def draw(self):
        self.parent.image.blit(self.image, self.rect)

    def handleEvent(self, event):
        self._onKeyEvent()

    def AI_injectMovement(self, vx, vy):
        if vy<-0.2:
            self.onKeyUp(pygame.K_DOWN)
            self.onKeyDown(pygame.K_UP)
        elif vy>0.2:
            self.onKeyUp(pygame.K_UP)
            self.onKeyDown(pygame.K_DOWN)
        else:
            self.onKeyUp(pygame.K_UP)
            self.onKeyUp(pygame.K_DOWN)

        if vx<-0.2:
            self.onKeyUp(pygame.K_RIGHT)
            self.onKeyDown(pygame.K_LEFT)
        elif vx>0.2:
            self.onKeyUp(pygame.K_LEFT)
            self.onKeyDown(pygame.K_RIGHT)
        else:
            self.onKeyUp(pygame.K_LEFT)
            self.onKeyUp(pygame.K_RIGHT)
        

    def _onKeyEvent(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] and keys[pygame.K_LEFT]:
            self.velocity[0] = 0
        elif keys[pygame.K_LEFT]:
            self.velocity[0] = -self.speed
        elif keys[pygame.K_RIGHT]:
            self.velocity[0] = self.speed
        else:
            self.velocity[0] = 0
        if keys[pygame.K_UP] and keys[pygame.K_DOWN]:
            self.velocity[1] = 0
        elif keys[pygame.K_UP]:
            self.velocity[1] = -self.speed
        elif keys[pygame.K_DOWN]:
            self.velocity[1] = self.speed
        else:
            self.velocity[1] = 0
        
        # diagonal velocity adjustment
        if self.velocity[0] != 0 and self.velocity[1] != 0:
            self.velocity[0] *= 0.77
            self.velocity[1] *= 0.77


    def checkCollisions(self, objList):
        # check collision with all objects
        collisionListID = self.rect.collidelistall(objList)

        # if collision with object
        if len(collisionListID) > 0:
            return True
        return False


    def collisionHandler(self):
        # transform parent rect to relative coordinate
        rect = self.parent.rect.copy()
        rect.move_ip(-self.parent.rect.left, -self.parent.rect.top)
        
        # peg player inside map surface
        self.rect.clamp_ip(rect)

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