import pygame
import numpy as np

from src.game.button import Button
from src.game.colorscheme import COLOR
from src.game.level import Level
from src.game.player import Player
from src.game.bot import Population

from src.game.heuristic import simpleGA



def main():
    pygame.init()
    SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
    NUM_POPULATION = 100
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Hardest Game Ever")
    FPS = 60
    FLAG_FAST_TRAINING = True
    clock = pygame.time.Clock()
    level = Level(screen)
    population = Population(NUM_POPULATION, 5)

    level.dataLoad("./src/level/level_1.map")
    level.playObstacles()
    generation = 0
    pause_iteration = 0

    ga = simpleGA(NUM_POPULATION)


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
            if pause_iteration < 10:
                pause_iteration += 1
                population.individuals[sort_index[-1]].image.fill((255, 0, 0))
                population.individuals[sort_index[-2]].image.fill((255, 127, 0))
                population.individuals[sort_index[-3]].image.fill((255, 255, 0))
            else:
                pause_iteration = 0
                population.individuals[sort_index[-1]].image.fill((0, 0, 200))
                population.individuals[sort_index[-2]].image.fill((0, 0, 200))
                population.individuals[sort_index[-3]].image.fill((0, 0, 200))
            
                generation += 1
                print('GENERATIION:', generation)
                # # TODO: add heuristics
                population.updateFitness((630, 240))
                fitnessVal, fitnessSum = population.fitnessProbability()
                sort_index = np.argsort(np.array(fitnessVal))
                new_instructions = ga.update(population.instructions, fitnessVal, fitnessSum)
                # print(np.sum(new_instructions-population.instructions))
                population.instructions = new_instructions
                population.updateInstructions()
                # print('After update:', population.instructions)
                # print('Each individual:', population.individuals[0].instructions)
                population.resetSteps()
                population.resetLives()
                population.resetPositions()

                level.dataLoad("./src/level/level_1.map")
                level.playObstacles()

            # population.individuals[sort_index[-1]].image.fill((0, 0, 0))
            # population.individuals[sort_index[-2]].image.fill((0, 0, 0))
            # population.individuals[sort_index[-3]].image.fill((0, 0, 0))
            # TEST: Show the best fitness
            # population.individuals[sort_index[-1]].image.fill((255, 0, 0))
            # population.individuals[sort_index[-2]].image.fill((255, 127, 0))
            # population.individuals[sort_index[-3]].image.fill((255, 255, 0))


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
        if not FLAG_FAST_TRAINING:
            clock.tick(FPS)



if __name__ == '__main__':
    main()