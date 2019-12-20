import sys, os
import numpy as np
import h5py as h5

root_dir = p = os.path.abspath('..')
tools_dir = root_dir + '/tools/'
cloudy_tools_dir = root_dir + '/cloudy_tools/'
figures_dir = root_dir + '/figures/'
sys.path.extend([ tools_dir, cloudy_tools_dir ] )
from tools import create_directory
from load_cloudy_output import *

#Load Cloudy tables
inDir = '/home/bruno/Desktop/Dropbox/Developer/cloudy_cooling_tools/outputs/cooling_uvHM_metals_off/'
inDir_metals = '/home/bruno/Desktop/Dropbox/Developer/cloudy_cooling_tools/outputs/cooling_uvHM_metals_on/'
name_base = 'cooling_run'

# type = 'Primordial'
# type = 'Metals'
Metals_on = False
# 
# run_values = get_run_values( inDir, name_base )
# data_keys = [ 'cooling_rate', 'heating_rate', 'mean_molecular_weight']
# cloudy_keys = { 'cooling_rate':"Cooling", 'heating_rate':"Heating", 'mean_molecular_weight':"MMW"}
# data_cloudy_primordial = {}
# for key in data_keys:
#   dens_vals, redshift_vals, temp_vals, table =  get_cloudy_table( run_values, key, name_base, inDir )
#   data_cloudy_primordial['density'] = dens_vals
#   data_cloudy_primordial['temperature'] = temp_vals
#   # data_cloudy_primordial['redshift'] = redshift_vals
#   # data_cloudy_primordial[key] = table
# 
#   #Appenbd the duplicate lat redshift
#   z_last = np.array([ redshift_vals[-1]])
#   redshift_vals = np.concatenate((redshift_vals, z_last ) )
#   data_cloudy_primordial['redshift'] = redshift_vals
# 
#   n_dens, n_redshift, n_temp = len(dens_vals), len(redshift_vals), len(temp_vals)
#   table_new = np.zeros([n_dens, n_redshift, n_temp])
#   for i in range(n_redshift-1):
#     table_new[:, i, :] = table[:, i, :]
#   table_new[:, -1, :] = table[:, -1, :] 
#   data_cloudy_primordial[cloudy_keys[key]] = table_new
# 
# 
# if Metals_on:
#   data_cloudy_metals = {}
#   for key in data_keys:
#     dens_vals, redshift_vals, temp_vals, table =  get_cloudy_table( run_values, key, name_base, inDir_metals )
#     data_cloudy_metals['density'] = dens_vals
#     data_cloudy_metals['temperature'] = temp_vals
# 
#     #Appenbd the duplicate lat redshift
#     z_last = np.array([ redshift_vals[-1]])
#     redshift_vals = np.concatenate((redshift_vals, z_last ) )
#     data_cloudy_metals['redshift'] = redshift_vals
# 
#     n_dens, n_redshift, n_temp = len(dens_vals), len(redshift_vals), len(temp_vals)
#     table_new = np.zeros([n_dens, n_redshift, n_temp])
#     for i in range(n_redshift-1):
#       table_new[:, i, :] = table[:, i, :]
#     table_new[:, -1, :] = table[:, -1, :] 
#     data_cloudy_metals[cloudy_keys[key]] = table_new
# 


#Load grackle file tables
fileName = 'data/CloudyData_UVB=HM2012.h5'
file_gk = h5.File( fileName, 'r' )



fileName = 'data/CloudyData_UVB=HM2012_cloudy_primordial.h5'
file_br = h5.File( fileName, 'w' )

