import pygame

from src.game.button import Button
from src.game.colorscheme import COLOR
from src.game.level import Level



def main():
    pygame.init()
    SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Hardest Game Ever")
    FPS = 60
    clock = pygame.time.Clock()

    level = Level(screen)

    # TODO: 
    # - buat score, konsepnya gimana?
    # - buat elapse time?
    # - tampilkan generasi NN
    
    level.dataLoad("./src/level/level_1.map")
    level.playObstacles()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            level.map.handleEvent(event)
            level.player.handleEvent(event)
            for obstacle in level.obstacles:
                obstacle.handleEvent(event)

        screen.fill(COLOR.BG)

        level.map.draw()
        level.map.update()

        level.player.draw()
        level.player.update()

        if level.FLAG_isPlaying and level.player.checkCollisions(level.getObstacleCollisionRects()):
            level.dataLoad("./src/level/level_1.map")
            level.playObstacles()

        for obstacle in level.obstacles:
            obstacle.draw()
            obstacle.update()

        pygame.display.update()
        clock.tick(FPS)



if __name__ == '__main__':
    main()