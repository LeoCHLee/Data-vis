from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd

# Sample DataFrame
energy_df = pd.DataFrame({
    "country": ["United States", "Canada", "Germany", "France"],
    "all renewables": [45.0, 60.0, 80.0, 50.0]
})

# Create the app
app = Dash(__name__)

# Create the figure
fig = px.choropleth(
    energy_df,
    locations="country",
    locationmode="country names",
    color="all renewables",
    hover_name="country",
    hover_data={"all renewables": True},
    color_continuous_scale="Viridis",
    labels={"all renewables": "Renewable Energy (%)"},
    title="Global Renewable Energy by Country (Raw Values)"
)

# Layout
app.layout = html.Div([
    dcc.Graph(
        id="choropleth-map",
        figure=fig
    ),
    html.Div(id="popup-content", style={"margin-top": "20px", "font-size": "18px", "font-weight": "bold"})
])

# Callback to handle clicks
@app.callback(
    Output("popup-content", "children"),
    Input("choropleth-map", "clickData")
)
def display_popup(clickData):
    if clickData is None:
        return "Click on a country to see more details."
    country = clickData["points"][0]["location"]  # Extract clicked country
    renewable = clickData["points"][0]["z"]       # Extract renewable value
    return f"You clicked on {country}. Renewable Energy: {renewable}%"

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
