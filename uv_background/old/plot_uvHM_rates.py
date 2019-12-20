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


inDir = '/home/bruno/Desktop/Dropbox/Developer/cloudy_cooling_tools/outputs/cooling_uvHM_metals_off_test/'
inDir_metals = '/home/bruno/Desktop/Dropbox/Developer/cloudy_cooling_tools/outputs/cooling_uvHM_metals_on/'
outDir = figures_dir + 'uvHM_metals_off_test/'
name_base = 'cooling_run'
create_directory( outDir )

#Load the run density and redshift values
run_values = get_run_values( inDir, name_base )


type = 'Primordial'
# type = 'Metals'

if type == 'Primordial': data_keys = [ 'cooling_rate', 'heating_rate', 'mean_molecular_weight']
if type == 'Metals': data_keys = [ 'cooling_rate', 'heating_rate', ]




data_cloudy = {}
for key in data_keys:
  dens_vals, redshift_vals, temp_vals, table =  get_cloudy_table( run_values, key, name_base, inDir )
  data_cloudy['density'] = dens_vals
  data_cloudy['redshift'] = redshift_vals
  data_cloudy['temperature'] = temp_vals
  data_cloudy[key] = table

data_cloudy_metals = {}
for key in data_keys:
  dens_vals, redshift_vals, temp_vals, table =  get_cloudy_table( run_values, key, name_base, inDir_metals )
  data_cloudy_metals['density'] = dens_vals
  data_cloudy_metals['redshift'] = redshift_vals
  data_cloudy_metals['temperature'] = temp_vals
  data_cloudy_metals[key] = table


fileName = 'data/CloudyData_UVB=HM2012.h5'
data_grackle = {}
for key in data_keys:
  dens_vals, redshift_vals, temp_vals, table =  get_grackle_table( key, fileName, type=type )
  data_grackle['density'] = dens_vals
  data_grackle['redshift'] = redshift_vals
  data_grackle['temperature'] = temp_vals
  data_grackle[key] = table


# indx_redshift = 0
n_redshift = 25
for indx_redshift in range(n_redshift):
  # print indx_redshift

  #Plot tables 
  n_rows = len(data_keys)      
  n_cols =  3
  fig, ax_list = plt.subplots(nrows=n_rows, ncols=n_cols, figsize=(10*n_cols,9.2*n_rows))
  plt.subplots_adjust(  wspace=0.3, hspace=0.3)



  for i,key in enumerate(data_keys):
    dens_vals_cl = data_cloudy['density']
    redshift_vals_cl = data_cloudy['redshift'] 
    temp_vals_cl = data_cloudy['temperature']

    dens_vals_gk = data_grackle['density']
    redshift_vals_gk = data_grackle['redshift'] 
    temp_vals_gk = data_grackle['temperature']
    
    if ( np.abs( dens_vals_gk - dens_vals_cl ) > 1e-6 ).any(): print 'Error: density mismatch'
    if ( np.abs( temp_vals_gk - temp_vals_cl ) > 1e-6 ).any(): print 'Error: temperature mismatch'
    
    temp_log = np.log10( temp_vals_cl )
    
    z_cl = data_cloudy['redshift'][indx_redshift]
    z_gk = data_grackle['redshift'][indx_redshift]
    if ( np.abs( z_gk - z_cl ) > 1e-6 ).any(): print 'Error: redshift mismatch'
    if i==0: print "\nIndex: {1}  z = {0:.2f}".format(z_cl, indx_redshift)
    
    
    data_gk = data_grackle[key][::-1, indx_redshift, :]
    data_cl = data_cloudy[key][::-1, indx_redshift, :]
    if type == 'Metals':
      floor = 1e-30
      data_gk = data_grackle[key][::-1, indx_redshift, :] + floor 
      data_primordial = data_cloudy[key][::-1, indx_redshift, :]
      data_metals = data_cloudy_metals[key][::-1, indx_redshift, :]
      data_cl = data_metals - data_primordial 
      data_cl[data_cl <= 0] = 0
      data_cl += floor
      # print data_cl.min(), data_cl.max()
      
    diff = ( data_cl - data_gk ) / data_gk
    
    if ( key == 'cooling_rate' or key == 'heating_rate' ):
      data_cl = np.log10( data_cl )
      data_gk = np.log10( data_gk )
    
    data_min = min( data_cl.min(), data_gk.min() )
    data_max = max( data_cl.max(), data_gk.max() )  
    
    if key == 'mean_molecular_weight':
      print "MMW: "
      print " Grackle:  {0:.3f}  {1:.3f}  ".format( data_gk.min(), data_gk.max() )
      print " Cloudy:   {0:.3f}  {1:.3f}  ".format( data_cl.min(), data_cl.max() )
    
    ax_row = ax_list[i]
    

    color_0 = 'jet'
    fs = 17
    fs_1 = 25

    ax = ax_row[0]
    im = ax.imshow( data_gk, extent=( temp_log[0], temp_log[-1], dens_vals_cl[0], dens_vals[-1]), aspect='auto', vmin=data_min, vmax=data_max, cmap=color_0)
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
    im = ax.imshow( data_cl, extent=( temp_log[0], temp_log[-1], dens_vals_cl[0], dens_vals[-1]), aspect='auto', vmin=data_min, vmax=data_max, cmap=color_0)
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
    im = ax.imshow( diff, extent=( temp_log[0], temp_log[-1], dens_vals_cl[0], dens_vals[-1]), aspect='auto', cmap=color_0)
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

