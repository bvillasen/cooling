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
from load_grackle_output import *
from load_hm12_data import *


# type = 'Primordial'
type = 'Metals'

uvb = 'Puchwein18'
# uvb = 'HM12'

outDir = figures_dir + 'grackle_files/uv_{0}_{1}_cloudy_lux/'.format(uvb, type)
create_directory( outDir )

if type == 'Primordial': data_keys = [ 'cooling_rate', 'heating_rate', 'mean_molecular_weight']
if type == 'Metals': data_keys = [ 'cooling_rate', 'heating_rate', ]

keys_grackle = {'cooling_rate': 'Cooling', 'heating_rate': 'Heating', 'mean_molecular_weight': 'MMW'}


#Load Gracke Data
file_name = 'data/CloudyData_UVB=HM2012.h5'
data_grackle = load_grackle_dataset( file_name )

#Load Cloudy Data
file_name = 'data/my_grackle_files/CloudyData_UVB=Puchwein2018_cloudy.h5'
data_cloudy = load_grackle_dataset( file_name )

uvb_rates_gk = data_grackle['UVBRates']
z_gk = uvb_rates_gk['z']
heating_HI_gk = uvb_rates_gk['Photoheating']['piHI']
heating_HeI_gk = uvb_rates_gk['Photoheating']['piHeI']
heating_HeII_gk = uvb_rates_gk['Photoheating']['piHeII']

ionization_HI_gk = uvb_rates_gk['Chemistry']['k24']
ionization_HeI_gk = uvb_rates_gk['Chemistry']['k26']
ionization_HeII_gk = uvb_rates_gk['Chemistry']['k25']

uvb_rates_cl = data_cloudy['UVBRates']
z_cl = uvb_rates_cl['z']
heating_HI_cl = uvb_rates_cl['Photoheating']['piHI']
heating_HeI_cl = uvb_rates_cl['Photoheating']['piHeI']
heating_HeII_cl = uvb_rates_cl['Photoheating']['piHeII']

ionization_HI_cl = uvb_rates_cl['Chemistry']['k24']
ionization_HeI_cl = uvb_rates_cl['Chemistry']['k26']
ionization_HeII_cl = uvb_rates_cl['Chemistry']['k25']

#Plot Heating and Ionizatiosnates
nrows=1
ncols = 2
fig, (ax1,ax2) = plt.subplots(nrows=nrows, ncols=ncols, figsize=(10*ncols,8*nrows))

fs = 17
lw = 3

alpha = 0.5
ax1.plot( z_cl, heating_HI_cl,  c='C1', linewidth=lw, alpha=alpha, label="HI" )
ax1.plot( z_cl, heating_HeI_cl,  c='C2', linewidth=lw, alpha=alpha, label="HeI" )
ax1.plot( z_cl, heating_HeII_cl,  c='C3',linewidth=lw, alpha=alpha, label="HeII" )

ax1.plot( z_gk, heating_HI_gk, '--', c='C1', linewidth=lw,  )
ax1.plot( z_gk, heating_HeI_gk, '--', c='C2', linewidth=lw,  )
ax1.plot( z_gk, heating_HeII_gk, '--', c='C3',linewidth=lw,  )

ax1.set_yscale('log')
ax1.legend( fontsize = fs)
# ax.set_title('UVB Rates H&M 2012')
ax1.set_xlabel('Redshift', fontsize=fs)
ax1.set_ylabel(r'Photoheating Rate   [eV s$^{-1}$]', fontsize=fs)

ax2.plot( z_cl, ionization_HI_cl,  c='C1', linewidth=lw,  label="HI", alpha=alpha  )
ax2.plot( z_cl, ionization_HeI_cl,  c='C2', linewidth=lw,  label="HeI", alpha=alpha )
ax2.plot( z_cl, ionization_HeII_cl,  c='C3',linewidth=lw, label="HeII", alpha=alpha  )

ax2.plot( z_gk, ionization_HI_gk, '--', c='C1', linewidth=lw,  )
ax2.plot( z_gk, ionization_HeI_gk, '--', c='C2', linewidth=lw,  )
ax2.plot( z_gk, ionization_HeII_gk, '--', c='C3',linewidth=lw,  )

ax2.set_yscale('log')
ax2.legend( fontsize = fs)
# ax.set_title('UVB Rates H&M 2012')
ax2.set_xlabel('Redshift', fontsize=fs)
ax2.set_ylabel(r'Photoionization Rate   [s$^{-1}$]', fontsize=fs)


fig.savefig( figures_dir + 'grackle_files/heating_ionization_rates_{0}.png'.format(uvb, type),  bbox_inches='tight', dpi=100)


# indx_redshift = 0
n_redshift = 26
for indx_redshift in range(n_redshift):
# for indx_redshift in [25]:
  # print indx_redshift

  #Plot tables 
  n_rows = len(data_keys)      
  n_cols =  3
  fig, ax_list = plt.subplots(nrows=n_rows, ncols=n_cols, figsize=(10*n_cols,9.2*n_rows))
  plt.subplots_adjust(  wspace=0.3, hspace=0.3)



  for i,key in enumerate(data_keys):
    key_grackle = keys_grackle[key]
    dens_vals_cl = data_cloudy['CoolingRates'][type][key_grackle]['Parameter1']
    redshift_vals_cl = data_cloudy['CoolingRates'][type][key_grackle]['Parameter2']
    temp_vals_cl = data_cloudy['CoolingRates'][type][key_grackle]['Temperature']

    dens_vals_gk = data_grackle['CoolingRates'][type][key_grackle]['Parameter1']
    redshift_vals_gk = data_grackle['CoolingRates'][type][key_grackle]['Parameter2']
    temp_vals_gk = data_grackle['CoolingRates'][type][key_grackle]['Temperature']

    if ( np.abs( dens_vals_gk - dens_vals_cl ) > 1e-3 ).any(): print 'Error: density mismatch new'
    if ( np.abs( temp_vals_gk - temp_vals_cl ) / temp_vals_gk > 1e-6 ).any(): print 'Error: temperature mismatch'

    temp_log = np.log10( temp_vals_cl )

    z_cl = redshift_vals_cl[indx_redshift]
    z_gk = redshift_vals_gk[indx_redshift]
    if ( np.abs( z_gk - z_cl ) > 1e-6 ).any(): print 'Error: redshift mismatch new'
    if i==0: print "\nIndex: {1}  z = {0:.2f}".format(z_cl, indx_redshift)
