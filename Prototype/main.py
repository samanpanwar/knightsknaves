import random
import itertools
from argparse import ArgumentParser

import Genetic.functions as f
import Genetic.Genome as G
import Genetic.global_variables as gv
import Genetic.sentence_formation as sf


def check_for_answer(elite):
    for gene in elite:
        if len(gene.truth_values) == 1 and gene.fitness_score >= 0:
            if gene.truth_values[0] == gv.ASSUMED_ANSWER:
                return gene
    return None
    

def create_boolean_question(population_size=50, number_of_people=3):

    # Setting Global Variables
    gv.POPULATION_SIZE = 50
    gv.PEOPLE_COUNT = number_of_people
    gv.BLOCK_SIZE = gv.PEOPLE_COUNT
    gv.VARIABLES = gv.ALL_VARIABLES[:gv.PEOPLE_COUNT*2-1]
    ten, thirty = int(gv.POPULATION_SIZE*0.1), int(gv.POPULATION_SIZE*0.3)

    # Make up a new Answer
    gv.ASSUMED_ANSWER = [random.choice([True, False]) for _ in range(gv.PEOPLE_COUNT)]

    # Initial Random population
    starting_population = G.generate_random_population(gv.POPULATION_SIZE)

    population = starting_population.copy()
    gen_count = 0
    
    while(True):
        # Genration Statisticss
        gen_count += 1
        print("Running Genration ",gen_count," ...")
         
        # Calculate Fitness
        for g in population:
            g.calculate_fitness()

        next_gen = []
        population.sort(key=lambda x:x.fitness_score, reverse=True)
         
        # Pick Elite
        elite = population[:ten]
        
        # Check for exit condition:
        ANSWER = check_for_answer(elite)
        if ANSWER is not None:
            break
        
        selected = G.SUS(population[ten:], thirty)
        
        # Crossover
        crossed_over = []
        for _ in selected:
            p1, p2 = random.sample(selected, 2)
            c1, c2 = p1.crossover(p2)
            crossed_over.extend([c1, c2])

       # Mutation
        for _ in crossed_over:
            g = random.choice(crossed_over)
            g.mutate()

        next_gen = elite + crossed_over + G.generate_random_population(N=ten)
        population = next_gen
        
       # End of Loop

    q_eqn = []

    # negate the block for Knaves (since knaves always lie).
    for truth_val, eqn in zip(gv.ASSUMED_ANSWER, ANSWER.eqn):
        if not truth_val:
             eqn = f.negate_equation(eqn)
        q_eqn.append(eqn)
    
    QUESTION = G.Genome(q_eqn)
    print("Bool Answer   : ", ANSWER)
    print("Bool Question : ", QUESTION)
    return QUESTION
             

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-ps", "--population-size", dest="population_count", default=50,
                        help="Population size for initial genetic algo population")
    parser.add_argument("-np", "--number-of-people", dest="number_of_people", default=3,
                        help="Total number of inhabitant on the island")
    args = parser.parse_args()
    
    while(True):
        try:
            create_boolean_question(int(args.population_count), int(args.number_of_people))
            break
        except ValueError:
            print("Error Occured")
