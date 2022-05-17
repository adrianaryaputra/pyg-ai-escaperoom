import pygame

from .colorscheme import COLOR



class Button(pygame.sprite.Sprite):
    def __init__(self, parent: pygame.Surface, position, size, text, onClick):
        super().__init__()
        self.parent = parent
        self.image = pygame.Surface(size=size)
        self.rect = self.image.get_rect(top=position[1], left=position[0])
        self.text = text
        self.font = pygame.font.SysFont("Arial", 20)
        self.textSurface = self.font.render(self.text, True, (0, 0, 0))
        self.textRect = self.textSurface.get_rect(center=(self.rect.width//2, self.rect.height//2))
        self.onClick = onClick


    def draw(self):
        self.parent.blit(self.image, self.rect)


    def update(self):
        mousePos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mousePos):
            self.image.fill(COLOR.BUTTON_HOVER)
            self.image.blit(self.textSurface, self.textRect)
        else:
            self.image.fill(COLOR.BUTTON)
            self.image.blit(self.textSurface, self.textRect)


    def handleEvent(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mousePos = pygame.mouse.get_pos()
                if self.rect.collidepoint(mousePos):
                    self.onClick()