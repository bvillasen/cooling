import os, sys
from os import listdir
from os.path import isfile, join
import numpy as np
import time
import h5py as h5





def get_run_values( inDir, file_name='run_values.dat' ):
  
  file = open( inDir + file_name, 'r' )
  lines = file.readlines()
  # n_dens 
  for i in range(2):
    line = lines[i].split()
    if i==0: n_dens = np.int(line[2])
    if i==1: n_redshift = np.int(line[2]) 
    # print line
  file.close()
  data = np.loadtxt( inDir + file_name ).T
  n_run_vals = data[0].astype(np.int)
  hden_vals = data[1]
  redshift_vals = data[2]
  run_vals = {}
  # print data
  for n_run in n_run_vals:
    run_vals[n_run] = {}
    run_vals[n_run]['density'] = hden_vals[n_run]
    run_vals[n_run]['redshift'] = redshift_vals[n_run]
  # hden_vals = np.array(list(set(list(hden_vals)) ))
  hden_vals = hden_vals[:n_dens]
  if len(hden_vals) != n_dens: print "ERROR: Loading density values"
  redshift_vals = redshift_vals[::n_dens]
  # print "N density: ", n_dens
  # print "N redshift: ", n_redshift
  return run_vals, hden_vals, redshift_vals






def Load_Run_Data( n_run, work_directory, run_vals ):
  run_dens = run_vals[n_run]['density']
  run_redshift = run_vals[n_run]['redshift']

  inDir = work_directory + 'run_{0}/'.format(n_run)
  file_name = inDir + 'output.dat'
  file = open(  file_name, 'r' )
  lines = file.readlines()
  # n_dens 
  for i in range(2):
    line = lines[i].split()
    if i==0: file_dens = np.float(line[2])
    if i==1: file_redshift = np.float(line[2])
  file.close()
  if file_dens != run_dens: print 'ERROR: density mismatch: {0}   {1}'.format(file_dens, run_dens)  
  if file_redshift != run_redshift: print 'ERROR: redshift mismatch: {0}   {1}'.format(file_redshift, run_redshift)  
  data = np.loadtxt( file_name ).T
  temp = data[0]
  cooling_rate = data[1]
  heating_rate = data[2]
  mmw = data[3]
  data_run = {}
  data_run['density'] = run_dens
  data_run['redshift'] = run_redshift
  data_run['temperature'] = temp
  data_run['cooling_rate'] = cooling_rate
  data_run['heating_rate'] = heating_rate
  data_run['mean_molecular_weight'] = mmw
  return data_run



def get_cloudy_table(  key,  work_directory,  ):

  run_vals, dens_vals, redshift_vals = get_run_values( work_directory, file_name='run_values.dat' )

  n_dens, n_redshift = len(dens_vals), len(redshift_vals)
  n_temp = 161
  table = np.zeros([ n_dens, n_redshift, n_temp ])

  for n_run in run_vals.keys():
    data_run = Load_Run_Data( n_run, work_directory, run_vals )
    dens = data_run['density']
    redshift = data_run['redshift']
    indx_dens = np.where( dens_vals == dens )[0]
    indx_redshift = np.where( redshift_vals == redshift )[0]
    if len(indx_dens) > 1: print "Error: density index ", indx_dens
    # if len(indx_redshift) > 1: print "Error: redshift index ", indx_redshift

    temp_cloudy = data_run['temperature']
    data_to_table = data_run[key]
    table[indx_dens, indx_redshift, :] = data_to_table
  temp_vals = temp_cloudy
  return dens_vals, redshift_vals, temp_vals, table





def load_cloudy_CoolingRates( indir_primordial, indir_metals, ):
  keys_grackle = {'cooling_rate': 'Cooling', 'heating_rate': 'Heating', 'mean_molecular_weight': 'MMW'}

  data = {}
  data['CoolingRates'] = {}

  type = 'Primordial'
  run_vals = get_run_values( indir_primordial )
  # print type
  data['CoolingRates'][type] = {}
  keys = [ 'cooling_rate', 'heating_rate', 'mean_molecular_weight']
  for key in keys:
    dens_vals, redshift_vals, temp_vals, table = get_cloudy_table( key,  indir_primordial  ) 
    n_dens, n_redshift, n_temp = len(dens_vals), len(redshift_vals), len(temp_vals),
    key_grackle = keys_grackle[key]
    # print ' ', key_grackle
    data['CoolingRates'][type][key_grackle] = {} 
    data['CoolingRates'][type][key_grackle]['data'] = table
    data['CoolingRates'][type][key_grackle]['Rank'] = 3
    data['CoolingRates'][type][key_grackle]['Dimension'] = np.array([n_dens, n_redshift, n_temp])
    data['CoolingRates'][type][key_grackle]['Parameter1'] = dens_vals
    data['CoolingRates'][type][key_grackle]['Parameter1_Name'] = 'hden'
    data['CoolingRates'][type][key_grackle]['Parameter2'] = redshift_vals
    data['CoolingRates'][type][key_grackle]['Parameter2_Name'] = 'redshift'
    data['CoolingRates'][type][key_grackle]['Temperature'] = temp_vals

  type = 'Metals'
  run_vals = get_run_values( indir_metals )
  # print type
  data['CoolingRates'][type] = {}
  keys = [ 'cooling_rate', 'heating_rate' ]
  for key in keys:
    dens_vals, redshift_vals, temp_vals, table = get_cloudy_table( key,  indir_metals  ) 
    n_dens, n_redshift, n_temp = len(dens_vals), len(redshift_vals), len(temp_vals),
    key_grackle = keys_grackle[key]
    # print ' ', key_grackle
    data['CoolingRates'][type][key_grackle] = {} 
    data['CoolingRates'][type][key_grackle]['data'] = table
    data['CoolingRates'][type][key_grackle]['Rank'] = 3
    data['CoolingRates'][type][key_grackle]['Dimension'] = np.array([n_dens, n_redshift, n_temp])
    data['CoolingRates'][type][key_grackle]['Parameter1'] = dens_vals
    data['CoolingRates'][type][key_grackle]['Parameter1_Name'] = 'hden'
    data['CoolingRates'][type][key_grackle]['Parameter2'] = redshift_vals
    data['CoolingRates'][type][key_grackle]['Parameter2_Name'] = 'redshift'
    data['CoolingRates'][type][key_grackle]['Temperature'] = temp_vals

  #Substract Primordial Coolinf from Metal Cooling

  keys = [ 'cooling_rate', 'heating_rate' ]
  for key in keys:
    key_grackle = keys_grackle[key]
    data_primordial = data['CoolingRates']['Primordial'][key_grackle]['data']
    data_metals = data['CoolingRates']['Metals'][key_grackle]['data']
    data_diff = data_metals - data_primordial
    print data_diff.min(),  data_diff.max()
    data_diff[data_diff<0] = 1e-30
    data['CoolingRates']['Metals'][key_grackle]['data'] = data_diff

  return data


def Add_UVBRates( data, rates ):
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
    return data

