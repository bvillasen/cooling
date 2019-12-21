import sys, os
import numpy as np
import h5py as h5
import matplotlib.pyplot as plt

cool_dir = os.path.dirname(os.getcwd()) + '/'
cloudy_dir = cool_dir + 'cloudy/'
uvb_dir = cool_dir + 'uv_background/'
tools_dir = cool_dir + 'tools/'
sys.path.extend([ uvb_dir, tools_dir ] )
from tools import create_directory, write_parameter_file
from load_grackle_output import *
from load_puchwein_data import *
from load_hm12_data import *





#Load Puchwein UVB Spectrum
uvb_spectrum_pw = {}
file_name = 'data/bkgthick.out'
uvb_spectrum_pw['redshift'], uvb_spectrum_pw['lambda'], uvb_spectrum_pw['J'] = load_puchwein_spectrum( file_name )


#Load HM12 UVB Spectrum
file_name = 'data/uvb_HM12.dat'
uvb_spectrum_hm = {}
uvb_spectrum_hm['redshift'], uvb_spectrum_hm['lambda'], uvb_spectrum_hm['J'] = load_hm12_spectrum( file_name )

diff = uvb_spectrum_hm['redshift'] - uvb_spectrum_pw['redshift']  


file_name = 'data/CloudyData_UVB=HM2012.h5'
rates_grackle = load_grackle_rates( file_name )


file_name = 'data/hm12.dat'
rates_hm = load_hm12_rates( file_name )

file_name = 'data/ionrate.out'
rates_pw = load_puchwein_rates( file_name )


z_gk = rates_grackle['redshift']
z_hm = rates_hm['redshift']

diff_HI = ( rates_grackle['photoionization']['HI']  -  rates_hm['photoionization']['HI'] ) / rates_hm['photoionization']['HI']
diff_HI = ( rates_grackle['photoionization']['HeI']  -  rates_hm['photoionization']['HeI'] ) / rates_hm['photoionization']['HeI']
diff_HeII = ( rates_grackle['photoionization']['HeII']  -  rates_hm['photoionization']['HeII'] ) / rates_hm['photoionization']['HeII']

#Plot Heating and Ionizatiosnates
nrows=1
ncols = 2
fig, (ax1,ax2) = plt.subplots(nrows=nrows, ncols=ncols, figsize=(10*ncols,8*nrows))

fs = 17
lw = 3

# ax1.plot( rates_pw['redshift'], rates_pw['photoheating']['HI'], c='C1', linewidth=lw, label="HI" )
# ax1.plot( rates_pw['redshift'], rates_pw['photoheating']['HeI'], c='C2', linewidth=lw, label="HeI" )
# ax1.plot( rates_pw['redshift'], rates_pw['photoheating']['HeII'], c='C3',linewidth=lw, label="HeII" )

alpha = 0.5
ax1.plot( rates_hm['redshift'], rates_hm['photoheating']['HI'],  c='C1', linewidth=lw, alpha=alpha, label="HI" )
ax1.plot( rates_hm['redshift'], rates_hm['photoheating']['HeI'],  c='C2', linewidth=lw, alpha=alpha, label="HeI" )
ax1.plot( rates_hm['redshift'], rates_hm['photoheating']['HeII'],  c='C3',linewidth=lw, alpha=alpha, label="HeII" )

ax1.plot( rates_grackle['redshift'], rates_grackle['photoheating']['HI'], '--', c='C1', linewidth=lw,  )
ax1.plot( rates_grackle['redshift'], rates_grackle['photoheating']['HeI'], '--', c='C2', linewidth=lw,  )
ax1.plot( rates_grackle['redshift'], rates_grackle['photoheating']['HeII'], '--', c='C3',linewidth=lw,  )

ax1.set_yscale('log')
ax1.legend( fontsize = fs)
# ax.set_title('UVB Rates H&M 2012')
ax1.set_xlabel('Redshift', fontsize=fs)
ax1.set_ylabel(r'Photoheating Rate   [eV s$^{-1}$]', fontsize=fs)

