import sys
import numpy as np
import h5py as h5
import matplotlib.pyplot as plt


def load_puchwein_spectrum( file_name ):
  file = open( file_name, 'r' )
  lines = file.readlines() 
  data = []
  counter = 0
  for line in lines:
    line = line.split()
    if line[0] == '#': continue
    if counter == 0:
      #Load the redshift data
      redshift_data = np.array( line, dtype=np.float )
    if counter > 0:
      #Load the spectrum
      data.append( np.array( line, dtype=np.float ) )
    counter += 1
  
  data = np.array( data )  
  lambda_data = data[:,0]
  J_data = data[:,1:]
  # print len(redshift_data)
  # print len(lambda_data)
  return redshift_data, lambda_data, J_data
  
def load_puchwein_rates( file_name ):
  # Load the HM2012 data extracted from the paper
  table= np.loadtxt( file_name ).T
  data = {
  'redshift': table[0],
  'photoionization':{
    'HI': table[1],
    'HeI': table[3],
    'HeII': table[5],
    },
  'photoheating':{
    'HI': table[2],
    'HeI': table[4],
    'HeII': table[6],
    },
  }
  return data

