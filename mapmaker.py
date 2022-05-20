from multiprocessing.pool import ThreadPool
import os
import pygame

from src.game.button import Button
from src.game.colorscheme import COLOR
from src.game.level import Level



def main():
    pygame.init()
    SCREEN_WIDTH, SCREEN_HEIGHT = 960, 600
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.DOUBLEBUF)
    pygame.display.set_caption("Map Maker")
    FPS = 60
    clock = pygame.time.Clock()

    level = Level(screen)
    pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP, pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP])

    buttons = pygame.sprite.Group()
    buttons.add(Button(screen, (10, 10), (150, 40), "Load Map", level.dataLoad))
    buttons.add(Button(screen, (10, 60), (150, 40), "Save Map", level.dataSave))
    buttons.add(Button(screen, (170, 10), (150, 40), "Create VU-Obs", level.createVUpObstacle))
    buttons.add(Button(screen, (170, 60), (150, 40), "Create HL-Obs", level.createHLeftObstacle))
    buttons.add(Button(screen, (330, 10), (150, 40), "Create VD-Obs", level.createVDownObstacle))
    buttons.add(Button(screen, (330, 60), (150, 40), "Create HR-Obs", level.createHRightObstacle))
    buttons.add(Button(screen, (490, 10), (150, 40), "Create CW-Obs", level.createCWObstacle))
    buttons.add(Button(screen, (490, 60), (150, 40), "Create CCW-Obs", level.createCCWObstacle))
    buttons.add(Button(screen, (650, 10), (150, 40), "Play Obstacles", level.playObstacles))
    buttons.add(Button(screen, (650, 60), (150, 40), "Stop Obstacles", level.stopObstacles))
    buttons.add(Button(screen, (810, 10), (140, 40), "Clear Obs", level.obstacles.empty))
    buttons.add(Button(screen, (810, 60), (140, 40), "Clear Map", level.map.clear))

    pool = ThreadPool(os.cpu_count())

    while 1:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pool.close()
                pygame.quit()

            pool.apply(level.map.handleEvent, (event,))
            pool.apply(level.player.handleEvent, (event,))
            pool.map(lambda o: o.handleEvent(event), level.obstacles)
            pool.map(lambda b: b.handleEvent(event), buttons)

        screen.fill(COLOR.BG)

        pool.apply(level.map.update, ())
        pool.apply(level.player.update, ())

        pool.apply(level.map.draw, ())
        pool.apply(level.player.draw, ())

        if level.FLAG_isPlaying and level.player.checkCollisions(level.getObstacleCollisionRects()):
            break

        pool.map(lambda o: o.update(), level.obstacles)
        pool.map(lambda o: o.draw(), level.obstacles)

        pool.apply(buttons.draw, (screen,))
        pool.apply(buttons.update, ())

        pygame.display.update()
        clock.tick(FPS)



if __name__ == '__main__':
    main()