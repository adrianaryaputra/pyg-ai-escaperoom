import pygame

from src.game.button import Button
from src.game.colorscheme import COLOR
from src.game.level import Level
from src.game.player import Player
from src.game.bot import Individual, Instructions



def main():
    pygame.init()
    SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
    NUM_POPULATION = 10
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Hardest Game Ever")
    FPS = 30
    clock = pygame.time.Clock()
    level = Level(screen, n_bot=10) 
    # level.player = Individual(level.map, (400, 300), 20, 5, Instructions(200, max_speed=3))

    # TODO: 
    # - buat score, konsepnya gimana?
    # - buat elapse time?
    # - tampilkan generasi NN

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            level.map.handleEvent(event)
            for individual in level.population:
                individual.handleEvent(event)
            # level.player.handleEvent(event)
            for obstacle in level.obstacles:
                obstacle.handleEvent(event)

        screen.fill(COLOR.BG)

        level.map.draw()
        level.map.update()

        for individual in level.population:
            individual.draw()
            individual.update()
        # level.player.draw()
        # level.player.update()

        # if level.FLAG_isPlaying and level.player.checkCollisions(level.getObstacleCollisionRects()):
        #     level.dataLoad("./src/level/level_1.map")
        #     level.playObstacles()

        for obstacle in level.obstacles:
            obstacle.draw()
            obstacle.update()

        pygame.display.update()
        clock.tick(FPS)



if __name__ == '__main__':
    main()