import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
from shapely.geometry import Point, Polygon, LineString  
import fiona
import testes.DADOS_EQUIPAMENTSOS_SAUDE as DADOS_EQUIPAMENTSOS_SAUDE


RAIO = 0.0056
AMBUS = []

class Local:
    def __init__(self, *args):
        self.id = args[0]
        self.position_x = args[1] 
        self.position_y = args[2]
        self.demand = args[3]
       
def prepare_locations():
    keys = list(DADOS_EQUIPAMENTSOS_SAUDE.PONTOS)   
    for i in range(len(DADOS_EQUIPAMENTSOS_SAUDE.PONTOS)):    
        new_local = Local(keys[i], DADOS_EQUIPAMENTSOS_SAUDE.PONTOS[keys[i]][0], DADOS_EQUIPAMENTSOS_SAUDE.PONTOS[keys[i]][1], DADOS_EQUIPAMENTSOS_SAUDE.PONTOS[keys[i]][2])
        AMBUS.append(new_local)




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



pontos = gpd.read_file("shape//Equipamentos_Saude_2023_apenas_samu.shp")

pontos = pontos.to_crs("wgs84")
base = merged.plot(column=variable, cmap='Greens', linewidth=0.8, ax=ax, edgecolor='0.8', legend=True, missing_kwds={
        "color": "lightgrey",
        "edgecolor": "green",
        "hatch": "///",
        "label": "Missing values",
    },)


ax.axis("off")


pontos.plot(ax=ax, marker='o', color='blue', markersize=5)

circles = []
prepare_locations()
for i in range(len(DADOS_EQUIPAMENTSOS_SAUDE.PONTOS)):
    circles.append(plt.Circle((AMBUS[i].position_x, AMBUS[i].position_y), RAIO, color='blue', fill=False))

for i in range(len(circles)):
    ax.add_artist(circles[i])
    #ax2.add_artist(points[i])


centroids = map_df.centroid
centroids = centroids.to_crs("wgs84")

centroids.plot(ax=ax, marker='o', color='red', markersize=5)


plt.show()

