import pandas as pd
import matplotlib.pyplot as plt

# Load the data
price_data = pd.read_csv("Electricity prices.csv")
green_data = pd.read_csv("renewable electricity by country.csv", encoding='ISO-8859-1')
plant_data = pd.read_csv("powerplants (global) - global_power_plants.csv", encoding='ISO-8859-1')

# Prepare price and green data
price_dict = dict(zip(price_data['Country'], price_data['household price']))
green_dict = dict(zip(green_data['country'], zip(green_data['all renewables'].str.strip('%').astype(float), green_data['continent'])))

# Merge data
for country in price_dict:
    if country in green_dict:
        price_dict[country] = (price_dict[country], *green_dict[country])
    else:
        price_dict[country] = (price_dict[country], None, None)

countries = list(price_dict.keys())
prices = [value[0] for value in price_dict.values()]
percentages = [value[1] for value in price_dict.values()]
continents = [value[2] for value in price_dict.values()]

# Define continent colors
continent_colors = {
    'Africa': 'green',
    'Asia': 'blue',
    'Europe': 'red',
    'N. America': 'purple',
    'Oceania': 'cyan',
    'S. America': 'orange'
}

# Create scatter plot with color-coded continents
colors = [continent_colors[cont] if cont in continent_colors else 'gray' for cont in continents]

plt.figure(figsize=(10, 6))
plt.scatter(percentages, prices, c=colors, marker='o')

# Labels and title
plt.xlabel('Renewable Energy Percentage')
plt.ylabel('Electricity Price (cents/kWh)')
plt.title('Scatter Plot of Electricity Prices vs Renewable Energy Percentage')

# Add legend for continents
handles = [plt.Line2D([0], [0], marker='o', color='w', label=key, markerfacecolor=value, markersize=10) for key, value in continent_colors.items()]
plt.legend(handles=handles, title="Continents")

# Add grid
plt.grid(True)

# Save the figure as an image file
output_image_path = "scatter_plot.png"
plt.savefig(output_image_path)

# Close the plot to free up memory
plt.close()
