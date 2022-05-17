import math
import pygame

from .colorscheme import COLOR


class Map(pygame.sprite.Sprite):
    def __init__(self, screen, map_position, block_dim, block_size):
        super().__init__()
        self.screen = screen
        self.position = map_position
        self.blockDim = block_dim
        self.blockSize = block_size
        self.size = (block_dim[0]*block_size, block_dim[1]*block_size)
        
        # create map surface
        self.image = pygame.Surface(size=self.size)
        self.image.fill(COLOR.WALL)
        self.rect = self.image.get_rect(top=self.position[1], left=self.position[0])

        # create blocks
        self.blockGroup = pygame.sprite.Group()
        self.blocks = []
        self.generateBlocks(block_dim, block_size)


    def generateBlocks(self, dim, size):
        for i in range(dim[0]):
            for j in range(dim[1]):
                self.blocks.append(Block(self.screen, (i*size, j*size), (size, size)))
                self.blockGroup.add(self.blocks[-1])


    def draw(self):
        self.screen.blit(self.image, self.rect)
        self.blockGroup.draw(self.image)


    def update(self):
        self.blockGroup.update()


    def handleEvent(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.rect.collidepoint(event.pos):
                mousePos = pygame.mouse.get_pos()
                clickedBlock = self.getBlockByPosition(mousePos)
                clickedBlock.onMouseDown()


    def getBlockByPosition(self, position):
        relativePos = (position[0] - self.rect.left, position[1] - self.rect.top)
        x = math.floor(relativePos[0] / self.blockSize)
        y = math.floor(relativePos[1] / self.blockSize)
        return self.blocks[y + x*self.blockDim[1]]


    def dataSave(self):
        data = []
        for block in self.blocks:
            data.append(block.dataSave())
        return data


    def dataLoad(self, data):
        for i in range(len(data)):
            self.blocks[i].dataLoad(data[i])



class Block(pygame.sprite.Sprite):
    def __init__(self, parent: pygame.Surface, position, size):
        super().__init__()
        self.parent = parent
        self.image = pygame.Surface(size=size)
        self.image.fill(COLOR.BG)
        self.rect = self.image.get_rect(top=position[1], left=position[0])

        self.foreground = pygame.Surface(size=(size[0]-2, size[1]-2))
        self.foreground_rect = self.foreground.get_rect(top=1, left=1)

        self.blockTypes = {
            "floor": (COLOR.FLOOR, False),
            "wall": (COLOR.WALL, True),
            "finish": (COLOR.FINISH, False),
        }
        self.blockType = "floor"
        self.configureType()


    def configureType(self):
        self.foreground.fill(self.blockTypes[self.blockType][0])
        self.image.blit(self.foreground, self.foreground_rect)
        self.collidable = self.blockTypes[self.blockType][1]


    def update(self):
        pass


    def onMouseDown(self):
        # find index of current block type
        blockTypeIndex = list(self.blockTypes.keys()).index(self.blockType)

        # find next block type
        blockTypeIndex += 1
        blockTypeIndex %= len(self.blockTypes)
        self.blockType = list(self.blockTypes.keys())[blockTypeIndex]
        self.configureType()


    def dataSave(self):
        return self.blockType


    def dataLoad(self, data):
        self.blockType = data
        self.configureType()