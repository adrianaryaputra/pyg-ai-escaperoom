import pygame
import numpy as np
import math


class simpleGA:
    def __init__(self, num_individual: int) -> None:
        self.num_individual = num_individual
        

    def update(self, instructions, fitnessVal, fitnessSum):
        self.instructions = instructions
        self.selection(fitnessVal, fitnessSum)
        self.crossover()
        self.mutation()

    def selection(self, fitnessVal, fitnessSum, num_selection: int = 1, random_seed: int = None):
        if random_seed is not None:
            np.random.seed(random_seed)
        rand_val = np.random.rand(num_selection)*fitnessSum
        selected = []
        for val in rand_val:
            fitnessCum = float(0)
            for n in range(len(fitnessVal)):
                fitnessCum += fitnessVal[n]
                if fitnessCum > val:
                    selected.append(self.instructions[n])
        self.selected = selected

    def crossover(self):
        pass