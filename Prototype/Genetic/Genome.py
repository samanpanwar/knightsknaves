import random
from . import functions as f
from . import global_variables as gv

class Genome(object):
    def __init__(self, eqn):
        self.eqn = eqn
        self.variables = [_ for _ in gv.VARIABLES if _ is not '1']
        self.possible_variables = gv.VARIABLES + [f.negate(_) for _ in gv.VARIABLES]
        self.fitness_score = 0
        self.truth_values = []
        self.history = [self.eqn]
        self.parents = []


    def calculate_fitness(self):
        score, count = 0, 0
        self.truth_values = [] 
        for row in f.truth_table(gv.PEOPLE_COUNT):
            truth_dict = {a:b for a, b in zip(self.variables, row)}
            eval_result = True
            for claim in self.eqn:
                eval_result &= f.evaluate(claim, truth_dict)
            if eval_result:
                self.truth_values.append(list(row))
                score += f.similarity_score(gv.ASSUMED_ANSWER, row)
                count += 1

        if count is not 0:
            self.fitness_score = score / count
        else:
            self.fitness_score -= 10.0
        
        truth_values = {a:b for a,b in zip(self.variables, gv.ASSUMED_ANSWER)}
        if f.is_illegal(self.eqn, truth_values):
            self.fitness_score -= 10.0


    def crossover(self, g, method="1p"):
        i, j = Genome(self.eqn), Genome(g.eqn)
        i.parent = [self.eqn, g.eqn, self.history, g.history]
        j.parent = [self.eqn, g.eqn, self.history, g.history]
        if method is "1p":
            for ind, (a, b) in enumerate(zip(i.eqn, j.eqn)):
                crossover_point = random.randint(0, len(a)-1)
                if random.choice([True, False]):
                    i.eqn[ind][:crossover_point], j.eqn[ind][:crossover_point] = j.eqn[ind][:crossover_point], i.eqn[ind][:crossover_point]
                    
        return i, j


    def mutate(self):
        i, j = random.randint(0, gv.PEOPLE_COUNT-1), random.randint(0, gv.PEOPLE_COUNT*2-2)
        ch = self.eqn[i][j]

        if ch in gv.OPERAND:
            self.eqn[i][j] = f.negate(ch)
        else:

            contendor = self.possible_variables.copy()
            for var in self.eqn[i][::2]:
                try:
                    contendor.remove(f.negate(var))
                    contendor.remove(var)
                except:
                    print(contendor, f.negate(var), self.eqn[i])
                    raise
            contendor.append(f.negate(ch))
            new_ch = random.choice(contendor)
            self.eqn[i][j] = new_ch
    

    def __repr__(self):
        eqn = " ; ".join(["".join(_) for _ in self.eqn])
        repr_str = f'B_eqn : {eqn} '
        if self.fitness_score is not None:
            f_score = round(self.fitness_score, 3)
            repr_str += f'\t fitness_score : {f_score}'
            repr_str += f'\tTT : {self.truth_values}'
        return repr_str


# Functions to Generate population
def generate_random_population(N):
    population = []
    for _ in range(N):
        eqn = f.random_equation(gv.BLOCK_SIZE, gv.PEOPLE_COUNT)
        g = Genome(eqn)
        population.append(g)
    return population


# Sampling Functions for Selection
def SUS(population, N):
    """Stochastic Universal Sampling"""
    random.shuffle(population)
    F = sum([_.fitness_score for _ in population])
    P = int(F/N)
    start = random.uniform(0, P)
    pointers = [start + i*P for i in range(N)]
    return RWS(population, pointers)


def RWS(population, pointers):
    """Roulette Wheel Selection"""
    keep = []
    fit_sum, i = 0, 0
    for p in pointers:
        while(fit_sum < p):
            i += 1
            fit_sum += population[i].fitness_score
        keep.append(population[i])
    return keep
