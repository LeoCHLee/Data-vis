import pandas as pd
import plotly.express as px
from plotly.data import gapminder
from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objects as go


# Initialize an empty dictionary
energy_data_dict = {}

# Read the CSV file with the correct encoding
data = pd.read_csv(r"C:\Users\leo22\OneDrive\Desktop\Trinity\Year 4\Data vis\Project\Data-vis\Project\renewable electricity by country.csv", encoding='ISO-8859-1')

# Loop through the rows of the DataFrame and fill the dictionary
for index, row in data.iterrows():
    country = row['country']          # Assuming 'country' is the column name for countries
    all_renewables = row['all renewables']  # Using the raw 'all renewables' value

   
    all_renewables = float(all_renewables.replace('%', '')) 
    
    # Add the country and its renewable energy value to the dictionary
    energy_data_dict[country] = all_renewables

energy_df = pd.DataFrame(list(energy_data_dict.items()), columns=["country", "all renewables"])


# Now create the choropleth map using raw values (no normalization)
fig = px.choropleth(energy_df,
                    locations="country",  # Column with country names
                    locationmode="country names",  # This specifies the country names mode
                    color="all renewables",  # Use the raw 'all renewables' values directly
                    hover_name="country",  # Column to show on hover
                    color_continuous_scale="RdYlGn",  # You can choose any color scale
                    labels={"all renewables": "Renewable Energy (%)"},  # Label for the legend
                    title="Global Renewable Energy by Country (Raw Values)")

# Update the color bar to make it continuous
fig.update_layout(
    coloraxis_colorbar=dict(
        title="Renewable Energy (%)",  # Title of the color bar
        tickvals=[0, 25, 50, 75, 100],  # Add tick values if needed
        ticktext=["0%", "25%", "50%", "75%", "100%"],  # Custom tick labels
        ticks="inside"  # Ensures ticks are inside the color bar
    )
)

print(data['all renewables'].dtypes)

# Show the map
fig.show()
