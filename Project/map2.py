import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from matplotlib.patches import Polygon
import requests
from flask import Flask, render_template, request
import os

app = Flask(__name__)

# Create the figure and Basemap
plt.figure(figsize=(7.5, 5))
m = Basemap(projection='mill', llcrnrlat=-60, urcrnrlat=90, llcrnrlon=-180, urcrnrlon=180)

# Draw the map boundary and coastlines
m.drawmapboundary(fill_color='#add8e6')
m.fillcontinents(color='lightgrey', lake_color='#add8e6', zorder=0)
m.drawcoastlines(linewidth=0.5)

# Add country borders
m.drawcountries(linewidth=0.5, color='black')

# Show the plot
plt.savefig('custom_colored_map6.png', dpi=300, bbox_inches='tight')
plt.show()