# #Get Cooling Rate
root_name = 'CoolingRates'
file_br.create_group( root_name )
for type in file_gk[root_name].keys():
  print ' ' + type
  group_gk = file_gk[root_name][type]
  group_br = file_br[root_name].create_group(type)
  for field in group_gk.keys():
    print '  ' + field
    field_group_gk = group_gk[field]
    data_gk = field_group_gk[...]
    if type == 'Primordial':
      print "  Cloudy data: ", field
      
      
      # data_cl = data_cloudy_primordial[field]
      
    # if type == 'Metals':
    #   if Metals_on:
    #     print "  Cloudy data: ", field
    #     data_cl = data_cloudy_metals[field] - data_cloudy_primordial[field]
    #     data_cl[data_cl <= 0] = 0
    #     floor = 1e-30
    #     data_cl += floor
    
    data_cl = data_gk
    # diff = ( data_cl - data_gk ) / data_gk
    diff = data_gk
    print ' {0}  {1}'.format( diff.min(), diff.max())
      
    field_group_br = group_br.create_dataset( field, data=data_cl )
    for attr in field_group_gk.attrs.keys():
      print '   ' + attr
      field_group_br.attrs[attr] = field_group_gk.attrs[attr]

# #Get UVBRates
root_name = 'UVBRates'
print root_name
file_br.create_group( root_name )
for key in ['z', 'Info']:
  print ' ' + key
  data = file_gk[root_name][key][...]
  if key == 'Info': data = np.array('Haardt & Madau (2012, ApJ, 746, 125) [Galaxies & Quasars]  Test by Bruno',  dtype='|S72')
  file_br[root_name].create_dataset( key, data=data )

for key in ['Chemistry', 'Photoheating']:
  print ' ' + key
  group = file_gk[root_name][key]
  group_br = file_br[root_name].create_group( key )
  for field in group.keys():
    if field not in ['k24', 'k25', 'k26', 'piHI', 'piHeI', 'piHeII']: continue
    print field
    data = group[field][...]
    group_br.create_dataset( field, data=data )

file_gk.close()
file_br.close()



















# cooling_rates = prim_cool_gk = file_gk['CoolingRates']['Primordial']['Cooling']
# 
# 
# prim_cool_gk = file_gk['CoolingRates']['Primordial']['Cooling'][...]
# prim_heat_gk = file_gk['CoolingRates']['Primordial']['Heating'][...]
# prim_mmw_gk = file_gk['CoolingRates']['Primordial']['MMW'][...]
# metal_cool_gk = file_gk['CoolingRates']['Metals']['Cooling'][...]
# metal_heat_gk = file_gk['CoolingRates']['Metals']['Heating'][...]
# 
# uvb_info = np.array('Haardt & Madau (2012, ApJ, 746, 125) [Galaxies & Quasars]  Test by Bruno',  dtype='|S72')
# uvb_z_gk = file_gk['UVBRates']['z'][...]
# uvb_k24_gk = file_gk['UVBRates']['Chemistry']['k24'][...]
# uvb_k25_gk = file_gk['UVBRates']['Chemistry']['k25'][...]
# uvb_k26_gk = file_gk['UVBRates']['Chemistry']['k26'][...]
# 
# uvb_piHI = file_gk['UVBRates']['Photoheating']['piHI'][...] 
# uvb_piHeI = file_gk['UVBRates']['Photoheating']['piHeI'][...] 
# uvb_piHeII = file_gk['UVBRates']['Photoheating']['piHeII'][...] 

# file_gk.close()




# fileName = 'data/CloudyData_UVB=HM2012_bruno.h5'
# file = h5.File( fileName, 'w' )
# 



