import pygame
import numpy as np

from src.game.button import Button
from src.game.colorscheme import COLOR
from src.game.level import Level
from src.game.player import Player
from src.game.bot import Population



def main():
    pygame.init()
    SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
    NUM_POPULATION = 10
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Hardest Game Ever")
    FPS = 60
    clock = pygame.time.Clock()
    level = Level(screen)
    population = Population(NUM_POPULATION, 5)

    level.dataLoad("./src/level/level_1.map")
    level.playObstacles()

    # TODO: 
    # - buat score, konsepnya gimana?
    # - buat elapse time?
    # - tampilkan generasi NN

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            level.map.handleEvent(event)
            # for individual in population.individuals:
            #     individual.handleEvent(event)
            # level.player.handleEvent(event)
            for obstacle in level.obstacles:
                obstacle.handleEvent(event)

        if population.allDead():
            # TODO: add heuristics
            population.updateFitness((630, 240))
            fitnessVal, fitnessSum = population.fitnessProbability()
            sort_index = np.argsort(np.array(fitnessVal))
            # new_instructions = ga.update(fitnessVal, fitnessSum, population.instructions)
            # population.updateInstructions(new_instruction)
            
            # level.dataLoad("./src/level/level_2.map")
            # level.playObstacles()


            # TEST: Show the best fitness
            population.individuals[sort_index[-1]].image.fill((255, 0, 0))
            population.individuals[sort_index[-2]].image.fill((255, 127, 0))
            population.individuals[sort_index[-3]].image.fill((255, 255, 0))


        screen.fill(COLOR.BG)

        level.map.draw()
        level.map.update()

        for individual in population.individuals:
            individual.draw(level)
            individual.update(level)
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