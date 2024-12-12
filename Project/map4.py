import plotly.express as px
import pandas as pd

# Sample data with latitude and longitude
plant_data = pd.read_csv("powerplants (global) - global_power_plants.csv", encoding='ISO-8859-1')

plant_data = dict()

# Create a scatter_geo plot
fig = px.scatter_geo(
    plant_data,
    lat="latitude",  # Column for latitude
    lon="longitude",  # Column for longitude
    text="city",  # Labels for points
    size="population",  # Bubble size based on population
    title="Cities by Population",
    projection="natural earth"  # Map projection style
)

# Show the map
fig.show()
