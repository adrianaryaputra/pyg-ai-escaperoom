import pygame, math

from src.game.map import Map
from src.game.colorscheme import COLOR



COLOR_WALL = (0, 0, 0)
COLOR_FLOOR = (180, 180, 180)
COLOR_FINISH = (80, 180, 80)
COLOR_BG = (150, 150, 150)



class Player(pygame.sprite.Sprite):
    def __init__(self, parent: pygame.sprite.Sprite, position, size, velocity):
        super().__init__()
        self.parent = parent
        self.image = pygame.Surface(size=(size, size))
        self.image.fill(COLOR.PLAYER)
        self.rect = self.image.get_rect(center=position)
        self.velocity = velocity
        self.speed = [0,0]


    def update(self):
        self.rect.move_ip(self.speed)
        self.collisionHandler()


    def draw(self):
        self.parent.image.blit(self.image, self.rect)


    def handleEvent(self, event):
        if event.type == pygame.KEYDOWN:
            self.onKeyDown(event.key)
        if event.type == pygame.KEYUP:
            self.onKeyUp(event.key)


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
            print(block)
            if block[0].rect.x == block[1].x and block[1].width < block[1].height:
                self.rect.right = block[0].rect.left
            elif block[0].rect.y == block[1].y and block[1].width > block[1].height:
                self.rect.bottom = block[0].rect.top
            elif block[1].width > block[1].height:
                self.rect.top = block[0].rect.bottom
            elif block[1].width < block[1].height:
                self.rect.left = block[0].rect.right

        # for block in collisionList:
        #     overlap = self.rect.clip(block)
        #     print(overlap)



def main():
    pygame.init()
    SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Map Maker")
    FPS = 60
    clock = pygame.time.Clock()

    map = Map(screen, (10, 110), (26, 16), 30)
    player = Player(map, (400, 300), 20, 5)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            map.handleEvent(event)
            player.handleEvent(event)

        screen.fill(COLOR_BG)

        map.draw()
        map.update()

        player.draw()
        player.update()

        pygame.display.update()
        clock.tick(FPS)




if __name__ == '__main__':
    main()