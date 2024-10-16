import random
import DADOS

MUTATION_RATE = 0.1
POPULATION_NUMBER = 150
NUMBER_POSIBLE_LOCATIONS = 40
ITERATIONS = 2000
PROBLEMA = [] 
ITERATION_UNTIL_NATURAL_DISASTER = 2000 
PERCENTAGE_OF_DEATHS_BY_DISASTER = 20

NUMERO_AMBU_TIPO_A = 20
NUMERO_AMBU_TIPO_B = 20


class Local:
    def __init__(self, *args):
        self.id = args[0]
        self.position_x = args[1] 
        self.position_y = args[2]
        self.demand = args[3]
        
def prepare_locations():
    keys = list(DADOS.PONTOS)   
    for i in range(NUMBER_POSIBLE_LOCATIONS):    
        new_local = Local(keys[i], DADOS.PONTOS[keys[i]][0], DADOS.PONTOS[keys[i]][1], DADOS.PONTOS[keys[i]][2])
        PROBLEMA.append(new_local)
        
        
class Solution:
    def __init__(self):
        self.xA = []
        self.xB = []
        self.number_type_A = 0
        self.number_type_B = 0
        for i in range(NUMBER_POSIBLE_LOCATIONS):
            self.xA.append('0')
            self.xB.append('0')
            
        self.rank = 0

    def __lt__(self, other):
        return self.rank < other.rank

    def __gt__(self, other):
        return self.rank > other.rank


def generate_number(start, end):
    return random.randrange(start, end)

def create_solution():
    new_solution = Solution()
    new_solution.number_type_A = generate_number(0, NUMERO_AMBU_TIPO_A )
    new_solution.number_type_B = generate_number(0, NUMERO_AMBU_TIPO_B)
    #print(f"\nnumber_type_A {new_solution.number_type_A}, number_type_B {new_solution.number_type_B}\n")
    for i in range(new_solution.number_type_A):
        new_index = generate_number(0, NUMBER_POSIBLE_LOCATIONS - 1)
        while(new_solution.xA[new_index] == '1' or new_solution.xA[new_index] == '#'):
            new_index = generate_number(0, NUMBER_POSIBLE_LOCATIONS - 1)
            if(new_solution.xA[new_index] == '0'):
                break
        new_symbol = generate_number(0, 10)  
        if(new_symbol < 2):
            new_solution.xA[new_index] = '#'
        else:    
            new_solution.xA[new_index] = '1'

    for i in range(new_solution.number_type_B):
        new_index = generate_number(0, NUMBER_POSIBLE_LOCATIONS - 1)
        while(new_solution.xB[new_index] == '1' or new_solution.xB[new_index] == '#'):
            new_index = generate_number(0, NUMBER_POSIBLE_LOCATIONS - 1)                    
            if(new_solution.xB[new_index] == '0'):
                break
        new_symbol = generate_number(0, 10)  
        if(new_symbol < 2):
            new_solution.xB[new_index] = '#' 
        else:          
            new_solution.xB[new_index] = '1'

    return new_solution
             
def calculate_rank(solution):
    for i in range(NUMBER_POSIBLE_LOCATIONS):
        if(solution.xA[i] == solution.xB[i] == '1'):
            solution.rank += PROBLEMA[i].demand
        elif(solution.xB[i] == '1'):    
            solution.rank += PROBLEMA[i].demand*0.5
        #elif(solution.xA[i] == '1' and solution.xB[i] == '#'):  
            #solution.rank += (PROBLEMA[i].demand)*0.5
        #elif(solution.xA[i] == '#' and solution.xB[i] == '1'):
            #solution.rank += (PROBLEMA[i].demand)*0.5
        
def choose_parent(population):
    temp_pop = []
    sum_rank = 0
    for i in range(POPULATION_NUMBER):   
        sum_rank += population[i].rank    
    for i in range(POPULATION_NUMBER):
        temp_pop.append((population[i].rank)/sum_rank)   

    rank_benchmark = random.uniform(0, 1)    
    for i in range(POPULATION_NUMBER):
        if( rank_benchmark < temp_pop[i]):
            return population[i]
    return population[POPULATION_NUMBER - 1]

def crossover_aux():
    new_value = generate_number(0, 1)
    if(new_value == 0):
        return '0'
    else:
        return '1'

