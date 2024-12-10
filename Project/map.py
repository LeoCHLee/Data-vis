import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from matplotlib.patches import Polygon

# Create the figure and Basemap
plt.figure(figsize=(15, 10))
m = Basemap(projection='mill', llcrnrlat=-60, urcrnrlat=90, llcrnrlon=-180, urcrnrlon=180)

# Draw the map boundary and coastlines
m.drawmapboundary(fill_color='lightblue')
m.fillcontinents(color='lightgrey', lake_color='lightblue', zorder=0)
m.drawcoastlines(linewidth=0.5)

# Read the shapefile for country boundaries (built into Basemap)
m.readshapefile(r'C:\Users\leo22\Desktop\Trinity SF Version\Year 4\Data Visualisation\Project\state_map-master\st99_d00', name='countries', drawbounds=True)

# Assign colors to specific regions
for info, shape in zip(m.countries_info, m.countries):
    # Make Ireland red
    if info['NAME'] == 'Ireland':
        poly = Polygon(shape, facecolor='red', edgecolor='black', zorder=2)
        plt.gca().add_patch(poly)
    # Make Europe green
    elif info['CONTINENT'] == 'Europe':
        poly = Polygon(shape, facecolor='green', edgecolor='black', zorder=1)
        plt.gca().add_patch(poly)
    # Make Asia yellow
    elif info['CONTINENT'] == 'Asia':
        poly = Polygon(shape, facecolor='yellow', edgecolor='black', zorder=1)
        plt.gca().add_patch(poly)

# Show the plot
plt.savefig('custom_colored_map.png', dpi=300, bbox_inches='tight')
plt.show()
