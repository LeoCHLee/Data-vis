import matplotlib.pyplot as plt
# from mpl_toolkits.basemap import Basemap
from matplotlib.patches import Polygon
import requests
from flask import Flask, render_template, request
import plotly.express as px
import pandas as pd




app = Flask(__name__)

@app.route('/')
def home():
   return render_template('home.html')


if __name__ == '__main__':  
   app.run(debug=True)