# 
# 
# fileName = 'data/CloudyData_UVB=HM2012_bruno.h5'
# file = h5.File( fileName, 'w' )
# 
# 
# dens_vals = np.array([-10. ,  -9.5,  -9. ,  -8.5,  -8. ,  -7.5,  -7. ,  -6.5,  -6. ,
#         -5.5,  -5. ,  -4.5,  -4. ,  -3.5,  -3. ,  -2.5,  -2. ,  -1.5,
#         -1. ,  -0.5,   0. ,   0.5,   1. ,   1.5,   2. ,   2.5,   3. ,
#          3.5,   4. ])
# 
# redshift_vals = np.array([ 0.     ,  0.12202,  0.25893,  0.41254,  0.58489,  0.77828,
#         0.99526,  1.2387 ,  1.5119 ,  1.8184 ,  2.1623 ,  2.5481 ,
#         2.9811 ,  3.4668 ,  4.0119 ,  4.6234 ,  5.3096 ,  6.0795 ,
#         6.9433 ,  7.9125 ,  9.     , 10.22   , 11.589  , 13.125  ,
#        14.849  , 14.849  ])
# 
# temp_vals = np.array([1.000000e+01, 1.122018e+01, 1.258925e+01, 1.412538e+01,
#        1.584893e+01, 1.778279e+01, 1.995262e+01, 2.238721e+01,
#        2.511886e+01, 2.818383e+01, 3.162278e+01, 3.548134e+01,
#        3.981072e+01, 4.466836e+01, 5.011872e+01, 5.623413e+01,
#        6.309573e+01, 7.079458e+01, 7.943282e+01, 8.912509e+01,
#        1.000000e+02, 1.122018e+02, 1.258925e+02, 1.412538e+02,
#        1.584893e+02, 1.778279e+02, 1.995262e+02, 2.238721e+02,
#        2.511886e+02, 2.818383e+02, 3.162278e+02, 3.548134e+02,
#        3.981072e+02, 4.466836e+02, 5.011872e+02, 5.623413e+02,
#        6.309573e+02, 7.079458e+02, 7.943282e+02, 8.912509e+02,
#        1.000000e+03, 1.122018e+03, 1.258925e+03, 1.412538e+03,
#        1.584893e+03, 1.778279e+03, 1.995262e+03, 2.238721e+03,
#        2.511886e+03, 2.818383e+03, 3.162278e+03, 3.548134e+03,
#        3.981072e+03, 4.466836e+03, 5.011872e+03, 5.623413e+03,
#        6.309573e+03, 7.079458e+03, 7.943282e+03, 8.912509e+03,
#        1.000000e+04, 1.122018e+04, 1.258925e+04, 1.412538e+04,
#        1.584893e+04, 1.778279e+04, 1.995262e+04, 2.238721e+04,
#        2.511886e+04, 2.818383e+04, 3.162278e+04, 3.548134e+04,
#        3.981072e+04, 4.466836e+04, 5.011872e+04, 5.623413e+04,
#        6.309573e+04, 7.079458e+04, 7.943282e+04, 8.912509e+04,
#        1.000000e+05, 1.122018e+05, 1.258925e+05, 1.412538e+05,
#        1.584893e+05, 1.778279e+05, 1.995262e+05, 2.238721e+05,
#        2.511886e+05, 2.818383e+05, 3.162278e+05, 3.548134e+05,
#        3.981072e+05, 4.466836e+05, 5.011872e+05, 5.623413e+05,
#        6.309573e+05, 7.079458e+05, 7.943282e+05, 8.912509e+05,
#        1.000000e+06, 1.122018e+06, 1.258925e+06, 1.412538e+06,
#        1.584893e+06, 1.778279e+06, 1.995262e+06, 2.238721e+06,
#        2.511886e+06, 2.818383e+06, 3.162278e+06, 3.548134e+06,
#        3.981072e+06, 4.466836e+06, 5.011872e+06, 5.623413e+06,
#        6.309573e+06, 7.079458e+06, 7.943282e+06, 8.912509e+06,
#        1.000000e+07, 1.122018e+07, 1.258925e+07, 1.412538e+07,
#        1.584893e+07, 1.778279e+07, 1.995262e+07, 2.238721e+07,
#        2.511886e+07, 2.818383e+07, 3.162278e+07, 3.548134e+07,
#        3.981072e+07, 4.466836e+07, 5.011872e+07, 5.623413e+07,
#        6.309573e+07, 7.079458e+07, 7.943282e+07, 8.912509e+07,
#        1.000000e+08, 1.122018e+08, 1.258925e+08, 1.412538e+08,
#        1.584893e+08, 1.778279e+08, 1.995262e+08, 2.238721e+08,
#        2.511886e+08, 2.818383e+08, 3.162278e+08, 3.548134e+08,
#        3.981072e+08, 4.466836e+08, 5.011872e+08, 5.623413e+08,
#        6.309573e+08, 7.079458e+08, 7.943282e+08, 8.912509e+08,
#        1.000000e+09])
# 
# 
# n_dens, n_redshift, n_temp = len(dens_vals), len(redshift_vals), len(temp_vals)
# # prim_cool_data = np.zeros( [n_dens, n_redshift, n_temp])
# # prim_heat_data = np.zeros( [n_dens, n_redshift, n_temp])
# # prim_mmw_data  = np.zeros( [n_dens, n_redshift, n_temp])
# # metal_cool_data = np.zeros( [n_dens, n_redshift, n_temp])
# # metal_heat_data = np.zeros( [n_dens, n_redshift, n_temp])
# 
# prim_cool_data = prim_cool_gk
# prim_heat_data = prim_heat_gk
# prim_mmw_data  = prim_mmw_gk
# metal_cool_data = metal_cool_gk
# metal_heat_data = metal_heat_gk
# 
# 
# cooling_rates = file.create_group( 'CoolingRates' )
# cooling_rates_prim = cooling_rates.create_group( 'Primordial')
# prim_cool = cooling_rates_prim.create_dataset( 'Cooling', data=prim_cool_data )
# prim_heat = cooling_rates_prim.create_dataset( 'Heating', data=prim_heat_data )
# prim_mmw  = cooling_rates_prim.create_dataset( 'MMW', data=prim_mmw_data )
# 
# 
# 
# prim_cool.attrs['Rank'] = 3
# prim_cool.attrs['Dimension'] = np.array([ n_dens, n_redshift, n_temp ])
# prim_cool.attrs['Parameter1'] = dens_vals
# prim_cool.attrs['Parameter1_Name'] = 'hden'
# prim_cool.attrs['Parameter2'] = redshift_vals
# prim_cool.attrs['Parameter2_Name'] = 'redshift'
# prim_cool.attrs['Temperature'] = temp_vals
# 
# prim_heat.attrs['Rank'] = 3
# prim_heat.attrs['Dimension'] = np.array([ n_dens, n_redshift, n_temp ])
# prim_heat.attrs['Parameter1'] = dens_vals
# prim_heat.attrs['Parameter1_Name'] = 'hden'
# prim_heat.attrs['Parameter2'] = redshift_vals
# prim_heat.attrs['Parameter2_Name'] = 'redshift'
# prim_heat.attrs['Temperature'] = temp_vals
# 
# 
# prim_mmw.attrs['Rank'] = 3
# prim_mmw.attrs['Dimension'] = np.array([ n_dens, n_redshift, n_temp ])
# prim_mmw.attrs['Parameter1'] = dens_vals
# prim_mmw.attrs['Parameter1_Name'] = 'hden'
# prim_mmw.attrs['Parameter2'] = redshift_vals
# prim_mmw.attrs['Parameter2_Name'] = 'redshift'
# prim_mmw.attrs['Temperature'] = temp_vals
# 
# 
# 
# 
# 
# cooling_rates_metals = cooling_rates.create_group( 'Metals')
# metal_cool = cooling_rates_metals.create_dataset( 'Cooling', data=metal_cool_data )
# metal_heat = cooling_rates_metals.create_dataset( 'Heating', data=metal_heat_data )
# 
# 
# 
# metal_cool.attrs['Rank'] = 3
# metal_cool.attrs['Dimension'] = np.array([ n_dens, n_redshift, n_temp ])
# metal_cool.attrs['Parameter1'] = dens_vals
# metal_cool.attrs['Parameter1_Name'] = 'hden'
# metal_cool.attrs['Parameter2'] = redshift_vals
# metal_cool.attrs['Parameter2_Name'] = 'redshift'
# metal_cool.attrs['Temperature'] = temp_vals
# 
# metal_heat.attrs['Rank'] = 3
# metal_heat.attrs['Dimension'] = np.array([ n_dens, n_redshift, n_temp ])
# metal_heat.attrs['Parameter1'] = dens_vals
# metal_heat.attrs['Parameter1_Name'] = 'hden'
# metal_heat.attrs['Parameter2'] = redshift_vals
# metal_heat.attrs['Parameter2_Name'] = 'redshift'
# metal_heat.attrs['Temperature'] = temp_vals
# 
# 
# 
# ###UVBackgrounf Rates
# 
# uvb_rates = file.create_group( 'UVBRates' )
# 
# info = np.array('Haardt & Madau (2012, ApJ, 746, 125) [Galaxies & Quasars]  Test by Bruno',  dtype='|S72')
# uvb_rates_info = uvb_rates.create_dataset('Info', data=info )
# 
# 
# z = np.array([ 0.     ,  0.04912,  0.1006 ,  0.1547 ,  0.2114 ,  0.2709 ,
#         0.3333 ,  0.3988 ,  0.4675 ,  0.5396 ,  0.6152 ,  0.6945 ,
#         0.7778 ,  0.8651 ,  0.9567 ,  1.053  ,  1.154  ,  1.259  ,
#         1.37   ,  1.487  ,  1.609  ,  1.737  ,  1.871  ,  2.013  ,
#         2.16   ,  2.316  ,  2.479  ,  2.649  ,  2.829  ,  3.017  ,
#         3.214  ,  3.421  ,  3.638  ,  3.866  ,  4.105  ,  4.356  ,
#         4.619  ,  4.895  ,  5.184  ,  5.488  ,  5.807  ,  6.141  ,
#         6.492  ,  6.859  ,  7.246  ,  7.65   ,  8.075  ,  8.521  ,
#         8.989  ,  9.479  ,  9.994  , 10.53   , 11.1    , 11.69   ,
#        12.32   , 12.97   , 13.66   , 14.38   , 15.13   ])
# uvb_rates_redshift = uvb_rates.create_dataset('z', data=z )
# 
# uvb_rates_chemistry = uvb_rates.create_group('Chemistry')
# 
# # Hydrogen ionoztion rates from HM12 paper
# k24_data = np.array([2.26435464e-14, 2.82806165e-14, 3.52419650e-14, 4.38035789e-14,
#        5.43043383e-14, 6.71260552e-14, 8.27130147e-14, 1.01570263e-13,
#        1.24266082e-13, 1.51416567e-13, 1.83639080e-13, 2.21563832e-13,
#        2.65733685e-13, 3.16572194e-13, 3.74133978e-13, 4.38301059e-13,
#        5.08049623e-13, 5.81786654e-13, 6.56665491e-13, 7.28967651e-13,
#        7.95595959e-13, 8.55152289e-13, 9.04243811e-13, 9.39533118e-13,
#        9.58794857e-13, 9.60658899e-13, 9.45345651e-13, 9.14571589e-13,
#        8.71195210e-13, 8.18746787e-13, 7.61191078e-13, 7.02053817e-13,
#        6.44608375e-13, 5.91136071e-13, 5.43258157e-13, 5.01670985e-13,
#        4.67443550e-13, 4.39318963e-13, 4.10668891e-13, 3.58737069e-13,
#        2.91840727e-13, 2.29117328e-13, 1.73955227e-13, 1.28326749e-13,
#        9.24206578e-14, 6.52575837e-14, 4.53476218e-14, 3.11055772e-14,
#        2.11280634e-14, 1.42403698e-14, 9.54328103e-15, 6.36993712e-15,
#        4.24618916e-15, 2.90645607e-15, 1.72543857e-15, 1.01288479e-15,
#        5.89558697e-16, 3.40078783e-16, 1.94108444e-16])
# k24 = uvb_rates_chemistry.create_dataset('k24', data=k24_data)
# 
# # Helium ionoztion rates from HM12 paper
# k25_data = np.array([5.64211358e-16, 6.87250092e-16, 8.37166088e-16, 1.01959055e-15,
#        1.24109453e-15, 1.50898052e-15, 1.83189436e-15, 2.21951829e-15,
#        2.68174441e-15, 3.22930690e-15, 3.87247495e-15, 4.62048936e-15,
#        5.47916141e-15, 6.44995849e-15, 7.52527402e-15, 8.68518917e-15,
#        9.89072349e-15, 1.10772645e-14, 1.21430028e-14, 1.29453312e-14,
#        1.34711019e-14, 1.37088872e-14, 1.36014717e-14, 1.31030300e-14,
#        1.22001389e-14, 1.09115517e-14, 9.28727524e-15, 7.42210400e-15,
#        5.45758175e-15, 3.61178414e-15, 2.14322766e-15, 1.17022987e-15,
#        6.09523570e-16, 3.10673002e-16, 1.56699024e-16, 7.82491806e-17,
#        3.86140615e-17, 1.87981841e-17, 8.82951163e-18, 3.32094681e-18,
#        1.20374433e-18, 4.55084515e-19, 1.78562554e-19, 7.23015730e-20,
#        3.01006051e-20, 1.29614557e-20, 5.85864359e-21, 2.83609108e-21,
#        1.49109242e-21, 8.49726749e-22, 5.19132064e-22, 3.38852325e-22,
#        2.20723159e-22, 1.49181153e-22, 1.03211572e-22, 7.16822904e-23,
#        4.99508123e-23, 3.49038664e-23, 2.02465180e-23])
# k25 = uvb_rates_chemistry.create_dataset('k25', data=k25_data)
# 
# k26_data = np.array([1.23691051e-14, 1.55589211e-14, 1.95332637e-14, 2.44645177e-14,
#        3.05634363e-14, 3.80685066e-14, 4.72433212e-14, 5.83935030e-14,
#        7.18254922e-14, 8.79204897e-14, 1.07075993e-13, 1.29717312e-13,
#        1.56112838e-13, 1.86513435e-13, 2.20968931e-13, 2.59279870e-13,
#        3.00884940e-13, 3.44759369e-13, 3.89295827e-13, 4.32189685e-13,
#        4.71774281e-13, 5.06908986e-13, 5.35309153e-13, 5.55270430e-13,
#        5.65272153e-13, 5.64581059e-13, 5.53716136e-13, 5.33934719e-13,
#        5.07068530e-13, 4.74928714e-13, 4.40183665e-13, 4.05217499e-13,
#        3.71731131e-13, 3.41005262e-13, 3.13834290e-13, 2.90440292e-13,
#        2.70273290e-13, 2.52802209e-13, 2.36616494e-13, 2.13169957e-13,
#        1.83157372e-13, 1.53535010e-13, 1.25073047e-13, 9.88499315e-14,
#        7.58574461e-14, 5.66629840e-14, 4.13320132e-14, 2.95252475e-14,
#        2.07271540e-14, 1.43460712e-14, 9.82189438e-15, 6.67641271e-15,
#        4.53703350e-15, 3.24705815e-15, 2.02589354e-15, 1.24238032e-15,
#        7.54402756e-16, 4.54019565e-16, 2.68414491e-16])
# k26 = uvb_rates_chemistry.create_dataset('k26', data=k26_data)
# 
# 
# 
# uvb_rates_photoheating = uvb_rates.create_group('Photoheating')
# 
# piHI_data = np.array([8.89846181e-14, 1.11366233e-13, 1.39077459e-13, 1.73257273e-13,
#        2.15259025e-13, 2.66649931e-13, 3.29192056e-13, 4.04942704e-13,
#        4.96066609e-13, 6.05077567e-13, 7.34299095e-13, 8.86300975e-13,
#        1.06303218e-12, 1.26612389e-12, 1.49600345e-12, 1.75171781e-12,
#        2.02958682e-12, 2.32297359e-12, 2.62095571e-12, 2.90791909e-12,
#        3.17343050e-12, 3.41041933e-12, 3.60485244e-12, 3.74435711e-12,
#        3.81926013e-12, 3.82399263e-12, 3.76066150e-12, 3.63673661e-12,
#        3.46377990e-12, 3.25560392e-12, 3.02831255e-12, 2.79703506e-12,
#        2.57372047e-12, 2.36731657e-12, 2.18291980e-12, 2.02361749e-12,
#        1.89061855e-12, 1.78030976e-12, 1.67071975e-12, 1.47875803e-12,
#        1.23016019e-12, 9.90666497e-13, 7.72073925e-13, 5.83962124e-13,
#        4.30382332e-13, 3.10257371e-13, 2.19540942e-13, 1.52908193e-13,
#        1.05149898e-13, 7.15654258e-14, 4.83252777e-14, 3.24591053e-14,
#        2.17841053e-14, 1.51907405e-14, 9.20978572e-15, 5.50934841e-15,
#        3.26811799e-15, 1.92262363e-15, 1.11605762e-15])
# piHI = uvb_rates_photoheating.create_dataset( 'piHI', data=piHI_data)
# 
# piHeI_data = np.array([1.12400610e-13, 1.39824906e-13, 1.73820857e-13, 2.15821910e-13,
#        2.67552433e-13, 3.31019530e-13, 4.08488163e-13, 5.02563767e-13,
#        6.15965189e-13, 7.51834860e-13, 9.12978160e-13, 1.10264804e-12,
#        1.32297856e-12, 1.57593355e-12, 1.86158580e-12, 2.17792419e-12,
#        2.51984862e-12, 2.87763338e-12, 3.23653328e-12, 3.57538390e-12,
#        3.88080540e-12, 4.14121046e-12, 4.33770078e-12, 4.45376286e-12,
#        4.47800165e-12, 4.40564771e-12, 4.24261334e-12, 4.00401034e-12,
#        3.71100843e-12, 3.38772480e-12, 3.06697560e-12, 2.77323202e-12,
#        2.51596561e-12, 2.29553173e-12, 2.10969350e-12, 1.95494009e-12,
#        1.82337714e-12, 1.70870451e-12, 1.60565313e-12, 1.46874259e-12,
#        1.29978443e-12, 1.12736989e-12, 9.53714572e-13, 7.83902281e-13,
#        6.24990185e-13, 4.83493061e-13, 3.63693652e-13, 2.66630280e-13,
#        1.91160500e-13, 1.34503311e-13, 9.32524337e-14, 6.40120903e-14,
#        4.38478135e-14, 3.16893981e-14, 1.99918494e-14, 1.24007223e-14,
#        7.63197171e-15, 4.67268934e-15, 2.80418296e-15])
# piHeI = uvb_rates_photoheating.create_dataset( 'piHeI', data=piHeI_data)
# 
# piHeII_data = np.array([1.14575931e-14, 1.38839545e-14, 1.68141850e-14, 2.03460103e-14,
#        2.45946268e-14, 2.96895815e-14, 3.57746443e-14, 4.30182062e-14,
#        5.15822688e-14, 6.16510536e-14, 7.33935888e-14, 8.69556832e-14,
#        1.02432756e-13, 1.19837016e-13, 1.39036132e-13, 1.59702415e-13,
#        1.81214088e-13, 2.02539803e-13, 2.22137383e-13, 2.37723881e-13,
#        2.48349426e-13, 2.53833353e-13, 2.53064976e-13, 2.45167982e-13,
#        2.29880459e-13, 2.07455635e-13, 1.78918972e-13, 1.45997660e-13,
#        1.11185093e-13, 7.78988126e-14, 4.99766748e-14, 2.97632159e-14,
#        1.68628170e-14, 9.28518734e-15, 5.02656617e-15, 2.68205554e-15,
#        1.40944076e-15, 7.28790677e-16, 3.66134210e-16, 1.56023871e-16,
#        6.25296102e-17, 2.69607279e-17, 1.28058729e-17, 6.74307305e-18,
#        3.88035742e-18, 2.39375329e-18, 1.54787355e-18, 1.03039830e-18,
#        6.97347322e-19, 4.75965483e-19, 3.26211808e-19, 2.23834252e-19,
#        1.52860950e-19, 1.06263211e-19, 7.52370070e-20, 5.31499430e-20,
#        3.73032516e-20, 2.57631966e-20, 1.54017609e-20])
# piHeII = uvb_rates_photoheating.create_dataset( 'piHeII', data=piHeII_data)
# 
# file.close()
