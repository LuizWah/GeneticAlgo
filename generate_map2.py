import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
from shapely.geometry import Point, Polygon, LineString  
import fiona
import DADOS_2
import shapefile
import testes.quadras as quadras

RAIO = 0.0056
POPS = []
QUADRA = []

class pop:
    def __init__(self, *args):
        self.id = args[0]
        self.position_x = args[1] 
        self.position_y = args[2]
        self.demand = args[3]

    def __lt__(self, other):
        return int(self.id) < int(other.id)

    def __gt__(self, other):
        return int(self.id) > int(other.id)

class quadra():
    def __init__(self, *args):
        self.id = args[0]
        self.position_x = args[1] 
        self.position_y = args[2]
        self.pop_id = args[3]

    def __lt__(self, other):
        return int(self.id) < int(other.id)

    def __gt__(self, other):
        return int(self.id) > int(other.id)



def prepare_locations():
    keys = list(DADOS_2.DISTRICTS_POINTS)   
    for i in range(len(DADOS_2.DISTRICTS_POINTS)):    
        new_local = pop(keys[i], DADOS_2.DISTRICTS_POINTS[keys[i]][0], DADOS_2.DISTRICTS_POINTS[keys[i]][1], DADOS_2.DISTRICTS_POINTS[keys[i]][2])
        POPS.append(new_local)

def prepare_quadras():
    keys = list(quadras.q)   
    for i in range(len(quadras.q)):    
        new_local = quadra(keys[i], quadras.q[keys[i]][0], quadras.q[keys[i]][1], quadras.q[keys[i]][2])
        QUADRA.append(new_local)


prepare_quadras()

QUADRA.sort()


div_index = open("div_index.txt", "a")


for i in range(len(QUADRA)):
    div_index.write(f"'{QUADRA[i].id}' : [{QUADRA[i].position_x}, {QUADRA[i].position_y}, '0'],\n")


# set the filepath and load
shp_path = "shape//Face_de_Quadra_2023//Face_de_Quadra_2023.shp"
#reading the file stored in variable fp
map_df = gpd.read_file(shp_path)
# check data type so we can see that this is not a normal dataframe, but a GEOdataframe

#print(map_df.sample(5))


#opening the csv(.shp) file which contains the data to be plotted on the map
df = gpd.read_file("shape//Face_de_Quadra_2023//Face_de_Quadra_2023.shp")

df.head()

# #selecting the columns required
# df = df[["Pop_setor","Dom_setor"]]
# #renaming the column name
# data_for_map = df.rename(index=str, columns={"Dom_setor": "D_setor","Pop_setor": "P_setor"})

# data_for_map.head()


# # joining the geodataframe with the cleaned up csv dataframe
# merged = map_df.set_index("Dom_setor").join(data_for_map.set_index("D_setor"))
# #.head() returns the top 5(by default ) lines of the dataframe
# print(merged.head())



# set a variable that will call whatever column we want to visualise on the map
variable = 'P_setor'
# set the range for the choropleth
vmin, vmax = 120, 220
# create figure and axes for Matplotlib
fig, ax = plt.subplots(1, figsize=(10, 6))



# pontos = gpd.read_file("shape//Equipamentos_Saude_2023_apenas_samu.shp")

# pontos = pontos.to_crs("wgs84")
# base = merged.plot(column=variable, cmap='Greens', linewidth=0.8, ax=ax, edgecolor='0.8', legend=True, missing_kwds={
#         "color": "lightgrey",
#         "edgecolor": "green",
#         "hatch": "///",
#         "label": "Missing values",
#     },)


# ax.axis("off")


# pontos.plot(ax=ax, marker='o', color='blue', markersize=5)

# centroids = map_df.centroid
# centroids = centroids.to_crs("wgs84")

# centroids.plot(ax=ax, marker='o', color='red', markersize=5)



# f = open("quadras.py", "a")
# g = open("ids.txt", "r").read().split('\n')
# i = 0
# for line in g:
#     string = centroids[i]
#     f.write(f"'{line}' : [{string.x}, {string.y}, '0'],\n")
#     i += 1

# plt.show()

