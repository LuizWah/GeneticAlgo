import random
import DADOS_2
import math

import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
import shapely.geometry 




MUTATION_RATE = 0.1
POPULATION_NUMBER = 500
NUMBER_POSIBLE_LOCATIONS = len(DADOS_2.DISTRICTS_POINTS)
ITERATIONS = 200

PROBLEMA = [] 
DISTANCE_MATRIX = []

NUMERO_AMBU_TIPO_A = 36
NUMERO_AMBU_TIPO_B = 36

TEMPO = 15#minutos
RAIO = 0.0056
VELOCIDADE = 36#km/h

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
    new_solution.number_type_A = NUMERO_AMBU_TIPO_A 
    new_solution.number_type_B = NUMERO_AMBU_TIPO_B 
    #print(f"\nnumber_type_A {new_solution.number_type_A}, number_type_B {new_solution.number_type_B}\n")
    for i in range(new_solution.number_type_A):
        new_index = generate_number(0, NUMBER_POSIBLE_LOCATIONS - 1)
        while(new_solution.xA[new_index] == '1' or new_solution.xA[new_index] == '#'):
            new_index = generate_number(0, NUMBER_POSIBLE_LOCATIONS - 1)
            if(new_solution.xA[new_index] == '0'):
                break
        new_symbol = generate_number(0, 10)  
    
        new_solution.xA[new_index] = '1'
        new_solution.xB[new_index] = '1'
    

    return new_solution       
        
def prepare_locations():
    keys = list(DADOS_2.DISTRICTS_POINTS)   
    for i in range(NUMBER_POSIBLE_LOCATIONS):    
        new_local = Local(keys[i], DADOS_2.DISTRICTS_POINTS[keys[i]][0], DADOS_2.DISTRICTS_POINTS[keys[i]][1], DADOS_2.DISTRICTS_POINTS[keys[i]][2])
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
       
                           
def calc_rank_aux(solution): 
    demand_satisfied = 0
    points_satisfied = [0]* NUMBER_POSIBLE_LOCATIONS
    for i in range(NUMBER_POSIBLE_LOCATIONS):
        if((solution.xB[i] == '1' ) and (PROBLEMA[i].demand != "nan")):#condition to satisfy
            for j in range(NUMBER_POSIBLE_LOCATIONS):
                if(DISTANCE_MATRIX[i][j] <= RAIO):
                    points_satisfied[i] = 1
                    #demand_satisfied += PROBLEMA[i].demand * 1
                    
                               
                        
    for i in range(NUMBER_POSIBLE_LOCATIONS):
        if(points_satisfied[i] == 1):
            demand_satisfied += PROBLEMA[i].demand       
    return demand_satisfied
      
def calculate_rank(solution):
    solution.rank = calc_rank_aux(solution) 
  
  
  
  
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
    j = generate_number(POPULATION_NUMBER%3, POPULATION_NUMBER - 1)    
    return population[j]

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
    random.seed(123)#669
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

        PERCENTAGE_ELITISM = 10#30 #20 #10
        PERCENTAGE_BAD_SOLUTION = 10#10 #10 #20
        PERCENTAGE_NEW_SOLUTIONS = 30#50 #50 #60
        PERCENTAGE_CHILD_SOLUTIONS = 50#10 #20 #10
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
    
best_sol = main()

def max_satisfaction():
    sat = 0
    for i in range(NUMBER_POSIBLE_LOCATIONS):
        if(PROBLEMA[i].demand != "nan"):
            sat += PROBLEMA[i].demand
    return sat    
print(f"percentage of coverage ={(best_sol.rank/max_satisfaction())*100}")





# set the filepath and load
shp_path = "shape//IBGE_Pop_Dom_2010.shp"
#reading the file stored in variable fp
map_df = gpd.read_file(shp_path)
# check data type so we can see that this is not a normal dataframe, but a GEOdataframe

#print(map_df.sample(5))



#opening the csv(.shp) file which contains the data to be plotted on the map
df = gpd.read_file("shape//IBGE_Pop_Dom_2010.shp")

df.head()

#selecting the columns required
df = df[["Pop_setor","Dom_setor"]]
#renaming the column name
data_for_map = df.rename(index=str, columns={"Dom_setor": "D_setor","Pop_setor": "P_setor"})

data_for_map.head()


# joining the geodataframe with the cleaned up csv dataframe
merged = map_df.set_index("Dom_setor").join(data_for_map.set_index("D_setor"))
#.head() returns the top 5(by default ) lines of the dataframe
print(merged.head())



# set a variable that will call whatever column we want to visualise on the map
variable = 'P_setor'
# set the range for the choropleth
vmin, vmax = 120, 220
# create figure and axes for Matplotlib
fig, ax = plt.subplots(1, figsize=(10, 6))


base = merged.plot(column=variable, cmap='Greens', linewidth=0.8, ax=ax, edgecolor='0.8', legend=True, missing_kwds={
        "color": "lightgrey",
        "edgecolor": "green",
        "hatch": "///",
        "label": "Missing values",
    },)


ax.axis("off")



circles = []

for i in range(NUMBER_POSIBLE_LOCATIONS):
    if(best_sol.xB[i] == '1'):
        circles.append(plt.Circle((PROBLEMA[i].position_x, PROBLEMA[i].position_y), RAIO, color='b', fill=False))


for i in range(len(circles)):
    ax.add_artist(circles[i])
    #ax2.add_artist(points[i])  
  
  
  

centroids = map_df.centroid
centroids = centroids.to_crs("wgs84")

centroids.plot(ax=ax, marker='o', color='red', markersize=5)

plt.show()
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
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


