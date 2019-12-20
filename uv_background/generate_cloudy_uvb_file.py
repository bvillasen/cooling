import sys
import numpy as np
import h5py as h5
import matplotlib.pyplot as plt


# Line 1: contains 60 fields identifying the sampling redshifts, from 0 to 15.93.
# Lines 2 through 576: the first field is the rest-frame wavelength in Angstroms, fields 2 through 61 give the background intensity
# J (in units of ergs/s/cm^2/Hz/sr) at the 60 sampling redshifts.  

fileName = 'data/uvb_HM12.dat'
file = open( fileName, 'r')
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

fileName = 'data/hm12_galaxy.ascii'
file = open( fileName, 'r')
lines = file.readlines()
n_header = 10
n_redshift_cl = 60
n_lambda_cl = 575
counter = 0
z_cl = []
lambda_cl = []
J_cl = [] 
J_for_redshift = []
loading_header = True
loading_redshift = False
loading_lambda = False
loading_sprectrum = False 
for i, line in enumerate(lines):
  if line[0] == '#': continue
  line = line.split()
  # if len(line) == 1: continue
  
  
  if loading_header and counter == n_header: 
    loading_header = False
    loading_redshift = True
    counter = 0 
    
  if loading_redshift and counter == n_redshift: 
    loading_redshift = False
    loading_lambda = True
    counter = 0 
  
  if loading_lambda and counter == n_lambda_cl: 
    loading_lambda = False
    loading_sprectrum = True
    counter = 0 
    
  if loading_sprectrum and counter == n_lambda_cl: 
    J_cl.append( J_for_redshift )
    J_for_redshift = []
    counter = 0 
    
  
  # if loading_sprectrum and counter == n_lambda_cl  
  
  if loading_redshift:  z_cl.extend( line )
  if loading_lambda:  lambda_cl.extend( line )
  if loading_sprectrum: J_for_redshift.extend(line)
  
    
    
  # if loading_redshift: print line
  counter +=  len(line)
J_cl.append( J_for_redshift )
z_cl = np.array(  z_cl, dtype=np.float )
lambda_cl = np.array(  lambda_cl, dtype=np.float )
J_cl = np.array( J_cl, dtype=np.float )    
    
    # if counter < n_redshift_cl + n_header : 
    #   z_cl.append(np.float(value)) 
    #   counter += 1

n_rows = 1      
n_cols =  2
fig, ax_list = plt.subplots(nrows=n_rows, ncols=n_cols, figsize=(10*n_cols,9.2*n_rows))
plt.subplots_adjust(  wspace=0.3, hspace=0.3)


for i in range(n_redshift):

  ax = ax_list[0] 
  ax.plot( J_lambda, J[:,i] )

  ax = ax_list[1] 
  ax.plot( lambda_cl, J_cl[i] )


fig.savefig( 'ubv_HM12.png',  bbox_inches='tight', dpi=100 )
