import pygame
import numpy as np
import math

from .colorscheme import COLOR


class xxxIndividual(pygame.sprite.Sprite):
    def __init__(self, position: tuple[int, int], size: int, instructions, max_speed: int) -> None:
        super().__init__()
        self.initial_position = position
        self.size = size
        self.velocity = np.array((0, 0))
        self.instructions = instructions
        self.max_speed = max_speed
        # create an object for representing image
        self.image = pygame.Surface(size=(size, size))
        # set the location of the object
        self.rect = self.image.get_rect(center=position)
        self.image.fill(COLOR.PLAYER)
        self.is_alive = True
        self.fitness = 0
        self.step = 0
        # self.last_update = True

    def calculateFitness(self, finish_point: tuple[int, int]) -> None:
        diff = ((self.rect.centerx - finish_point[0]), (self.rect.centery - finish_point[1]))
        eucdistance = math.sqrt(diff[0]**2 + diff[1]**2)
        try:
            self.fitness = 1.0 / (eucdistance**2)
            # clip fitness to 999
            self.fitness = 999 if self.fitness > 999 else self.fitness
        except ZeroDivisionError:
            # catch zero division error
            self.fitness = 1000

    def update(self, level):
        if not self.is_alive:
            return
            # if not self.last_update:
            #     return
            # else:
            #     self.velocity = np.array([0, 0])
            #     self.last_update = False
        if len(self.instructions) > self.step:
            self.velocity += self.instructions[self.step]
            self.velocity = np.clip(self.velocity, 
                np.ones(self.velocity.shape)*-self.max_speed, 
                np.ones(self.velocity.shape)*self.max_speed)
            self.step += 1
        else:
            self.is_alive = False
            self.velocity = np.array([0, 0])
        # self.position += self.velocity
        self.rect.move_ip(self.velocity)
        self.collisionHandler(level)

    def draw(self, level):
        pygame.draw.rect(self.image, (255,255,255), self.image.get_rect(), 3)
        level.map.image.blit(self.image, self.rect)

    def checkCollisions(self, objList):
        # check collision with all objects
        collisionListID = self.rect.collidelistall(objList)

        # if collision with object
        if len(collisionListID) > 0:
            return True
        return False

    def collisionHandler(self, level):
        # transform parent rect to relative coordinate
        rect = level.map.rect.copy()
        rect.move_ip(-level.map.rect.left, -level.map.rect.top)
        
        # Check if player touch the edge -> Die
        if not rect.collidepoint(self.rect.topleft) or not rect.collidepoint(self.rect.bottomright):
            self.is_alive = False

        # peg player inside map surface
        self.rect.clamp_ip(rect)

        # check collision with all blocks
        collidableBlock = [block for block in level.map.blocks if block.collidable]
        collisionListID = self.rect.collidelistall(collidableBlock)
        collisionList = [collidableBlock[i] for i in collisionListID]
        collisionClip = [self.rect.clip(coll) for coll in collisionList]

        if len(collisionListID) > 0:
            self.is_alive = False

        for block in zip(collisionList, collisionClip):
            if block[0].rect.x == block[1].x and block[1].width < block[1].height:
                self.rect.right = block[0].rect.left
            elif block[0].rect.y == block[1].y and block[1].width > block[1].height:
                self.rect.bottom = block[0].rect.top
            elif block[1].width > block[1].height:
                self.rect.top = block[0].rect.bottom
            elif block[1].width < block[1].height:
                self.rect.left = block[0].rect.right

        # check collision with obstacles
        if self.checkCollisions(level.getObstacleCollisionRects()):
            self.is_alive = False
            # self.last_update = False

class Population():
    def __init__(self, num_individual: int, max_speed: int = 3, individual_type: pygame.sprite.Sprite = xxxIndividual ) -> None:
        self.initial_position = (150, 240)  # start position(150, 240) finish position(630, 240)
        self.num_instruction = 200
        self.num_individual = num_individual
        self.max_speed = max_speed
        self.instructions = self._createInstructions()
        # self.steps = np.zeros(num_individual)
        self.individuals = []
        for n in range(self.num_individual):
            self.individuals.append(individual_type(self.initial_position, 20, self.instructions[n], self.max_speed))

    def _createInstructions(self):
        instructions = []
        for n in range(self.num_instruction):
            instructions.append(self._randomAngle())
        return np.array(instructions)

    def _randomAngle(self, seed: int = None):
        '''
        ex:  [[[1, 2], [2, 4]],  [[1, 3], [4, 5]], ]
        '''
        if seed is not None:
            np.random.seed(seed)
        val = np.random.rand(self.num_instruction) * 2 * math.pi
        directions = np.stack((np.cos(val)*self.max_speed, np.sin(val)*self.max_speed), axis=1)
        directions = directions.astype(int)
        return directions
        

    def updateInstructions(self) -> None:
        for n in range(self.num_individual):
            self.individuals[n].instructions = self.instructions[n]

    def updateFitness(self, finish_point: tuple[int, int]) -> None:
        for n in range(self.num_individual):
            self.individuals[n].calculateFitness(finish_point)
    
    def resetSteps(self) -> None:
        # self.steps = np.zeros(self.num_individual)
        for n in range(self.num_individual):
            self.individuals[n].step = 0

    def resetLives(self) -> None:
        for n in range(self.num_individual):
            self.individuals[n].is_alive = True

    def resetPositions(self) -> None:
        for n in range(self.num_individual):
            self.individuals[n].rect.center = self.individuals[n].initial_position
            self.individuals[n].velocity = np.array((0, 0))

    def allDead(self) -> bool:
        for n in range(self.num_individual):
            if self.individuals[n].is_alive:
                return False
        return True

    def fitnessProbability(self) -> tuple[list[float], float]:
        fitnessSum = 0
        fitnessVal = []
        for n in range(self.num_individual):
            fitnessSum += self.individuals[n].fitness
            fitnessVal.append(self.individuals[n].fitness)
        return fitnessVal, fitnessSum