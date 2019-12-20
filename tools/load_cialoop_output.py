import os, sys
from os import listdir
from os.path import isfile, join
import numpy as np
import time
import h5py as h5


def get_cialoop_table_noUV( run_values, key, name_base, inDir ):
  dens_vals = []
  temp_vals = []
  for n_run in run_values.keys():
    dens_vals.append( run_values[n_run]['density'])
    data_dic = load_cialoop_data( n_run, name_base, inDir )
    temp_vals = data_dic['data']['temperature']
  dens_vals = np.array(dens_vals)
  temp_vals = np.array(temp_vals)
  n_dens, n_temp = len(dens_vals), len(temp_vals)
  table  = np.zeros([n_dens, n_temp])

  for n_run in run_values.keys():
    dens = run_values[n_run]['density']
    indx_dens = np.where(dens_vals == dens)[0]
    # print n_run, indx_dens
    data_dic = load_cialoop_data( n_run, name_base, inDir )
    table[indx_dens, :] = data_dic['data'][key]
  return dens_vals, temp_vals, table
  

def get_cialoop_table( run_values, key, name_base, inDir,  ):

  dens_vals, redshift_vals = get_run_density_redshift( run_values, )

  n_dens, n_redshift = len(dens_vals), len(redshift_vals)
  n_temp = 161
  table = np.zeros([ n_dens, n_redshift, n_temp ])

  for n_run in run_values.keys():
    data_run = get_run_data( n_run, run_values, name_base, inDir )
    dens = data_run['density']
    redshift = data_run['redshift']
    indx_dens = np.where( dens_vals == dens )[0]
    indx_redshift = np.where( redshift_vals == redshift )[0]
    if len(indx_dens) > 1: print "Error: density index"
    if len(indx_redshift) > 1: print "Error: redshift index"

    temp_cialoop = data_run['temperature']
    data_to_table = data_run[key]
    table[indx_dens, indx_redshift, :] = data_to_table
  temp_vals = temp_cialoop
  return dens_vals, redshift_vals, temp_vals, table



def get_run_density_redshift( run_values, z=True ):
  dens_vals = []
  redshift_vals = []
  for key in run_values.keys():
    dens_vals.append( run_values[key]['density'] )
    redshift_vals.append( run_values[key]['redshift'] )
  dens_vals = np.array( list(set( dens_vals )) )
  dens_vals.sort()
  redshift_vals = np.array( list(set( redshift_vals )) )
  redshift_vals.sort()
  return dens_vals, redshift_vals


def get_run_data( n_run, run_values, name_base, inDir):
  data = {}
  data_run = load_cialoop_data( n_run, name_base, inDir )
  dens = run_values[n_run]['density']
  redshift = run_values[n_run]['redshift']
  temperature = data_run['data']['temperature']
  cooling_rate = data_run['data']['cooling_rate']
  heating_rate = data_run['data']['heating_rate']
  mmw = data_run['data']['mean_molecular_weight']
  data['density'] = dens
  data['redshift'] = redshift
  data['temperature'] = temperature
  data['cooling_rate'] = cooling_rate
  data['heating_rate'] = heating_rate
  data['mean_molecular_weight'] = mmw
  return data

def get_run_values_cialoop( inDir, name_base, z=True ):
  fileName = inDir + name_base + '.run'
  file = open( fileName, 'r')
  lines = file.readlines()
  header_all = []
  data_all = []
  run_values = {}
  for line in lines:
    if line[0] == '#':
      header_all.append(line[1:-1])
    else:
      if z: 
        n_run, dens, redshift = line.split()
        n_run = np.int( n_run )
        dens = np.float( dens )
        redshift = np.float(redshift.split(',')[0])
        # print n_run, dens, redshift
        run_values[n_run] = { 'density':dens, 'redshift':redshift }
      else:
        n_run, dens = line.split()
        n_run = np.int( n_run )
        dens = np.float( dens )
        # print n_run, dens, redshift
        run_values[n_run] = { 'density':dens, }
  return run_values

def get_cialoop_data_file_names( name_base, inDir ):
  dataFiles = [f for f in listdir(inDir) if (isfile( join(inDir, f)) and (f.find(name_base) == 0 ) and (f.find('.dat') > 0 )  ) ]
  dataFiles = np.sort( dataFiles )
  nFiles = len( dataFiles )
  return nFiles, dataFiles


def load_cialoop_data( n_file, name_base, inDir ):
  file_name = '{0}_run{1}.dat'.format( name_base, n_file )
  file = open( inDir + file_name, 'r' )
  lines = file.readlines()
  header = []
  header_loop = []
  data = []
  loading_lines = False
  for line in lines:
    if line[0] == '#':  
      header.append(line[1:-1])
      if line.find('\n') == 1 : loading_lines = False
      if loading_lines: header_loop.append( line[2:-1] )
      if line.find('Loop values') > 0 : loading_lines = True
    else:
      data_line = np.array( line.split() ).astype(np.float)
      data.append(data_line)
  file.close()

  data = np.array(data).T
  temp = data[0]
  rate_heating = data[1]
  rate_cooling = data[2]
  mean_molecular_weight = data[3]
  # print temp

  data_dic = {
   'header': header,
   'header_loop': header_loop,
   'data': {
    'temperature': temp,
    'heating_rate': rate_heating,
    'cooling_rate': rate_cooling,
    'mean_molecular_weight': mean_molecular_weight
   }
  }
  return data_dic