from itertools import chain
import pygame
from src.game.obstacle import BouncingObstacle

from src.game.button import Button
from src.game.colorscheme import COLOR
from src.game.level import Level



def main():
    pygame.init()
    SCREEN_WIDTH, SCREEN_HEIGHT = 960, 600
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Map Maker")
    FPS = 60
    clock = pygame.time.Clock()

    level = Level(screen)

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

    # Add Surrounding Wall
    # for i in range(16):
    #     level.map.blocks[i].onMouseDown()
    #     level.map.blocks[-i-1].onMouseDown()
    # for i in range(1, 25):
    #     level.map.blocks[i*16].onMouseDown()
    #     level.map.blocks[(i+1)*16-1].onMouseDown()

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

        if level.FLAG_MODE:
            if level.player.checkCollisions([x.rect for x in level.obstacles if x.__class__ == 'BouncingObstacle']):
                break
            list_of_rects = [x.minirectangle for x in level.obstacles if x.__class__ == 'RotatingObstacle']
            list_of_rects = list(chain.from_iterable(list_of_rects))
            if level.player.checkCollisions(list_of_rects):
                break


        for obstacle in level.obstacles:
            obstacle.draw()
            obstacle.update()

        buttons.draw(screen)
        buttons.update()

        pygame.display.update()
        clock.tick(FPS)



if __name__ == '__main__':
    main()