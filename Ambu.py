
import random
import DADOS
import math

import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
import shapely.geometry 




MUTATION_RATE = 0.1
POPULATION_NUMBER = 300
NUMBER_POSIBLE_LOCATIONS = 40
ITERATIONS = 200
PROBLEMA = [] 
ITERATION_UNTIL_NATURAL_DISASTER = 2000 
PERCENTAGE_OF_DEATHS_BY_DISASTER = 20
DISTANCE_MATRIX = []



NUMERO_AMBU_TIPO_A = 10
NUMERO_AMBU_TIPO_B = 10
RAIO = 200
PI = 3.14

class Local:
    def __init__(self, *args):
        self.id = args[0]
        self.position_x = args[1] 
        self.position_y = args[2]
        self.demand = args[3]
       
      
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
    new_solution.number_type_A = generate_number(5, NUMERO_AMBU_TIPO_A)
    new_solution.number_type_B = generate_number(5, NUMERO_AMBU_TIPO_B)
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
        
def prepare_locations():
    keys = list(DADOS.PONTOS)   
    for i in range(NUMBER_POSIBLE_LOCATIONS):    
        new_local = Local(keys[i], DADOS.PONTOS[keys[i]][0], DADOS.PONTOS[keys[i]][1], DADOS.PONTOS[keys[i]][2])
        PROBLEMA.append(new_local)



def calc_distance(points_index_1, points_index_2):
    x = pow((PROBLEMA[points_index_1].position_x - PROBLEMA[points_index_2].position_x), 2)     
    y = pow((PROBLEMA[points_index_1].position_y - PROBLEMA[points_index_2].position_y), 2)     
    distance = pow((x + y), 0.5)
    
    return distance     
       
def create_distance_matrix():
    for i in range(NUMBER_POSIBLE_LOCATIONS):
        distances = []
        for j in range(NUMBER_POSIBLE_LOCATIONS):
            distances.append(calc_distance(i, j))
        DISTANCE_MATRIX.append(distances)  
       
def get_intersections(x0, y0, x1, y1):
    d=math.sqrt((x1-x0)**2 + (y1-y0)**2)
    
    a=(RAIO**2-RAIO**2+d**2)/(2*d)
    h=math.sqrt(RAIO**2-a**2)
    x2=x0+a*(x1-x0)/d   
    y2=y0+a*(y1-y0)/d   
    x3=x2+h*(y1-y0)/d     
    y3=y2-h*(x1-x0)/d 

    x4=x2-h*(y1-y0)/d
    y4=y2+h*(x1-x0)/d
        
    return (x3, y3, x4, y4)       
       
                   
def calc_penalties(solution):
    penalty = 0
    for i in range(NUMBER_POSIBLE_LOCATIONS):
        if(solution.xB[i] == '1'):#condition to satisfy
            for j in range(NUMBER_POSIBLE_LOCATIONS):
                if(DISTANCE_MATRIX[i][j] < 2*RAIO and i != j and solution.xB[j] == '1'):
                    #calc coords pontos intercesão
                    inter_points = get_intersections(PROBLEMA[i].position_x, PROBLEMA[i].position_y, PROBLEMA[j].position_x, PROBLEMA[j].position_y)
                    #calc corda
                    corda = pow(pow(inter_points[0] - inter_points[2], 2) + pow(inter_points[1] - inter_points[3],2),0.5)
                    
                    #calc setor
                    side1 =  2*(RAIO*RAIO) - (corda*corda)
                    side2 = 2*(RAIO*RAIO)
                    theta = math.acos(side1/side2)
                    
                    #print(theta)
                    #print("------")
                    #print(side1/side2)
                    #print("------")
                    setor = (theta*math.pi*(RAIO*RAIO))/(2*math.pi)
                    
                    #calc triangulo
                    altura = pow(RAIO*RAIO - corda*corda/4, 0.5)
                    triangulo = (corda*altura)/2
                    #calc segmento
                    segmento = setor - triangulo
                    penalty += 2*segmento  
                    
    print(f"penaçlty === {penalty}")                  
    return penalty                          
                
           
def calc_area(solution): 
    number_location_satisfied = 0
    for i in range(NUMBER_POSIBLE_LOCATIONS):
        if(solution.xB[i] == solution.xA[i] == '1'):#condition to satisfy
            number_location_satisfied += 1
        elif(solution.xB[i] == '1'):
            number_location_satisfied += 0.5    
    area = math.pi*RAIO*RAIO*number_location_satisfied
    return area
      
def calculate_rank(solution):
    solution.rank = calc_area(solution) - calc_penalties(solution)  
  
  
  
  
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
    #random.seed(8)
    #testing 1 , 5 , 4
    prepare_locations()
    create_distance_matrix()
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

    circles = []

    for i in range(NUMBER_POSIBLE_LOCATIONS):
        if(best_solution_so_far.xB[i] == '1'):
            circles.append(plt.Circle((PROBLEMA[i].position_x, PROBLEMA[i].position_y), RAIO, color='b', fill=False))


    fig, ax = plt.subplots()  

    ax.set_xlim((-1000, 1000))
    ax.set_ylim((-1000, 1000))

    for i in range(len(circles)):
        ax.add_artist(circles[i])
        #ax2.add_artist(points[i])

    plt.gca().set_aspect('equal', adjustable='box')

    plt.show()


main()


  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
#main           
# prepare_locations()           
# create_distance_matrix()

# sol = create_solution()
# calculate_rank_2(sol)

# print(sol.rank)  
# print(sol.xB)

#everything below is plotting


# circles = []

# for i in range(NUMBER_POSIBLE_LOCATIONS):
#     if(sol.xB[i] == '1'):
#         circles.append(plt.Circle((PROBLEMA[i].position_x, PROBLEMA[i].position_y), RAIO, color='b', fill=False))


# fig, ax = plt.subplots()  

# ax.set_xlim((-1000, 1000))
# ax.set_ylim((-1000, 1000))

# for i in range(len(circles)):
#     ax.add_artist(circles[i])
#     #ax2.add_artist(points[i])

# plt.gca().set_aspect('equal', adjustable='box')

# plt.show()


