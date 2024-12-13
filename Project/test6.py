import dash
from dash import dcc, html
import plotly.graph_objects as go
import pandas as pd

# Sample data with latitude and longitude
plant_data = pd.read_csv("powerplants (global) - global_power_plants.csv", encoding='ISO-8859-1')

# Assign unique colors to each primary fuel type
color_mapping = {
    'Hydro': '#636EFA',          # Blue
    'Solar': '#EF553B',          # Red
    'Gas': '#00CC96',            # Green
    'Other': '#AB63FA',          # Purple
    'Oil': '#FFA15A',            # Orange
    'Wind': '#19D3F3',           # Cyan
    'Nuclear': '#FF6692',        # Pink
    'Coal': '#B6E880',           # Light Green
    'Waste': '#FF97FF',          # Magenta
    'Biomass': '#FECB52',        # Yellow
    'Wave and Tidal': '#1F77B4', # Dark Blue
    'Petcoke': '#E377C2',        # Light Pink
    'Geothermal': '#8C564B',     # Brown
    'Storage': '#7F7F7F',        # Gray
    'Cogeneration': '#BCBD22',   # Olive
}

# Map colors to the primary_fuel column
plant_data['color'] = plant_data['primary_fuel'].map(color_mapping)

# Create the Scattermapbox plot
fig = go.Figure()

fig.add_trace(go.Scattermapbox(
    lat=plant_data['latitude'],
    lon=plant_data['longitude'],
    mode='markers',
    marker=go.scattermapbox.Marker(
        size=5,
        color=plant_data['color'],  # Use the mapped colors
        opacity=0.7
    ),
    text=plant_data['primary_fuel'],  # Tooltip with primary fuel
    hoverinfo="text"
))

# Update layout for the map
fig.update_layout(
    mapbox=dict(
        style="carto-positron",
        zoom=6,  # Initial zoom level
        center={"lat": 20, "lon": 0}  # Initial center of the map
    ),
    title="Power Plants",
    margin={"r": 0, "t": 40, "l": 0, "b": 0},  # Remove excessive margins for better visibility
    dragmode="pan"  # Enable dragging/panning
)

# Create a Dash app
app = dash.Dash(__name__)

# Build a static legend
legend_items = [
    html.Div(
        children=[
            html.Div(style={"backgroundColor": color, "width": "20px", "height": "20px", "display": "inline-block", "marginRight": "10px"}),
            html.Span(fuel)
        ],
        style={"marginBottom": "5px"}
    )
    for fuel, color in color_mapping.items()
]

# Layout for the app
app.layout = html.Div([
    html.Div(
        children=[
            html.H4("Legend", style={"marginBottom": "10px"}),
            *legend_items
        ],
        style={
            "position": "absolute",
            "top": "40px",
            "left": "10px",
            "backgroundColor": "white",
            "padding": "10px",
            "border": "1px solid #ccc",
            "borderRadius": "5px",
            "zIndex": 1000
        }
    ),
    dcc.Graph(figure=fig, style={"height": "90vh"})
])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
