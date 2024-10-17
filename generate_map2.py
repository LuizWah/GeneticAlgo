import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
from shapely.geometry import Point, Polygon, LineString  


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



pontos = gpd.read_file("shape//Equipamentos_Saude_2023.shp")

pontos = pontos.to_crs("wgs84")
base = merged.plot(column=variable, cmap='Greens', linewidth=0.8, ax=ax, edgecolor='0.8', legend=True, missing_kwds={
        "color": "lightgrey",
        "edgecolor": "red",
        "hatch": "///",
        "label": "Missing values",
    },)


ax.axis("off")


pontos.plot(ax=ax, marker='o', color='blue', markersize=5)

centroids = map_df.centroid
centroids = centroids.to_crs("wgs84")

# f = open("DADOS_3.py", "a")
# g = open("DADOS_2.py")
# last_string = g.readlines()
# string = "0"
# for i in range(413): 
#     if(i > 0):
#         string =  (last_string[i].strip('\n'))[: len(last_string[i]) - 3] + str(data_for_map["P_setor"][i -1]).strip('\n') + "],"
#         f.write(f"{string}")
#         f.write("\n")
    
# f.close()




centroids.plot(ax=ax, marker='o', color='red', markersize=5)

plt.show()

