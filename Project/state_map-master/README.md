# state_map
Plot state map given state-wise data. 

Included:
  fillstates.py -- a slight modification of the same file from basemap examples
  st99_d00.dbf  -- attribute file
  st99_d00.shp  -- shape file (i.e., the geometry)
  st99_d00.shx  -- shape index

Note, the latter st99 files come with the basemap examples but are themselves
available from the USDA: 

https://infosys.ars.usda.gov/svn/code/weps1/trunk/weps.install/db/gis/st99_d00/

To get Alaska and Hawaii on the same map, I adapted the approach of MomoPP:

http://stackoverflow.com/questions/39742305/how-to-use-basemap-python-to-plot-us-with-50-states

To run, you'll need to install basemap (which, if you use conda, is as 
easy as conda install basemap).

Mods by Jeremy Roberts (2017).  jaroberts@ksu.edu.

