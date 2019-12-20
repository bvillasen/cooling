import sys
import numpy as np
import matplotlib.pyplot as plt
import h5py as h5
import os.path
from mpl_toolkits.axes_grid1 import make_axes_locatable


root_dir = p = os.path.abspath('..')
tools_dir = root_dir + '/tools/'
cloudy_tools_dir = root_dir + '/cloudy_tools/'
figures_dir = root_dir + '/figures/'
sys.path.extend([ tools_dir, cloudy_tools_dir ] )
from tools import create_directory
from load_cloudy_output import *


inDir = '/home/bruno/Desktop/Dropbox/Developer/cloudy_cooling_tools/outputs/cooling_noUV_metals_off/'
inDir_metals = '/home/bruno/Desktop/Dropbox/Developer/cloudy_cooling_tools/outputs/cooling_uvHM_metals_on/'
outDir = figures_dir + 'noUV/'
name_base = 'cooling_run'
create_directory( outDir )

#Load the run density and redshift values
run_values = get_run_values( inDir, name_base, z=False )
# 
# 
type = 'Primordial'
# type = 'Metals'
# 
if type == 'Primordial': data_keys = [ 'cooling_rate', 'mean_molecular_weight']
if type == 'Metals': data_keys = [ 'cooling_rate'  ]
# 

data_cloudy = {}
for key in data_keys:
  dens_vals,  temp_vals, table =  get_cloudy_table_noUV( run_values, key, name_base, inDir,  )
  data_cloudy['density'] = dens_vals
  data_cloudy['temperature'] = temp_vals
  data_cloudy[key] = table
# 
# data_cloudy_metals = {}
# for key in data_keys:
#   dens_vals, redshift_vals, temp_vals, table =  get_cloudy_table( run_values, key, name_base, inDir_metals )
#   data_cloudy_metals['density'] = dens_vals
#   data_cloudy_metals['redshift'] = redshift_vals
#   data_cloudy_metals['temperature'] = temp_vals
#   data_cloudy_metals[key] = table


fileName = 'data/CloudyData_noUVB.h5'

data_grackle = {}
for key in data_keys:
  dens_vals,  temp_vals, table =  get_grackle_table_noUV( key, fileName, type=type )
  data_grackle['density'] = dens_vals
  data_grackle['temperature'] = temp_vals
  data_grackle[key] = table

# 
# data_cloudy = data_grackle
# indx_redshift = 0

# print indx_redshift

#Plot tables 
n_rows = 1      
n_cols =  2
fig, ax_list = plt.subplots(nrows=n_rows, ncols=n_cols, figsize=(10*n_cols,9.2*n_rows))
plt.subplots_adjust(  wspace=0.3, hspace=0.3)



dens_vals_cl = data_cloudy['density']
temp_vals_cl = data_cloudy['temperature']

dens_vals_gk = data_grackle['density'] 
temp_vals_gk = data_grackle['temperature']

cool_gk = data_grackle['cooling_rate'][0]
cool_cl = data_cloudy['cooling_rate'][0]



mmw_gk = data_grackle['mean_molecular_weight'][0]
mmw_cl = data_cloudy['mean_molecular_weight'][0]

indxs = np.where( cool_gk > 0 )[0]
indx_0 = indxs[0]
temp_0 = temp_vals[indx_0]
temp = temp_vals_gk[indxs]

fs = 15

ax = ax_list[0]
ax.plot( temp_vals_gk, cool_gk, linewidth=3, label='Grackle' )
ax.plot( temp_vals_cl, cool_cl, label='Cloudy' ) 
ax.set_xscale('log')
ax.set_xlabel( 'Temperature [K]', fontsize=fs)
ax.set_ylabel('Cooling Rate [ergs s$^{-1}$ cm$^{-3}$ ] ', fontsize=fs)
ax.legend( fontsize=15)

ax = ax_list[1]
ax.plot( temp_vals_gk, mmw_gk, linewidth=3, label='Grackle' )
ax.plot( temp_vals_cl, mmw_cl, label='Cloudy' ) 
ax.set_xscale('log')
ax.set_xlabel( 'Temperature [K]', fontsize=fs)
ax.set_ylabel('Mean Molecular Weight', fontsize=fs)
ax.legend( fontsize=15)







fig.savefig( outDir + 'tables_1D.png',  bbox_inches='tight', dpi=100 )

