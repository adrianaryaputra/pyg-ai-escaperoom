import numpy as np
import random





class simpleGA:
    def __init__(self, num_individual: int) -> None:
        self.num_individual = num_individual
        self.random_seed = None

        ## Hyperparameters
        self.num_selection = 10
        self.r_crossover = 0.8
        self.r_mutation = 0.05
        # self.selection = self.selection_roulette
        self.selection = self.selection_ranking
        self.crossover = self.crossover_one_point
        self.mutation = self.mutation_instruction
        
    def update(self, instructions, fitnessVal, fitnessSum):
        arrSelected = self.selection(fitnessVal, fitnessSum, self.random_seed, self.num_selection, instructions)
        arrSelected = self.crossover(arrSelected, self.num_individual, self.r_crossover)
        arrSelected = self.mutation(arrSelected, self.r_mutation)
        return np.array(arrSelected)

    @staticmethod
    def selection_roulette(fitnessValue, fitnessSum, random_seed, num_selection, instructions):
        '''
        '''
        if random_seed is not None:
            np.random.seed(random_seed)
        rand_val = np.random.rand(num_selection) * fitnessSum
        arrSelected = []
        for val in rand_val:
            fitnessCum = 0 
            for n in range(len(fitnessValue)):
                fitnessCum += fitnessValue[n]
                if fitnessCum > val:
                    arrSelected.append(instructions[n])
                    break
        return arrSelected
    
    
    @staticmethod
    def selection_ranking(fitnessValue, fitnessSum, random_seed, num_selection, instructions):
        '''
        '''
        idx_sort = np.argsort(np.array(fitnessValue))[::-1]
        return instructions[idx_sort][:num_selection]

    @staticmethod
    def crossover_one_point(arrSelected, num_individual, r_cross=0.3):
        arrSelectedNew = []
        for i in range(num_individual):
            parent1, parent2 = random.sample(list(arrSelected), 2)
            if np.random.rand() < r_cross:
                new_pop1, new_pop2 = parent1.copy(), parent2.copy()
                idx_split = np.random.randint(1, len(parent1) - 2)
                new_pop1 = list(parent1[:idx_split]) + list(parent2[idx_split:])
                idx_split = np.random.randint(1, len(parent1) - 2)
                new_pop2 = list(parent2[:idx_split]) + list(parent1[idx_split:])
                arrSelectedNew.append(np.array(new_pop1))
                arrSelectedNew.append(np.array(new_pop2))
            else:
                arrSelectedNew.append(np.array(parent1))
                arrSelectedNew.append(np.array(parent2))

        # Check only take new population with same num pop as before
        arrSelectedNew = random.sample(arrSelectedNew, num_individual)
        return arrSelectedNew

    @staticmethod
    def mutation_instruction(arrSelected, r_mutation=0.05):
        max_value = np.max(arrSelected)
        for i in range(len(arrSelected)):
            for j in range(len(arrSelected[i])):
                if np.random.rand() < r_mutation:
                    # random x instruction
                    random_state = np.random.randint(3)
                    if random_state == 0:
                        x = 0
                    elif random_state == 1:
                        x = max_value
                    else:
                        x = -max_value

                    # random y instruction
                    random_state = np.random.randint(3)
                    if random_state == 0:
                        y = 0
                    elif random_state == 1:
                        y = max_value
                    else:
                        y = -max_value

                    ## mutation 
                    arrSelected[i][j] = [x, y]
        return arrSelected