# 
# 
# 
# 
# fileName = 'data/CloudyData_UVB=HM2012.h5'
# file = h5.File( fileName, 'r' )
# 
# 
# rates = file['CoolingRates']
# rates_primordial = rates['Primordial']
# 
# #Get values for temperature in the table
# temp_vals = rates_primordial['Cooling'].attrs['Temperature']
# temp_vals_log = np.log10( temp_vals )
# 
# #Get values for density in the table
# dens_vals = rates_primordial['Cooling'].attrs['Parameter1']
# 
# #Get values for redshift in the table
# redshift_vals = rates_primordial['Cooling'].attrs['Parameter2']
# 
# #Get cooling rates [ dens, redshift, temperature ]
# cooling_rate_all = rates_primordial['Cooling'][...]
# cooling_rate_0 = cooling_rate_all[0, 0, : ] 
# 
# diff = (cooling_rate_cloudy_0 - cooling_rate_0) / cooling_rate_0



# 
# #Get uv background photoheating and photoionization rates
# uvb_photoheating = file['UVBRates']['Photoheating']
# uvb_photoheating_HI = uvb_photoheating['piHI'][...]
# uvb_photoheating_HI = uvb_photoheating['piHeI'][...]
# uvb_photoheating_HI = uvb_photoheating['piHeII'][...]
# uvb_photoionization = file['UVBRates']['Chemistry']
# uvb_photoionization_HI = uvb_photoionization['k24'][...]
# uvb_photoionization_HeI = uvb_photoionization['k25'][...]
# uvb_photoionization_HeII = uvb_photoionization['k26'][...]
# 
# 
# #Load the HM2012 data extracted from the paper
# table_hm12 = np.loadtxt( 'data/hm12.dat' ).T
# data_hm12 = {
# 'redshift': table_hm12[0],
# 'photoionization':{
#   'HI': table_hm12[1],
#   'HeI': table_hm12[3],
#   'HeII': table_hm12[5],
#   },
# 'photoheating':{
#   'HI': table_hm12[2],
#   'HeI': table_hm12[4],
#   'HeII': table_hm12[6],
#   },
# }











# #Plot UVB uvb_rates
# nrows=1
# ncols = 1
# fig, ax = plt.subplots(nrows=nrows, ncols=ncols, figsize=(10*ncols,8*nrows))
# 
# lw = 3
# ax.plot( z, uvb_HI, linewidth=lw, label="HI" )
# ax.plot( z, uvb_HeI, linewidth=lw, label="HeI" )
# ax.plot( z, uvb_HeII, linewidth=lw, label="HeII" )
# 
# ax.set_yscale('log')
# ax.legend()
# ax.set_title('UVB Rates H&M 2012')
# ax.set_xlabel('Redshift')
# ax.set_ylabel('Photo-Heating Rate')
# 
# fig.savefig( 'uvb_rates.png',  bbox_inches='tight', dpi=100)
