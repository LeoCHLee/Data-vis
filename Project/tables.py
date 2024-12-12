import pandas as pd
import numpy
import matplotlib.pyplot as plt


price_data = pd.read_csv("Electricity prices.csv")

green_data = pd.read_csv("renewable electricity by country.csv", encoding='ISO-8859-1')

price_dict = dict(zip(price_data['Country'], price_data['household price']))

green_dict = dict(zip(green_data['country'], zip(green_data['all renewables'].str.strip('%').astype(float), green_data['continent'])))

for country in price_dict:
    if country in green_dict:
        price_dict[country] = (price_dict[country], *green_dict[country])  # Add percentage as a second value
    else:
        price_dict[country] = (price_dict[country], None, None)  # Default to None if no data is available

countries = list(price_dict.keys())
prices = [value[0] for value in price_dict.values()]
percentages = [value[1] for value in price_dict.values()]

continents = [value[2] for value in price_dict.values()]

continent_colors = {
    'Africa': 'green',
    'Asia': 'blue',
    'Europe': 'red',
    'N. America': 'purple',
    'Oceania': 'cyan',
    'S. America': 'orange'
}

# Create the scatter plot
colors = [continent_colors[cont] if cont in continent_colors else 'gray' for cont in continents]

# Create the scatter plot with color-coded continents
plt.figure(figsize=(10, 6))
plt.scatter(percentages, prices, c=colors, marker='o')

# Labels and title
plt.xlabel('Renewable Energy Percentage')
plt.ylabel('Electricity Price (cents/kWh)')
plt.title('Scatter Plot of Electricity Prices vs Renewable Energy Percentage')

# Add legend for continents
handles = [plt.Line2D([0], [0], marker='o', color='w', label=key, markerfacecolor=value, markersize=10) for key, value in continent_colors.items()]
plt.legend(handles=handles, title="Continents")

plt.grid(True)
plt.show()


# print(price_dict)

# green_dict = {}

#take in continent data - encode colours based on continents





