import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

# Sample data with latitude and longitude
plant_data = pd.read_csv("powerplants (global) - global_power_plants.csv", encoding='ISO-8859-1')

plant_dict= dict(zip(plant_data['country_long'], zip(plant_data['primary_fuel'], zip(plant_data['latitude'], plant_data['longitude']))))


# print(plant_dict)

# # Create a scatter_geo plot
# fig = px.scatter_geo(
#     plant_data,
#     lat="latitude",  # Column for latitude
#     lon="longitude",  # Column for longitude
#     #text="primary_fuel",  # Labels for points
#     #size="population",  # Bubble size based on population
#     title="Cities by Population",
#     projection="natural earth"  # Map projection style
# )





# Create a scatter_geo plot with colors based on primary_fuel
fig = px.scatter_geo(
    plant_data,
    lat="latitude",  # Column for latitude
    lon="longitude",  # Column for longitude
    color="primary_fuel",  # Colors based on primary fuel
    title="Power Plants by Primary Fuel",
    projection="natural earth"  # Map projection style
)


#--------------------------------------------------------------------------------------------------
# fig = go.Figure()

# fig.add_trace(go.Scattermapbox(
#     lat=plant_data['latitude'],
#     lon=plant_data['longitude'],
#     mode='markers',
#     marker=go.scattermapbox.Marker(size=5, color=plant_data['primary_fuel']),
#     text=plant_data['primary_fuel']
# ))

# fig.update_layout(
#     mapbox_style="carto-positron",
#     mapbox_zoom=2,
#     mapbox_center={"lat": 20, "lon": 0},
#     title="Power Plants (WebGL Optimized)"
# )

#---------------------------------------------------------------------------------------------------


fig.show()



