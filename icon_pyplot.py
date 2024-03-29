import numpy as np
from netCDF4 import Dataset
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import matplotlib.tri as tri

# some pdf viewers have problems with matplotlib plot. If so, use the commented lines below
# from matplotlib import rc
# rc('text', usetex=True)
# rc('font', size=40)
# rc('legend', fontsize=9)
# rc('text.latex', preamble=r'\usepackage{cmbright}')

ipath = 'data/'
ifile_var = 'test_var.nc'
ifile_grid = 'test_grid_DOM01.nc'

# read in data
var_string = 't_2m'
f_var = Dataset(ipath+ifile_var, 'r')
var = np.squeeze(f_var.variables[var_string][:])
#print(type(var))
level = np.linspace(265, 285, 50)
labels= np.arange(265, 286, 1)


# create basic map
fig = plt.figure(figsize=(12, 13))
m = Basemap(projection='cyl', llcrnrlon=5.5, llcrnrlat=47.2, urcrnrlon=15.3, urcrnrlat=55, resolution='i')
m.drawcoastlines(linewidth=1.7)
m.drawcountries(linewidth=1.7)


# use this for contour plot with filled triangles. You need the grid file for that
def create_triagulation_triangles(ifile_grid_in):

    f_grid = Dataset(ifile_grid_in, 'r')
    triangles = np.swapaxes(f_grid.variables['vertex_of_cell'][:]-1, 0, 1)
    vlon, vlat = np.degrees(f_grid.variables['vlon'][:]), np.degrees(f_grid.variables['vlat'][:])
    triang_out = tri.Triangulation(vlon, vlat, triangles)
    return triang_out

triang = create_triagulation_triangles(ipath+ifile_grid)
plt.tripcolor(triang, facecolors=var, vmin=265, vmax=285, edgecolors='k')
cbar = plt.colorbar(ticks=labels, fraction=0.036)
cbar.ax.tick_params(labelsize=10)
cbar.set_label(label='Temperature in K', rotation=90)
plt.show()
#plt.savefig('Plot_unstructured_triangles.png')

##################################################################################

# use this for a smoothed contour plot
fig = plt.figure(figsize=(12, 13))
m = Basemap(projection='cyl', llcrnrlon=5.5, llcrnrlat=47.2, urcrnrlon=15.3, urcrnrlat=55, resolution='i')
m.drawcoastlines(linewidth=1.7)
m.drawcountries(linewidth=1.7)


def create_triagulation_smooth(ifile_grid_in):

    f_grid = Dataset(ipath+ifile_grid, 'r')
    clon, clat = np.degrees(f_grid.variables['clon'][:]), np.degrees(f_grid.variables['clat'][:])
    triang_out = tri.Triangulation(clon, clat)
    return triang_out

triang = create_triagulation_smooth(ipath+ifile_grid)

# convert to numpy array or just take the data (maskarrays cannot be plotted by tricontourf)
# plt.tricontourf(triang, np.array(var), levels=level)
plt.tricontourf(triang, var.data, levels=level)
cbar = plt.colorbar(ticks=labels, fraction=0.036)
cbar.ax.tick_params(labelsize=10)
cbar.set_label(label='Temperature in K', rotation=90)
plt.show()
#plt.savefig('Plot_unstructured.png')
