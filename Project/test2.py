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

# Map fuel to color
plant_data['color'] = plant_data['primary_fuel'].map(color_mapping)

# Create the Scattermapbox plot
fig1 = go.Figure()


#add plots
fig1.add_trace(go.Scattermapbox(
    lat = plant_data['latitude'],
    lon = plant_data['longitude'],
    mode = 'markers',
    marker = go.scattermapbox.Marker(
        size = 5,
        color = plant_data['color'],  # Use the mapped colors
        opacity = 0.7
    ),
    text=plant_data['primary_fuel'],  # Tooltip with primary fuel
    hoverinfo = "text"
))


#change layout
fig1.update_layout(
    mapbox=dict(
        style = "carto-positron",
        zoom = 6,  # Initial zoom level
        center = {"lat": 20, "lon": 0}  # Initial center of the map
    ),
    title = "Power Plants",
    margin = {"r": 0, "t": 40, "l": 0, "b": 0},  # Remove excessive margins for better visibility
    dragmode="pan"  # Enable dragging/panning
)

#panda datgram
data = pd.read_csv(r"C:\Users\leo22\OneDrive\Desktop\Trinity\Year 4\Data vis\Project\Data-vis\Project\renewable electricity by country.csv", encoding='ISO-8859-1')


energy_data_dict = {}


#dict country: percentage
for index, row in data.iterrows():
    country = row['country']
    all_renewables = float(row['all renewables'].replace('%', ''))
    energy_data_dict[country] = all_renewables

energy_df = pd.DataFrame(list(energy_data_dict.items()), columns=["country", "all renewables"])

#color map
fig2 = px.choropleth(
    energy_df,
    locations = "country",
    locationmode = "country names",
    color="all renewables",
    hover_name = "country",
    color_continuous_scale="RdYlGn",
    labels = {"all renewables": "Renewable Energy (%)"},
    title = "Global Renewable Energy by Country"
)

fig2.update_layout(
    coloraxis_colorbar = dict(
        title = "Renewable Energy (%)",
        tickvals = [0, 25, 50, 75, 100],
        ticktext = ["0%", "25%", "50%", "75%", "100%"],
        ticks="inside"
    )
)


plant_data['primary_fuel'] = plant_data['primary_fuel'].str.strip().str.title()
countries = sorted(plant_data['country_long'].dropna().unique())

# dash similar to flask for ui
app = dash.Dash(__name__)

# tabs n shit
app.layout = html.Div([
    html.H1("Global Energy Stats", style={'textAlign': 'center'}),

    dcc.Tabs(id = "tabs", value='tab-1', children=[
        # First Tab: Power Plants Map
        dcc.Tab(label = "Power Plants Map", value='tab-1', children=[
            html.Div(id = "legend-container", children=[
                html.H4("Legend", style={"marginBottom": "10px"}),
                *(  #I don't know what this does
                    html.Div([
                        html.Div(style = {"backgroundColor": color, "width": "20px", "height": "20px", "display": "inline-block", "marginRight": "10px"}),
                        html.Span(fuel)
                    ], style={"marginBottom": "5px"}) for fuel, color in color_mapping.items()
                )
            ], style={
                "position": "absolute",
                "top": "200px",
                "left": "10px",
                "backgroundColor": "white",
                "padding": "10px",
                "border": "1px solid #ccc",
                "borderRadius": "5px",
                "zIndex": 1000
            }),
            dcc.Graph(figure=fig1, style={"height": "90vh"})
        ]),

        # tab 2
        dcc.Tab(label="Renewable Energy Map", value='tab-2', children=[
            dcc.Graph(figure=fig2, style={"height": "90vh"})
        ]),

        # Tab 3
        dcc.Tab(label="Graphs", value='tab-3', children=[
            html.Div([
                # pie chart
                html.Div([
                    html.Label("Select a Country:", style={'fontSize': '18px'}),
                    dcc.Dropdown(
                        id = 'country-dropdown',
                        options = [{'label': country, 'value': country} for country in countries],
                        value = countries[0],#default to first 
                        placeholder = "Select a country",
                        style = {'width': '80%', 'marginTop': '10px'}
                    ),
                    dcc.Graph(id = 'pie-chart', style = {'width': '90%', 'height': '400px', 'marginTop': '0px', 'marginLeft': 'auto', 'marginRight': 'auto'}),
                    ], style={'display': 'inline-block', 'padding': '10px', 'width': '48%'}),  
                
                # graph
                 html.Div([
                 html.Label("", style={'fontSize': '18px', 'textAlign': 'center'}),
                 html.Img(src = "/static/scatter_plot.png", style = {'width': '80%', 'marginTop': '20px', 'height': '400px'}),  # loading pre created graph
          
                ], style={'display': 'inline-block', 'padding': '10px', 'width': '48%', 'float': 'right'})  
            ])
        ])
    ])
])

# callback for the pie chart country selection
@app.callback(
    Output('pie-chart', 'figure'),
    Input('country-dropdown', 'value')
)
def update_pie_chart(selected_country):
    # Filter data for the selected country
    country_data = plant_data[plant_data['country_long'] == selected_country]
    fuel_counts = country_data['primary_fuel'].value_counts().reset_index()
    #name columns for easy usage
    fuel_counts.columns = ['Fuel Type', 'Count']


    # Map custom colors based on fuel type
    fuel_counts['Color'] = fuel_counts['Fuel Type'].map(color_mapping)

    # pie chart mapped to color map
    fig = px.pie(
        fuel_counts,
        values = 'Count',
        names = 'Fuel Type',
        title = f"Power Plant Types in {selected_country}",
        color_discrete_map = color_mapping  
    )
    fig.update_traces(hovertemplate='<b>%{label}</b><br>Count: %{value}<extra></extra>')
    return fig

if __name__ == "__main__":
    app.run_server(debug=True)
