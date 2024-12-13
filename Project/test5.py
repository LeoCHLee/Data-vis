import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# Prepare data for the first map (Power Plants)
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
fig1 = go.Figure()

fig1.add_trace(go.Scattermapbox(
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
fig1.update_layout(
    mapbox=dict(
        style="carto-positron",
        zoom=6,  # Initial zoom level
        center={"lat": 20, "lon": 0}  # Initial center of the map
    ),
    title="Power Plants",
    margin={"r": 0, "t": 40, "l": 0, "b": 0},  # Remove excessive margins for better visibility
    dragmode="pan"  # Enable dragging/panning
)

# Prepare data for the second map (Renewable Energy)
data = pd.read_csv(r"C:\Users\leo22\OneDrive\Desktop\Trinity\Year 4\Data vis\Project\Data-vis\Project\renewable electricity by country.csv", encoding='ISO-8859-1')

# Clean data and create dictionary
energy_data_dict = {}
for index, row in data.iterrows():
    country = row['country']
    all_renewables = float(row['all renewables'].replace('%', ''))
    energy_data_dict[country] = all_renewables

energy_df = pd.DataFrame(list(energy_data_dict.items()), columns=["country", "all renewables"])

# Create the choropleth map
fig2 = px.choropleth(
    energy_df,
    locations="country",
    locationmode="country names",
    color="all renewables",
    hover_name="country",
    color_continuous_scale="RdYlGn",
    labels={"all renewables": "Renewable Energy (%)"},
    title="Global Renewable Energy by Country (Raw Values)"
)

fig2.update_layout(
    coloraxis_colorbar=dict(
        title="Renewable Energy (%)",
        tickvals=[0, 25, 50, 75, 100],
        ticktext=["0%", "25%", "50%", "75%", "100%"],
        ticks="inside"
    )
)

# Create the Dash app
app = dash.Dash(__name__)

# Build a static legend for the first map
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

# Layout for the app with tabs and static legend
app.layout = html.Div([
    # Tabs for switching between maps
    dcc.Tabs(id="tabs", value='tab-1', children=[
        dcc.Tab(label="Power Plants Map", value='tab-1', children=[
            html.Div(id="legend-container", children=[
                html.H4("Legend", style={"marginBottom": "10px"}),
                *legend_items
            ], style={
                "position": "absolute",
                "top": "40px",
                "left": "10px",
                "backgroundColor": "white",
                "padding": "10px",
                "border": "1px solid #ccc",
                "borderRadius": "5px",
                "zIndex": 1000
            }),
            dcc.Graph(figure=fig1, style={"height": "90vh"})
        ]),
        dcc.Tab(label="Renewable Energy Map", value='tab-2', children=[
            dcc.Graph(figure=fig2, style={"height": "90vh"})
        ])
    ])
])

# Callback to show or hide legend based on tab selection
@app.callback(
    Output('legend-container', 'style'),
    [Input('tabs', 'value')]
)
def toggle_legend(selected_tab):
    # If the 'Power Plants Map' tab is selected, show the legend
    if selected_tab == 'tab-1':
        return {
            "position": "absolute",
            "top": "250px",
            "left": "10px",
            "backgroundColor": "white",
            "padding": "10px",
            "border": "1px solid #ccc",
            "borderRadius": "5px",
            "zIndex": 1000
        }
    # If the 'Renewable Energy Map' tab is selected, hide the legend
    else:
        return {"display": "none"}

if __name__ == "__main__":
    app.run_server(debug=True)
