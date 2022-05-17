import pygame



class BasicObject(pygame.sprite.Sprite):
    def __init__(self, parent: pygame.sprite.Sprite, position, size, velocity):
        super().__init__()
        self.parent = parent
        self.image = pygame.Surface(size=(size, size))
        self.rect = self.image.get_rect(center=position)
        self.velocity = velocity
        self.speed = [0,0]


    def update(self):
        self.rect.move_ip(self.speed)
        self.collisionHandler()


    def draw(self):
        self.parent.image.blit(self.image, self.rect)


    def handleEvent(self, event):
        pass


    def collisionHandler(self):
        # transform parent rect to relative coordinate
        rect = self.parent.rect.copy()
        rect.move_ip(-self.parent.rect.left, -self.parent.rect.top)

        # peg player inside map surface
        self.rect.clamp_ip(rect)


    def getRelativePosition(self, position):
        return (position[0] - self.parent.rect.left, position[1] - self.parent.rect.top)


    def dataSave(self):
        return {
            'position': self.rect.center,
            'velocity': self.velocity
        }


    def dataLoad(self, data):
        self.rect.center = data['position']
        self.velocity = data['velocity']