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
from load_grackle_output import *

#Load Gracke Data
file_name = 'data/CloudyData_UVB=HM2012.h5'
data_gk = load_grackle_dataset( file_name )


types = ['Primordial', 'Metals']

#Set the output file
file_name_out = 'data/my_grackle_files/CloudyData_UVB=HM2012_bruno.h5'
file_out = h5.File( file_name_out, 'w' )

# Add Cooling Rate
root_name = 'CoolingRates'
print root_name
group_root = file_out.create_group( root_name )
for type in types:
  print ' ' + type
  group_gk = data_gk[root_name][type]
  group_out = group_root.create_group(type)
  keys = group_gk.keys()
  for key in keys:
    print '  ' + key
    data_set_gk = group_gk[key]
    table_gk = data_set_gk['data']
    data_set = group_out.create_dataset( key, data=table_gk )
    attrs = data_set_gk.keys()
    for attr_key in attrs:
      if attr_key == 'data': continue
      print attr_key
      data_set.attrs[attr_key] = data_set_gk[attr_key]

# Add UVBRates

root_name = 'UVBRates'
print root_name
group_out = file_out.create_group( root_name )
for key in ['z', 'Info']:
  print ' ' + key
  data = data_gk[root_name][key][...]
  if key == 'Info': data = np.array('Haardt & Madau (2012, ApJ, 746, 125) [Galaxies & Quasars]  Test by Bruno',  dtype='|S72')
  group_out.create_dataset( key, data=data )
  
for key in ['Chemistry', 'Photoheating']:
  print ' ' + key
  group_gk = data_gk[root_name][key]
  group_out = file_out[root_name].create_group( key )
  for field in group_gk.keys():
    if field not in ['k24', 'k25', 'k26', 'piHI', 'piHeI', 'piHeII']: continue
    print field
    data = group_gk[field][...]
    group_out.create_dataset( field, data=data )


file_out.close()