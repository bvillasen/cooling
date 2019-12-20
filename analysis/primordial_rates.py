import sys
import numpy as np
import matplotlib.pyplot as plt
import h5py as h5
import os.path
from mpl_toolkits.axes_grid1 import make_axes_locatable
from cooling_rates import *

cool_dir = os.path.dirname(os.getcwd()) + '/'
uvb_dir = cool_dir + 'uv_background/'
tools_dir = cool_dir + 'tools/'
sys.path.extend([ uvb_dir, tools_dir ] )
from tools import create_directory
from load_cloudy_output import *
from load_grackle_output import *
from load_cialoop_output import *

#Composition
n_H = 1
n_He = 0.1
#Temperature
# T = np.array([ 1e4, 1e5 ])
n_points = 1000
T = np.logspace( 3.8, 9, n_points )


#Get ionization fractions
ionization_frac = Get_Ionization_Fractions( n_H, n_He, T  ) 
n_HI = ionization_frac['HI']
n_HII = ionization_frac['HII']
n_HeI = ionization_frac['HeI']
n_HeII = ionization_frac['HeII']
n_HeIII = ionization_frac['HeIII']
mu = ( n_HI + n_HII + 4*(n_HeI + n_HeII + n_HeIII) ) / ( n_HI + 2*n_HII + n_HeI + 2*n_HeII + 3*n_HeIII)


#Get All cooling rates  
cooling_rates = Get_Cooling_Rates( n_H, n_He, T  )
Lambda_exitation_HI = cooling_rates['Excitation']['HI']
Lambda_exitation_HeII = cooling_rates['Excitation']['HeII']
Lambda_ionization_HI = cooling_rates['Ionization']['HI']
Lambda_ionization_HeI = cooling_rates['Ionization']['HeI']
Lambda_ionization_HeII = cooling_rates['Ionization']['HeII']
Lambda_recombination_HII = cooling_rates['Recombination']['HII']
Lambda_recombination_HeII = cooling_rates['Recombination']['HeII']
Lambda_recombination_HeIII = cooling_rates['Recombination']['HeIII']
Lambda_recombination_HeII_dielectronic = cooling_rates['Recombination']['HeII_dielectronic']
Lambda_bremst = cooling_rates['Bremsstrahlung']


Lambda_total = 0
for type in ['Excitation', 'Ionization', 'Recombination']:
  for key in cooling_rates[type].keys():
    Lambda_total +=  cooling_rates[type][key]
Lambda_total += cooling_rates['Bremsstrahlung']



#Load Grackle Cooling Rates
fileName = uvb_dir + 'data/CloudyData_noUVB.h5'
data_keys = [ 'cooling_rate', 'mean_molecular_weight']

data_grackle = {}
for key in data_keys:
  dens_vals,  temp_vals, table =  get_grackle_table_noUV( key, fileName, type='Primordial' )
  data_grackle['density'] = dens_vals
  data_grackle['temperature'] = temp_vals
  data_grackle[key] = table
temp_gk = data_grackle['temperature']
cool_gk = data_grackle['cooling_rate'][0]
mu_gk = data_grackle['mean_molecular_weight'][0]

#Load Cloudy Cooling Rates
cloudy_dir = '/home/bruno/Desktop/Dropbox/Developer/cloudy_cooling_tools/outputs/cooling_noUV_metals_off/'
name_base = 'cooling_run'
run_values = get_run_values_cialoop( cloudy_dir, name_base, z=False )
data_cloudy = {}
for key in data_keys:
  dens_vals,  temp_vals, table =  get_cialoop_table_noUV( run_values, key, name_base, cloudy_dir,  )
  data_cloudy['density'] = dens_vals
  data_cloudy['temperature'] = temp_vals
  data_cloudy[key] = table
temp_cl = data_cloudy['temperature']
cool_cl = data_cloudy['cooling_rate'][0]
mu_cl = data_cloudy['mean_molecular_weight'][0]