# 

    data_gk = data_grackle['CoolingRates'][type][key_grackle]['data'][::-1, indx_redshift, :]
    data_cl = data_cloudy['CoolingRates'][type][key_grackle]['data'][::-1, indx_redshift, :]

    # print data_gk.min(), data_gk.max()
    data_gk[data_gk < 1e-40] = 1e-40
    data_cl[data_cl < 1e-40] = 1e-40

    diff = ( data_cl - data_gk ) / data_gk
# 
    if ( key == 'cooling_rate' or key == 'heating_rate' ):
      data_cl = np.log10( data_cl )
      data_gk = np.log10( data_gk )

    data_min = min( data_cl.min(), data_gk.min() )
    data_max = max( data_cl.max(), data_gk.max() )  
    # print data_min, data_max

    if key == 'mean_molecular_weight':
      print "MMW: "
      print " Grackle:  {0:.3f}  {1:.3f}  ".format( data_gk.min(), data_gk.max() )
      print " Cloudy:   {0:.3f}  {1:.3f}  ".format( data_cl.min(), data_cl.max() )

    ax_row = ax_list[i]


    color_0 = 'jet'
    fs = 17
    fs_1 = 25

    ax = ax_row[0]
    im = ax.imshow( data_gk, extent=( temp_log[0], temp_log[-1], dens_vals_cl[0], dens_vals_cl[-1]), aspect='auto', vmin=data_min, vmax=data_max, cmap=color_0)
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.1)
    cb = fig.colorbar( im, cax=cax )
    cb.ax.tick_params(labelsize=17) 
    ax.set_xlabel( 'log Temperature [K]', fontsize=fs)
    ax.set_ylabel( r'log Density [cm$^{-3}$]', fontsize=fs)
    if i==0: ax.set_title( 'Grackle Table', fontsize=fs_1)
    ax.tick_params(axis='both', which='major', labelsize=15)
    ax.tick_params(axis='both', which='minor', labelsize=8)


    ax = ax_row[1]
    im = ax.imshow( data_cl, extent=( temp_log[0], temp_log[-1], dens_vals_cl[0], dens_vals_cl[-1]), aspect='auto', vmin=data_min, vmax=data_max, cmap=color_0)
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.1)
    cb = fig.colorbar( im, cax=cax )
    cb.ax.tick_params(labelsize=17) 
    ax.set_xlabel( 'log Temperature [K]', fontsize=fs)
    ax.set_ylabel( r'log Density [cm$^{-3}$]', fontsize=fs)
    if i==0: ax.set_title( 'Cloudy Result', fontsize=fs_1)
    ax.tick_params(axis='both', which='major', labelsize=15)
    ax.tick_params(axis='both', which='minor', labelsize=8)


    ax = ax_row[2]
    im = ax.imshow( diff, extent=( temp_log[0], temp_log[-1], dens_vals_cl[0], dens_vals_cl[-1]), aspect='auto', cmap=color_0)
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.1)
    cb = fig.colorbar( im, cax=cax )
    cb.ax.tick_params(labelsize=17) 
    ax.set_xlabel( 'log Temperature [K]', fontsize=fs)
    ax.set_ylabel( r'log Density [cm$^{-3}$]', fontsize=fs)
    if i==0: ax.set_title( 'Fractional Difference', fontsize=fs_1)
    ax.tick_params(axis='both', which='major', labelsize=15)
    ax.tick_params(axis='both', which='minor', labelsize=8)

    fig.suptitle( 'Z = {0:.2f}'.format(z_cl), fontsize= 25, y=0.92)


  if type == 'Primordial':
    ax.annotate(r'log Cooling Rate [ergs s$^{-1}$ cm$^{-3}$ ] ', xy=(.04, .915), xycoords='figure fraction', fontsize=25, rotation=90)
    ax.annotate(r'log Heating Rate [ergs s$^{-1}$ cm$^{-3}$ ] ', xy=(.04, .59), xycoords='figure fraction', fontsize=25, rotation=90)
    ax.annotate('Mean Molecular Weight', xy=(.04, .24), xycoords='figure fraction', fontsize=25, rotation=90)

  if type == 'Metals':
    ax.annotate(r'log Cooling Rate [ergs s$^{-1}$ cm$^{-3}$ ] ', xy=(.04, .91), xycoords='figure fraction', fontsize=25, rotation=90)
    ax.annotate(r'log Heating Rate [ergs s$^{-1}$ cm$^{-3}$ ] ', xy=(.04, .41), xycoords='figure fraction', fontsize=25, rotation=90)

  fig.savefig( outDir + 'tables_{0}.png'.format(n_redshift-indx_redshift -1),  bbox_inches='tight', dpi=100 )
