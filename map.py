import geopandas as gpd
import geoplot
import geoplot.crs as gcrs
import matplotlib.pyplot as plt

data = gpd.read_file(
    "/home/amaru/Literacy_Database/MS_Lit/project/static/ms_map.geojson"
)

geoplot.polyplot(
    data,
    projection=gcrs.AlbersEqualArea(),
    edgecolor='darkgrey',
    facecolor='lightgrey',
    linewidth=.3,
    figsize=(12, 8)
)

print(type(data))

plt.show()
