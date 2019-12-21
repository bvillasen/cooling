import os, sys
from os import listdir
from os.path import isfile, join
import numpy as np
import time
import h5py as h5

def load_grackle_rates( fileName ):
  file_gk = h5.File( fileName, 'r' )

  # Redshift
  z = file_gk['UVBRates']['z'][...] 
  
  info = file_gk['UVBRates']['Info'][...]
  
  # Photoionization Reactions
  # k24:   HI    + p   -> HII   + e
  # k25:   HeII  + p   -> HeIII + e
  # k26:   HeI   + p   -> HeII  + e
  ion_rate_HI = file_gk['UVBRates']['Chemistry']['k24'][...] 
  ion_rate_HeI = file_gk['UVBRates']['Chemistry']['k26'][...] 
  ion_rate_HeII = file_gk['UVBRates']['Chemistry']['k25'][...]


  heat_rate_HI = file_gk['UVBRates']['Photoheating']['piHI'][...]
  heat_rate_HeI = file_gk['UVBRates']['Photoheating']['piHeI'][...]
  heat_rate_HeII = file_gk['UVBRates']['Photoheating']['piHeII'][...]

  rates = {}
  rates['Info'] = info
  rates['redshift'] = z
  rates['photoheating'] = {}
  rates['photoheating']['HI'] = heat_rate_HI
  rates['photoheating']['HeI'] = heat_rate_HeI
  rates['photoheating']['HeII'] = heat_rate_HeII

  rates['photoionization'] = {}
  rates['photoionization']['HI'] = ion_rate_HI
  rates['photoionization']['HeI'] = ion_rate_HeI
  rates['photoionization']['HeII'] = ion_rate_HeII
  return rates


def get_grackle_table_noUV( key, fileName, type='Primordial'):
  file = h5.File( fileName, 'r' )


  rates = file['CoolingRates']
  rates_primordial = rates[type]
   
  #Get values for temperature in the table
  temp_vals = rates_primordial['Cooling'].attrs['Temperature']

  #Get values for density in the table
  dens_vals = rates_primordial['Cooling'].attrs['Parameter1']

  keys_grackle = {'cooling_rate': 'Cooling', 'heating_rate': 'Heating', 'mean_molecular_weight': 'MMW'}
  key_grackle = keys_grackle[key]

  #Get table [ dens,  temperature ]
  table = rates_primordial[key_grackle][...]
  file.close()
  return dens_vals, temp_vals, table


def get_grackle_table( key, fileName, type='Primordial' ):
  file = h5.File( fileName, 'r' )


  rates = file['CoolingRates']
  rates_primordial = rates[type]

  #Get values for temperature in the table
  temp_vals = rates_primordial['Cooling'].attrs['Temperature']

  #Get values for density in the table
  dens_vals = rates_primordial['Cooling'].attrs['Parameter1']

  #Get values for redshift in the table
  redshift_vals = rates_primordial['Cooling'].attrs['Parameter2']


  keys_grackle = {'cooling_rate': 'Cooling', 'heating_rate': 'Heating', 'mean_molecular_weight': 'MMW'}
  key_grackle = keys_grackle[key]

  #Get table [ dens, redshift, temperature ]
  table = rates_primordial[key_grackle][...]
  file.close()
  return dens_vals, redshift_vals, temp_vals, table


def load_grackle_dataset( file_name ):
  file =   file = h5.File( file_name, 'r' )
  data = {}

  rates = load_grackle_rates( file_name )
  data['UVBRates'] = {}
  data['UVBRates']['Info'] = rates['Info']
  data['UVBRates']['z'] = rates['redshift']
  data['UVBRates']['Photoheating'] = {}
  data['UVBRates']['Photoheating']['piHI'] = rates['photoheating']['HI']
  data['UVBRates']['Photoheating']['piHeI'] = rates['photoheating']['HeI']
  data['UVBRates']['Photoheating']['piHeII'] = rates['photoheating']['HeII']
  data['UVBRates']['Chemistry'] = {}
  data['UVBRates']['Chemistry']['k24'] = rates['photoionization']['HI'] 
  data['UVBRates']['Chemistry']['k25'] = rates['photoionization']['HeII']
  data['UVBRates']['Chemistry']['k26'] = rates['photoionization']['HeI'] 

  keys_grackle = {'cooling_rate': 'Cooling', 'heating_rate': 'Heating', 'mean_molecular_weight': 'MMW'}

  data['CoolingRates'] = {}
  for type in [ 'Primordial', 'Metals' ]:
    data['CoolingRates'][type] = {}
    keys = [ 'cooling_rate', 'heating_rate', 'mean_molecular_weight']
    if type == 'Metals': keys = [ 'cooling_rate', 'heating_rate' ]
    for key in keys:
      dens_vals, redshift_vals, temp_vals, table = get_grackle_table( key, file_name, type )
      n_dens, n_redshift, n_temp = len(dens_vals), len(redshift_vals), len(temp_vals),
      key_grackle = keys_grackle[key]
      data['CoolingRates'][type][key_grackle] = {} 
      data['CoolingRates'][type][key_grackle]['data'] = table
      data['CoolingRates'][type][key_grackle]['Rank'] = 3
      data['CoolingRates'][type][key_grackle]['Dimension'] = np.array([n_dens, n_redshift, n_temp])
      data['CoolingRates'][type][key_grackle]['Parameter1'] = dens_vals
      data['CoolingRates'][type][key_grackle]['Parameter1_Name'] = 'hden'
      data['CoolingRates'][type][key_grackle]['Parameter2'] = redshift_vals
      data['CoolingRates'][type][key_grackle]['Parameter2_Name'] = 'redshift'
      data['CoolingRates'][type][key_grackle]['Temperature'] = temp_vals
    
  return data


