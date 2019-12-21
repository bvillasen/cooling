import sys
import numpy as np
import h5py as h5
import matplotlib.pyplot as plt


def load_hm12_spectrum( file_name ):
  file = open( file_name, 'r')
  lines = file.readlines()

  lines_all = []
  for line in lines:
    if line[0] == '#': continue
    if line[0] == '\n': continue
    if line[-1] == '\n': line = line[:-1]
    lines_all.append(line)
    
  z = np.array( lines_all[0].split(), dtype=np.float )
  n_redshift = len(z)
  print 'N Redshift: ', n_redshift

  data = []
  for line in lines_all[1:]:
    row = np.array( line.split(), dtype=np.float)
    data.append(row)
  data = np.array(data)

  J_lambda = data[:,0]
  J = data[:,1:]
  return z, J_lambda, J
  
def load_hm12_rates( file_name ):
  # Load the HM2012 data extracted from the paper
  table_hm12 = np.loadtxt( file_name ).T
  data_hm12 = {
  'Info': np.array('Haardt & Madau (2012, ApJ, 746, 125) [Galaxies & Quasars] Cloudy', dtype='|S64'),
  'redshift': table_hm12[0],
  'photoionization':{
    'HI': table_hm12[1],
    'HeI': table_hm12[3],
    'HeII': table_hm12[5],
    },
  'photoheating':{
    'HI': table_hm12[2],
    'HeI': table_hm12[4],
    'HeII': table_hm12[6],
    },
  }
  return data_hm12
