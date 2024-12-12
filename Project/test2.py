import plotly.express as px
import pandas as pd

# Sample data with latitude and longitude
data = pd.DataFrame({
    "city": ["New York", "London", "Tokyo", "Sydney"],
    "latitude": [40.7128, 51.5074, 35.6895, -33.8688],
    "longitude": [-74.0060, -0.1278, 139.6917, 151.2093],
    "population": [8419000, 8982000, 13929000, 5312000]
})

# Create a scatter_geo plot
fig = px.scatter_geo(
    data,
    lat="latitude",  # Column for latitude
    lon="longitude",  # Column for longitude
    text="city",  # Labels for points
    size="population",  # Bubble size based on population
    title="Cities by Population",
    projection="natural earth"  # Map projection style
)

# Show the map
fig.show()