# ax2.plot( rates_pw['redshift'], rates_pw['photoionization']['HI'], c='C1', linewidth=lw, label="HI" )
# ax2.plot( rates_pw['redshift'], rates_pw['photoionization']['HeI'], c='C2', linewidth=lw, label="HeI" )
# ax2.plot( rates_pw['redshift'], rates_pw['photoionization']['HeII'], c='C3',linewidth=lw, label="HeII" )

ax2.plot( rates_hm['redshift'], rates_hm['photoionization']['HI'],  c='C1', linewidth=lw,  label="HI", alpha=alpha  )
ax2.plot( rates_hm['redshift'], rates_hm['photoionization']['HeI'],  c='C2', linewidth=lw,  label="HeI", alpha=alpha )
ax2.plot( rates_hm['redshift'], rates_hm['photoionization']['HeII'],  c='C3',linewidth=lw, label="HeII", alpha=alpha  )

ax2.plot( rates_grackle['redshift'], rates_grackle['photoionization']['HI'], '--', c='C1', linewidth=lw,  )
ax2.plot( rates_grackle['redshift'], rates_grackle['photoionization']['HeI'], '--', c='C2', linewidth=lw,  )
ax2.plot( rates_grackle['redshift'], rates_grackle['photoionization']['HeII'], '--', c='C3',linewidth=lw,  )

ax2.set_yscale('log')
ax2.legend( fontsize = fs)
# ax.set_title('UVB Rates H&M 2012')
ax2.set_xlabel('Redshift', fontsize=fs)
ax2.set_ylabel(r'Photoionization Rate   [s$^{-1}$]', fontsize=fs)


fig.savefig( 'figures/heating_ionization_rates.png',  bbox_inches='tight', dpi=100)


# 
# #Plot Heating rates
# nrows=1
# ncols = 1
# fig, ax = plt.subplots(nrows=nrows, ncols=ncols, figsize=(10*ncols,8*nrows))
# 
# fs = 17
# lw = 3
# ax.plot( rates_pw['redshift'], rates_pw['photoheating']['HI'], c='C1', linewidth=lw, label="HI" )
# ax.plot( rates_pw['redshift'], rates_pw['photoheating']['HeI'], c='C2', linewidth=lw, label="HeI" )
# ax.plot( rates_pw['redshift'], rates_pw['photoheating']['HeII'], c='C3',linewidth=lw, label="HeII" )
# 
# ax.plot( rates_hm['redshift'], rates_hm['photoheating']['HI'], '--', c='C1', linewidth=lw,  )
# ax.plot( rates_hm['redshift'], rates_hm['photoheating']['HeI'], '--', c='C2', linewidth=lw,  )
# ax.plot( rates_hm['redshift'], rates_hm['photoheating']['HeII'], '--', c='C3',linewidth=lw,  )
# 
# ax.plot( rates_grackle['redshift'], rates_grackle['photoheating']['HI'], '.', c='C1', linewidth=lw,  )
# ax.plot( rates_grackle['redshift'], rates_grackle['photoheating']['HeI'], '.', c='C2', linewidth=lw,  )
# ax.plot( rates_grackle['redshift'], rates_grackle['photoheating']['HeII'], '.', c='C3',linewidth=lw,  )
# 
# ax.set_yscale('log')
# ax.legend( fontsize = fs)
# # ax.set_title('UVB Rates H&M 2012')
# ax.set_xlabel('Redshift', fontsize=fs)
# ax.set_ylabel(r'Photoheating Rate   [eV s$^{-1}$]', fontsize=fs)
# fig.savefig( 'figures/heating_rates.png',  bbox_inches='tight', dpi=100)
# 
# #Plot Ionization rates
# nrows=1
# ncols = 1
# fig, ax = plt.subplots(nrows=nrows, ncols=ncols, figsize=(10*ncols,8*nrows))
# 
# fs = 17
# lw = 3
# ax.plot( rates_pw['redshift'], rates_pw['photoionization']['HI'], c='C1', linewidth=lw, label="HI" )
# ax.plot( rates_pw['redshift'], rates_pw['photoionization']['HeI'], c='C2', linewidth=lw, label="HeI" )
# ax.plot( rates_pw['redshift'], rates_pw['photoionization']['HeII'], c='C3',linewidth=lw, label="HeII" )
# 
# ax.plot( rates_hm['redshift'], rates_hm['photoionization']['HI'], '--', c='C1', linewidth=lw,  )
# ax.plot( rates_hm['redshift'], rates_hm['photoionization']['HeI'], '--', c='C2', linewidth=lw,  )
# ax.plot( rates_hm['redshift'], rates_hm['photoionization']['HeII'], '--', c='C3',linewidth=lw,  )
# 
# ax.plot( rates_grackle['redshift'], rates_grackle['photoionization']['HI'], '.', c='C1', linewidth=lw,  )
# ax.plot( rates_grackle['redshift'], rates_grackle['photoionization']['HeI'], '.', c='C2', linewidth=lw,  )
# ax.plot( rates_grackle['redshift'], rates_grackle['photoionization']['HeII'], '.', c='C3',linewidth=lw,  )
# 
# ax.set_yscale('log')
# ax.legend( fontsize = fs)
# # ax.set_title('UVB Rates H&M 2012')
# ax.set_xlabel('Redshift', fontsize=fs)
# ax.set_ylabel(r'Photoionization Rate   [s$^{-1}$]', fontsize=fs)
# fig.savefig( 'figures/ionization_rates.png',  bbox_inches='tight', dpi=100)
# 

