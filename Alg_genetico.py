from POSSIBLE import DISTRICTS_POINTS as DP
import math
import random


import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
import shapely.geometry 




POPULATION_NUMBER = 1
ITERATIONS = 1

NUMBER_LOCATIONS = len(DP)
NUMBER_AMBUS_TYPE_A = 1
NUMBER_AMBUS_TYPE_B = 3
LOCATIONS = [] 
DISTANCE_MATRIX = []
RAIO = 0.0336
#15min, 30min, 1h
#0.0084, 0.0168, 0.0336
def random_number(start, end):
    return random.randrange(start, end)


class Location:
    def __init__ (self, *args):
        self.id = args[0]
        self.coord_x = args[1]
        self.coord_y = args[2]
        self.weight = args[3]

def calc_distance(x1, y1, x2, y2):
    return pow((pow((x1 - x2),2) + pow((y1 - y2), 2)), 0.5)

def prepare_locations():
    keys = list(DP)

    for i in range(NUMBER_LOCATIONS ):
        local = Location(keys[i], DP[keys[i]][0], DP[keys[i]][1], DP[keys[i]][2])
        LOCATIONS.append(local)

def create_distance_matrix():
    for i in range(NUMBER_LOCATIONS ):
        distances = []
        for j in range(NUMBER_LOCATIONS ):
            distances.append(calc_distance(LOCATIONS[i].coord_x, LOCATIONS[i].coord_y, LOCATIONS[j].coord_x, LOCATIONS[j].coord_y))
        DISTANCE_MATRIX.append(distances)

class Solution:
    def __init__(self):
        self.xA = [0] * len(DP)
        self.xB = [0] * len(DP)
        self.non_zeros_A = []
        self.non_zeros_B = []
        self.rank = 0

    def __lt__(self, other):
        return self.rank < other.rank

    def __gt__(self, other):
        return self.rank > other.rank

def create_solution():
    new_sol = Solution()
    for i in range(NUMBER_AMBUS_TYPE_A):    
        rando_index = random_number(0, NUMBER_LOCATIONS )
        if(rando_index not in new_sol.non_zeros_A):
            new_sol.non_zeros_A.append(rando_index)
            new_sol.xA[rando_index] = 1

    for i in range(NUMBER_AMBUS_TYPE_B):    
        rando_index = random_number(0, NUMBER_LOCATIONS )
        if(rando_index not in new_sol.non_zeros_B):
            new_sol.non_zeros_B.append(rando_index)
            new_sol.xB[rando_index] = 1            
    return new_sol

def evaluate_solution(solution):
    coverage_points = [0]*NUMBER_LOCATIONS
    for j in range(NUMBER_LOCATIONS ):
        for i in range(len(solution.non_zeros_A)):
            if((DISTANCE_MATRIX[solution.non_zeros_A[i]][j] <= RAIO) and ( solution.non_zeros_A[i] != j)):
                #print(f"{DISTANCE_MATRIX[solution.non_zeros_A[i]][j]} < {RAIO}\n")
                if(solution.xA[solution.non_zeros_A[i]] == 1):
                    coverage_points[j] = 1
        for i in range(len(solution.non_zeros_B)):   
            if((DISTANCE_MATRIX[solution.non_zeros_B[i]][j] <= RAIO) and ( solution.non_zeros_B[i] != j)):
                #print(f"{DISTANCE_MATRIX[solution.non_zeros_B[i]][j]} < {RAIO}\n")
                if(solution.xB[solution.non_zeros_B[i]] == 1):
                    coverage_points[j] = 1
   
    for i in range(len(coverage_points)):
        if(LOCATIONS[i].weight != "nan"):
            if(coverage_points[i] == 1 ):
                solution.rank += float(LOCATIONS[i].weight)


def crossover_aux():
    new_value = random_number(0, 1)
    if(new_value == 0):
        return 0
    else:
        return 1

def crossover(base, guia):
    nova = Solution()
    
    for i in range(NUMBER_LOCATIONS):
        if(base.xA[i] == guia.xA[i]):
            nova.xA[i] = (base.xA[i])
            nova.non_zeros_A.append(i)
        elif(base.xA[i] == 1):
            nova.xA[i] = 1
            nova.non_zeros_A.append(i)
        elif(base.xA[i] == 0 and guia.xA[i] != 0):
            nova.xA[i] = (crossover_aux())
            if(nova.xA[i] == 1):
                nova.non_zeros_A.append(i)

        if(base.xB[i] == guia.xB[i] ):
            nova.xB[i] = (base.xB[i])
            if(nova.xA[i] == 1):
                nova.non_zeros_A.append(i)
        elif(base.xB[i] == 1 and guia.xB[i] == 0):
            if(nova.xA[i] == 1):
                nova.xB[i] = 1
                nova.non_zeros_A.append(i)
            else:
                nova.xB[i] = 0
        elif(base.xB[i] == 0 and guia.xB[i] == 1):
            if(nova.xA[i] == 1):
                nova.xB[i] = 1
                nova.non_zeros_A.append(i)
            else:
                nova.xB[i] = 0 
    evaluate_solution(nova)
    return nova