#Cloudy direct values
my_cloudy_file = '/home/bruno/Desktop/Dropbox/Developer/cooling_tools/cloudy_tools/data/primordial/temporal_c13/run_0/output.dat'
data_cloudy_1 = np.loadtxt( my_cloudy_file ).T
Temp = data_cloudy_1[0]
cooling_cloudy = data_cloudy_1[1]
mu_cloudy = data_cloudy_1[3]

#Plot Cooling rates comparison
n_rows = 1      
n_cols =  2
fig, ax_list = plt.subplots(nrows=n_rows, ncols=n_cols, figsize=(10*n_cols,9.2*n_rows))
plt.subplots_adjust(  wspace=0.3, hspace=0.3)

ax = ax_list[0]
ax.plot( temp_gk, cool_gk, linewidth=5,  label='Grackle' )
ax.plot( temp_cl, cool_cl,  linewidth=3, label='Cloudy v17' )
ax.plot( Temp, cooling_cloudy, '--', c='C9', linewidth=2, label='Cloudy v13' )
ax.plot( T, Lambda_total,'--', c='k', label='Katz+95' )
ax.legend()
fs = 15
ax.set_ylim(1e-24, 3e-22)
ax.set_xlim(3e3, 2e9)
ax.set_xscale('log')
ax.set_yscale('log')
ax.set_xlabel( 'Temperature [K]', fontsize=fs)
ax.set_ylabel( r' $\Lambda \, / \, \mathrm{n_H} ^ 2$ [erg s$^{-1}$ cm$^3$]', fontsize=fs)


ax = ax_list[1]
ax.plot( temp_gk, mu_gk, linewidth=4, label='Grackle' )
ax.plot( temp_cl, mu_cl,  label='Cloudy v17' )
ax.plot( Temp, mu_cloudy, c='C9', linewidth=2, label='Cloudy v13' )
ax.plot( T, mu,'--', c='k', label='Katz+95' )
ax.legend()
ax.set_xlim(3e3, 2e9)
ax.set_xscale('log')
ax.set_xlabel( 'Temperature [K]', fontsize=fs)
ax.set_ylabel( r' Mean Molecular Weight', fontsize=fs)


fig.savefig('primordial_cooling_comparison_cloudy13.png',  bbox_inches='tight', dpi=200 )


#Plot the cooling rates
n_rows = 1      
n_cols =  1
fig, ax_list = plt.subplots(nrows=n_rows, ncols=n_cols, figsize=(10*n_cols,9.2*n_rows))
plt.subplots_adjust(  wspace=0.3, hspace=0.3)

ax = ax_list
ax.plot( T, Lambda_exitation_HI, c='C0', linestyle='-', label='HI_excitation'  )
ax.plot( T, Lambda_exitation_HeII, c='C2', linestyle='-', label='HeII_excitation'  )
ax.plot( T, Lambda_ionization_HI, c='C0', linestyle='--', label='HI_ionization'  )
ax.plot( T, Lambda_ionization_HeI, c='C1', linestyle='--', label='HeI_ionization' )
ax.plot( T, Lambda_ionization_HeII, c='C2', linestyle='--', label='HeII_ionization' )
ax.plot( T, Lambda_recombination_HII, c='C3', linestyle='-.', label='HII_recombination' )
ax.plot( T, Lambda_recombination_HeII, c='C2', linestyle='-.', label='HeII_recombination' )
ax.plot( T, Lambda_recombination_HeIII,c='C4', linestyle='-.', label='HeIII_recombination' )
ax.plot( T, Lambda_recombination_HeII_dielectronic, c='C9', linestyle='--', label='HeII_recombination dielect' )
ax.plot( T, Lambda_bremst, c='C5', linestyle='-', label='Bremsstrahlung' )
ax.plot( T, Lambda_total, c='k', linewidth=2, label='Total' )
ax.legend()

fs = 15
ax.set_ylim(1e-25, 3e-22)
ax.set_xscale('log')
ax.set_yscale('log')
ax.set_xlabel( 'Temperature [K]', fontsize=fs)
ax.set_ylabel( r' $\Lambda \, / \, \mathrm{n_H} ^ 2$ [erg s$^{-1}$ cm$^3$]', fontsize=fs)
fig.savefig('primordial_cooling.png',  bbox_inches='tight', dpi=200 )