# 
# z_vals = [ 1.1, 3.6, 4.9, 6.9, 9.1, 11.2  ]
# indxs_pw, indxs_hm = [], []
# for z in z_vals:
#   diff = np.abs(uvb_spectrum_pw['redshift'] - z)
#   indx = np.where( diff == diff.min())[0]
#   indxs_pw.append(indx[0])
# 
#   diff = np.abs(uvb_spectrum_hm['redshift'] - z)
#   indx = np.where( diff == diff.min())[0]
#   indxs_hm.append(indx[0])
# 
# n_rows = 3
# n_cols =  2
# fig, ax_list = plt.subplots(nrows=n_rows, ncols=n_cols, figsize=(10*n_cols,9.2*n_rows))
# plt.subplots_adjust(  wspace=0.3, hspace=0.3)
# ax_list = ax_list.flatten()
# 
# fs = 22
# for i in range( n_rows*n_cols):
# 
#   indx_pw = indxs_pw[i]
#   indx_hm = indxs_hm[i]
# 
#   z_hm = uvb_spectrum_hm['redshift'][indx_hm]
#   z_pw = uvb_spectrum_pw['redshift'][indx_pw]
#   if np.abs( z_hm - z_pw ) > 1e-4: print "ERROR: redshift missmatch"
# 
#   ax = ax_list[i]
#   ax.plot( uvb_spectrum_hm['lambda'], uvb_spectrum_hm['J'][:,indx_hm], label='HM12' ) 
#   ax.plot( uvb_spectrum_pw['lambda'], uvb_spectrum_pw['J'][:,indx_pw], label='Puchwein+18' )
#   ax.legend( fontsize = 18 )
#   text = 'z = {0:.1f}'.format( z_hm )
#   ax.text(0.2, 0.8, text, fontsize=fs, horizontalalignment='right', verticalalignment='center', transform=ax.transAxes,)
# 
#   ax.set_xscale('log')
#   ax.set_yscale('log')
#   ax.set_ylim( 1e-30, 1e-18)
#   ax.set_xlim( 5, 5e3)
# 
#   ax.set_ylabel( r'$J \,\, [\mathrm{erg} \,\, \mathrm{cm}^{-2} \,\, \mathrm{s}^{-1} \,\, \mathrm{Hz}^{-1}  \,\, \mathrm{sr}^{-1}]$', fontsize=fs)
#   ax.set_xlabel( r'$\lambda \,\, [\AA]$', fontsize=fs)
# 
#   ax.tick_params(axis='both', which='major', labelsize=18, size=5)
#   ax.tick_params(axis='both', which='minor', labelsize=15, size=3)
# 
# fig.savefig( 'figures/ubv_comparison_1.png',  bbox_inches='tight', dpi=100 )