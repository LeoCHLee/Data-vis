import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Load and preprocess data
plant_data = pd.read_csv("powerplants (global) - global_power_plants.csv", encoding='ISO-8859-1')

# Clean and standardize 'primary_fuel' column
plant_data['primary_fuel'] = plant_data['primary_fuel'].str.strip().str.title()

# Get unique countries for dropdown menu
countries = plant_data['country_long'].unique()
#dropna
countries = sorted(countries)  # Sort countries alphabetically

# Create the Dash app
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Graphs", style={'textAlign': 'center'}),
    
    # Main container for the two sections
    html.Div([
        # Left section
        html.Div([
            html.Label("Select a Country:", style={'fontSize': '18px'}),
            dcc.Dropdown(
                id='country-dropdown',
                options=[{'label': country, 'value': country} for country in countries],
                value=countries[0],  # Default value
                placeholder="Select a country",
                style={'width': '90%', 'marginBottom': '10px'}
            ),
            dcc.Graph(id='pie-chart', style={'height': '400px', 'marginTop': '20px'}),
        ], style={'width': '45%', 'float': 'left', 'padding': '10px'}),
        
        # Divider
        html.Div(
            style={
                'width': '2px',
                'backgroundColor': ' #000000',
                'height': 'auto',
                'margin': '0 10px'
            }
        ),
        
        # Right section
        html.Div([
            html.Label("Unrelated Graph (Placeholder)", style={'fontSize': '18px', 'textAlign': 'center'}),
            dcc.Graph(id='another-graph', style={'height': '500px'}),
        ], style={'width': '45%', 'float': 'left', 'padding': '10px'}),
    ], style={'display': 'flex', 'flexDirection': 'row', 'justifyContent': 'space-between'})
])

# Define callback to update pie chart based on selected country
@app.callback(
    Output('pie-chart', 'figure'),
    Input('country-dropdown', 'value')
)
def update_pie_chart(selected_country):
    # Filter data for the selected country
    country_data = plant_data[plant_data['country_long'] == selected_country]
    
    # Aggregate data by primary fuel type
    fuel_counts = country_data['primary_fuel'].value_counts().reset_index()
    fuel_counts.columns = ['Fuel Type', 'Count']
    
    # Create pie chart with annotations for the number of power plants
    fig = px.pie(
        fuel_counts,
        values='Count',
        names='Fuel Type',
        title=f"Power Plant Types in {selected_country}",
        color_discrete_sequence=px.colors.qualitative.Plotly
    )
    
    # Add custom hover text to display the count of each type
    fig.update_traces(
        hovertemplate='<b>%{label}</b><br>Count: %{value}<extra></extra>'
    )
    
    return fig

# Define placeholder callback for another graph
@app.callback(
    Output('another-graph', 'figure'),
    Input('country-dropdown', 'value')
)
def update_another_graph(selected_country):
    # Placeholder graph: Replace this logic with your desired visualization
    fig = px.bar(
        x=['X1', 'X2', 'X3'], y=[10, 15, 7],
        labels={'x': 'Placeholder X', 'y': 'Placeholder Y'},
        title=f"Unrelated Graph for {selected_country}"
    )
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