def choose_parent(population):
    temp_pop = []
    sum_rank = 1
    for i in range(POPULATION_NUMBER):   
        sum_rank += population[i].rank  
    for i in range(POPULATION_NUMBER):
        temp_pop.append((population[i].rank)/(sum_rank - 1))   

    rank_benchmark = random.uniform(0, 1)    
    for i in range(POPULATION_NUMBER):
        if( rank_benchmark < temp_pop[i]):
            return population[i]
    j = POPULATION_NUMBER - 1   
    return population[j]



def main():
    random.seed()#669
    #testing 1 , 5 , 4
    prepare_locations()
    create_distance_matrix()
    population = []
    for i in range(POPULATION_NUMBER):
        new_solution = create_solution()

        population.append(new_solution)
        evaluate_solution(population[i])
        #print("--------------------")
        #print(population[i].xA)
        #print("\n")
        #print(population[i].xB)
        #print("--------------------")
        #print(f"Rank: {population[i].rank}")
    
    best_solution_so_far = population[POPULATION_NUMBER - 1]
    print(population[POPULATION_NUMBER - 1].rank)
    for i in range(ITERATIONS):
        print(f"iteration {i}")
        #print(population[POPULATION_NUMBER - 1].non_zeros_A)
        #print(population[POPULATION_NUMBER - 1].non_zeros_B)
        if(best_solution_so_far.rank < population[POPULATION_NUMBER - 1].rank):
            best_solution_so_far = population[POPULATION_NUMBER - 1]
            print(population[POPULATION_NUMBER - 1].rank)
        new_pop = []

        PERCENTAGE_ELITISM = 20#30 #20 #10
        PERCENTAGE_BAD_SOLUTION = 10#10 #10 #20
        PERCENTAGE_NEW_SOLUTIONS = 40#50 #50 #60
        PERCENTAGE_CHILD_SOLUTIONS = 30#10 #20 #10
        # 20 10 30 40 1-16.5 2-18 3-16 4-17.5 5-19 6-16 7-15 8-18.5 9-16.5 10-16.5
       
        amount_elite_ind = int((PERCENTAGE_ELITISM * POPULATION_NUMBER)/100)
        for i in range(amount_elite_ind):
            new_pop.append(population[POPULATION_NUMBER - i - 1])

        amount_bad_ind = int((PERCENTAGE_BAD_SOLUTION * POPULATION_NUMBER)/100)
        for i in range(amount_bad_ind):
            temp_vec = []
            index = random_number(amount_elite_ind , POPULATION_NUMBER - 1)

            while(index in temp_vec):
                index = random_number(amount_elite_ind , POPULATION_NUMBER - 1)
                if( index not in temp_vec):
                    break
            temp_vec.append(index)
            
            new_pop.append(population[index])

        amount_new_ind = int((PERCENTAGE_NEW_SOLUTIONS * POPULATION_NUMBER)/100)
        for i in range(amount_new_ind):
            new_solution = create_solution()
            evaluate_solution(new_solution)

            new_pop.append(new_solution)

        amount_new_ind = int((PERCENTAGE_CHILD_SOLUTIONS * POPULATION_NUMBER)/100)
        for i in range(amount_new_ind):
            if(ITERATIONS > (ITERATIONS*0.5)/100 ):
                parent1 = best_solution_so_far
            parent2 = choose_parent(population)
            
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
    return best_solution_so_far

def plot_sol(best_sol, sol_name):
    # set the filepath and load
    shp_path = "shape//Face_de_Quadra_2023.shp"
    #reading the file stored in variable fp
    map_df = gpd.read_file(shp_path)
    # check data type so we can see that this is not a normal dataframe, but a GEOdataframe

    #print(map_df.sample(5))



    #opening the csv(.shp) file which contains the data to be plotted on the map
    df = gpd.read_file("shape//Face_de_Quadra_2023.shp")

    df.head()



    fig, ax = plt.subplots(1, figsize=(10, 6))


    ax.axis("off")



    circles = []

    for i in range(NUMBER_LOCATIONS):
        if(best_sol.xA[i] == 1 or best_sol.xB[i] == 1):
            circles.append(plt.Circle((LOCATIONS[i].coord_x, LOCATIONS[i].coord_y), RAIO, color='b', fill=False))


    for i in range(len(circles)):
        ax.add_artist(circles[i])
        #ax2.add_artist(points[i])  
    
    
    

    centroids = map_df.centroid
    centroids = centroids.to_crs("wgs84")

    centroids.plot(ax=ax, marker='o', color='red', markersize=5, alpha=0.5) 

    plt.savefig(f"solutions_images/{sol_name}.svg")


# random.seed()#669
# prepare_locations()
# create_distance_matrix()


# test_sol = create_solution()

# print(test_sol.non_zeros_A)
# print(test_sol.non_zeros_B)
# for i in range(NUMBER_LOCATIONS ):
#    if(test_sol.xA[i] == "1" or test_sol.xA[i] == "#"):
#         print(f"{i}  {test_sol.xA[i]}\n")
# for i in range(NUMBER_LOCATIONS ):
#     if(test_sol.xB[i] == "1" or test_sol.xB[i] == "#"):
#         print(f"{i}  {test_sol.xB[i]}\n")


# evaluate_solution(test_sol)
# print(test_sol.rank)


