import pygame

from src.game.obstacle import BouncingObstacle, RotatingObstacle
from src.game.button import Button
from src.game.colorscheme import COLOR
from src.game.level import Level



def main():
    pygame.init()
    SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Map Maker")
    FPS = 60
    clock = pygame.time.Clock()

    level = Level(screen)

    obs2 = RotatingObstacle(level.map, (300,300), 20, 2, 1)
    obs2.play()

    buttons = pygame.sprite.Group()
    buttons.add(Button(screen, (10, 10), (150, 40), "Load Map", level.dataLoad))
    buttons.add(Button(screen, (10, 60), (150, 40), "Save Map", level.dataSave))
    buttons.add(Button(screen, (170, 10), (150, 40), "Create V-Obs", level.createVObstacle))
    buttons.add(Button(screen, (170, 60), (150, 40), "Create H-Obs", level.createHObstacle))
    buttons.add(Button(screen, (330, 10), (150, 40), "Create CW-Obs", level.createCWObstacle))
    buttons.add(Button(screen, (330, 60), (150, 40), "Create CCW-Obs", level.createCCWObstacle))
    buttons.add(Button(screen, (490, 10), (150, 40), "Play Obstacles", level.playObstacles))
    buttons.add(Button(screen, (490, 60), (150, 40), "Stop Obstacles", level.stopObstacles))
    buttons.add(Button(screen, (650, 10), (140, 40), "Clear Obs", level.obstacles.empty))
    buttons.add(Button(screen, (650, 60), (140, 40), "Clear Map", level.map.clear))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            level.map.handleEvent(event)
            level.player.handleEvent(event)
            for obstacle in level.obstacles:
                obstacle.handleEvent(event)
            for button in buttons:
                button.handleEvent(event)

        screen.fill(COLOR.BG)

        level.map.draw()
        level.map.update()

        level.player.draw()
        level.player.update()

        for obstacle in level.obstacles:
            obstacle.draw()
            obstacle.update()

        buttons.draw(screen)
        buttons.update()

        pygame.display.update()
        clock.tick(FPS)



if __name__ == '__main__':
    main()