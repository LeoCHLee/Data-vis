# Adapted from fillstates.py from the basemap examples 

from __future__ import print_function
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap as Basemap
from matplotlib.colors import rgb2hex
from matplotlib.patches import Polygon
from matplotlib.colors import LinearSegmentedColormap
 
popdensity = {
    'New Jersey':  438.00,
    'Rhode Island':   387.35,
    'Massachusetts':   312.68,
    'Connecticut':	  271.40,
    'Maryland':   209.23,
    'New York':    155.18,
    'Delaware':    154.87,
    'Florida':     114.43,
    'Ohio':	 107.05,
    'Pennsylvania':	 105.80,
    'Illinois':    86.27,
    'California':  83.85,
    'Hawaii':  72.83,
    'Virginia':    69.03,
    'Michigan':    67.55,
    'Indiana':    65.46,
    'North Carolina':  63.80,
    'Georgia':     54.59,
    'Tennessee':   53.29,
    'New Hampshire':   53.20,
    'South Carolina':  51.45,
    'Louisiana':   39.61,
    'Kentucky':   39.28,
    'Wisconsin':  38.13,
    'Washington':  34.20,
    'Alabama':     33.84,
    'Missouri':    31.36,
    'Texas':   30.75,
    'West Virginia':   29.00,
    'Vermont':     25.41,
    'Minnesota':  23.86,
    'Mississippi':	 23.42,
    'Iowa':	 20.22,
    'Arkansas':    19.82,
    'Oklahoma':    19.40,
    'Arizona':     17.43,
    'Colorado':    16.01,
    'Maine':  15.95,
    'Oregon':  13.76,
    'Kansas':  12.69,
    'Utah':	 10.50,
    'Nebraska':    8.60,
    'Nevada':  7.03,
    'Idaho':   6.04,
    'New Mexico':  5.79,
    'South Dakota':	 3.84,
    'North Dakota':	 3.59,
    'Montana':     2.39,
    'Wyoming':      1.96,
    'Alaska':     0.42}

def make_map(state_data = popdensity, title='Population Density') :
    """ Take in state-wise data in dictionary format and plot on map 
        of U.S.
    """
    plt.figure(1,figsize=(9,5))
    # Lambert Conformal map of lower 48 states.
    m = Basemap(llcrnrlon=-119,llcrnrlat=19,urcrnrlon=-64,urcrnrlat=49,
                projection='lcc',lat_1=33,lat_2=45,lon_0=-95)
    # draw state boundaries.
    # data from U.S Census Bureau
    # http://www.census.gov/geo/www/cob/st2000.html
    shp_info = m.readshapefile('st99_d00','states',drawbounds=True)
    # population density by state from
    # hplttp://en.wikipedia.org/wiki/List_of_U.S._states_by_population_density
 
    # Segmented color scheme ranging from blue to red
    b2r = {'red':   ((0.0, 0.0, 0.0),
                     (1.0, 1.0, 1.0)),
           'green': ((0.0, 0.0, 0.0),
                     (1.0, 0.0, 0.0)),
           'blue':  ((0.0, 1.0, 1.0),
                     (1.0, 0.0, 0.0))
          }
    # modified version with slightly better purple emphasis
    bpr = {'red':   ((0.0, 0.0, 0.0),
                     (0.25, 0.5, 0.5),
                     (1.0, 1.0, 1.0)),
           'green': ((0.0, 0.0, 0.0),
                     (1.0, 0.0, 0.0)),
            'blue': ((0.0, 1.0, 1.0),
                     (0.75, 0.5, 0.5),
                     (1.0, 0.0, 0.0))
          }         
    cmap = LinearSegmentedColormap('BlueRed1', bpr)
  
    # choose a color for each state based on state-wise data.
    colors={}
    statenames=[]
    vmin = min(state_data.values()) 
    vmax = max(state_data.values())
    for shapedict in m.states_info:
        statename = shapedict['NAME']
        # skip DC and Puerto Rico.
        if statename not in ['District of Columbia','Puerto Rico']:           
            pop = popdensity[statename]
            # calling colormap with value between 0 and 1 returns rgba value.  
            colors[statename] = cmap(((pop-vmin)/(vmax-vmin)))[:3]
        statenames.append(statename)
    # cycle through state names, color each one.
    ax = plt.gca() # get current axes instance
    for nshape,seg in enumerate(m.states):
        # skip DC and Puerto Rico.
        if statenames[nshape] not in ['District of Columbia','Puerto Rico']:
            # To plot Alaska and Hawaii, I've modified the approach of 
            # MomoPP:
            # http://stackoverflow.com/questions/39742305/how-to-use-basemap-python-to-plot-us-with-50-states
            if statenames[nshape] == 'Alaska':
            # Alaska is too big. Scale it down to 35% first, then transate it. 
                seg = list(map(lambda (x,y): (0.35*x + 1000000, 0.35*y-1300000), seg))
            if statenames[nshape] == 'Hawaii':
                seg = list(map(lambda (x,y): (x + 5100000, y-1500000), seg))
            # TODO: Hawaii has small small tails that appear to cover the
            # the western U.S.  Never knew!
            color = rgb2hex(colors[statenames[nshape]]) 
            poly = Polygon(seg,facecolor=color,edgecolor='black')
            ax.add_patch(poly)
    plt.title(title)
    # Hackish way to define color map
    tmp=np.linspace(vmin, vmax,100)
    im = plt.imshow(np.array([tmp, tmp]), cmap=cmap)
    plt.colorbar(im, fraction=0.046, pad=0.04)
    plt.savefig(title + '.png')
    plt.savefig(title + '.pdf')
    #plt.axis([])
    plt.show()

if __name__ == '__main__' :
    make_map(state_data = popdensity, title='Population Density')