def crossover(base, guia):
    nova = Solution()
    for i in range(NUMBER_POSIBLE_LOCATIONS):
        if(base.xA[i] == guia.xA[i]):
            nova.xA[i] = (base.xA[i])
        elif(base.xA[i] == '1'):
            nova.xA[i] = (base.xA[i])
        elif(base.xA[i] == '#'):
            nova.xA[i] = (crossover_aux())
        elif(base.xA[i] == '0' and guia.xA[i] != '0'):
            nova.xA[i] = (crossover_aux())


        if(base.xB[i] == guia.xB[i] ):
            nova.xB[i] = (base.xB[i])
        elif(base.xB[i] == '1' and guia.xB[i] == '0'):
            if(nova.xA[i] == '1'):
                nova.xB[i] = ('1')
            else:
                nova.xB[i] = ('0')
        elif(base.xB[i] == '1' and guia.xB[i] == '#'):
            if(nova.xA[i] == '1'):
                nova.xB[i] = ('1')
            else:
                nova.xB[i] = (crossover_aux())  
        elif(base.xB[i] == '#' and guia.xB[i] == '1'):
            if(nova.xA[i] == '1'):
                nova.xB[i] = ('1')
            else:
                nova.xB[i] = (crossover_aux())  
        elif(base.xB[i] == '#' and guia.xB[i] == '0'):
            if(nova.xA[i] == '#'):
                nova.xB[i] = ('#')
            else:
                nova.xB[i] = (crossover_aux())   
        elif(base.xB[i] == '0' and guia.xB[i] == '1'):
            if(nova.xA[i] == '1'):
                nova.xB[i] = ('1')
            else:
                nova.xB[i] = ('0') 
        if(base.xB[i] == '0' and guia.xB[i] == '#'):
            if(nova.xA[i] == '1'):
                nova.xB[i] = ('1')
            else:
                nova.xB[i] = (crossover_aux())                                 

    calculate_rank(nova)
    return nova

def main():
    #random.seed(8031)
    prepare_locations()
    
    population = []
    for i in range(POPULATION_NUMBER):
        new_solution = create_solution()

        population.append(new_solution)
        calculate_rank(population[i])
        #print("--------------------")
        #print(population[i].xA)
        #print("\n")
        #print(population[i].xB)
        #print("--------------------")
        #print(f"Rank: {population[i].rank}")
    
    best_solution_so_far = population[POPULATION_NUMBER - 1]
    print(population[POPULATION_NUMBER - 1].rank)
    for i in range(ITERATIONS):
        if(best_solution_so_far.rank < population[POPULATION_NUMBER - 1].rank):
            best_solution_so_far = population[POPULATION_NUMBER - 1]
            print(population[POPULATION_NUMBER - 1].rank)
        new_pop = []

        PERCENTAGE_ELITISM = 20
        PERCENTAGE_BAD_SOLUTION = 10
        PERCENTAGE_NEW_SOLUTIONS = 30
        PERCENTAGE_CHILD_SOLUTIONS = 40
        # 20 10 30 40 1-16.5 2-18 3-16 4-17.5 5-19 6-16 7-15 8-18.5 9-16.5 10-16.5
       
        amount_elite_ind = int((PERCENTAGE_ELITISM * POPULATION_NUMBER)/100)
        for i in range(amount_elite_ind):
            new_pop.append(population[POPULATION_NUMBER - i - 1])

        amount_bad_ind = int((PERCENTAGE_BAD_SOLUTION * POPULATION_NUMBER)/100)
        for i in range(amount_bad_ind):
            temp_vec = []
            index = generate_number(amount_elite_ind , POPULATION_NUMBER - 1)

            while(index in temp_vec):
                index = generate_number(amount_elite_ind , POPULATION_NUMBER - 1)
                if( index not in temp_vec):
                    break
            temp_vec.append(index)
            
            new_pop.append(population[index])

        amount_new_ind = int((PERCENTAGE_NEW_SOLUTIONS * POPULATION_NUMBER)/100)
        for i in range(amount_new_ind):
            new_solution = create_solution()
            calculate_rank(new_solution)

            new_pop.append(new_solution)

        amount_new_ind = int((PERCENTAGE_CHILD_SOLUTIONS * POPULATION_NUMBER)/100)
        for i in range(amount_new_ind):
            parent1 = choose_parent(population)
            parent2 = choose_parent(population)
            if(parent1.rank > parent2.rank):
                temp = parent1
                parent1 = parent2
                parent2 = temp
            new_solution = crossover(parent1, parent2)
            new_pop.append(new_solution)

        new_pop.sort()
        population = new_pop

       
    print(f"\n----------------------\nRANKING OF BEST SOLUTION: {best_solution_so_far.rank}\n----------------------\n")
    print(f"Vetor xA: {best_solution_so_far.xA}\n")
    print(f"Vetor xB: {best_solution_so_far.xB}\n")
    #new_child = crossover(population[POPULATION_NUMBER - 1], population[POPULATION_NUMBER - 2])
    #print(new_child.xA)
    #print("---------------------")
    #print(new_child.xB)
    #print("---------------------")
    #print(new_child.rank)




main()

