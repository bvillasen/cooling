import sys, os, time, shutil
from subprocess import call
import numpy as np
from mpi4py import MPI
from subprocess import Popen


cool_dir = os.path.dirname(os.getcwd()) + '/'
cloudy_dir = cool_dir + 'cloudy/'
uvb_dir = cool_dir + 'uv_background/'
tools_dir = cool_dir + 'tools/'
sys.path.extend([ uvb_dir, tools_dir ] )
from tools import create_directory, write_parameter_file
from cloudy_tools import *


comm = MPI.COMM_WORLD
rank = comm.Get_rank()
nprocs = comm.Get_size()


print_out = False

# type = 'primordial'
type = 'metals'

uvb_name = 'HM12'
# uvb_name = 'Puchwein18'


if rank == 0:
  print "Type: {0}".format( type )
  print "UVB: {0}".format( uvb_name)
comm.Barrier()
time.sleep(2)

if type == 'primordial': composition_parameters = composition_metals_off
if type == 'metals': composition_parameters = [ 'no molecules' ]


# work_directory = '/home/bruno/Desktop/Dropbox/Developer/cooling_tools/cloudy_tools/data/uv_{0}_{1}/'.format(uvb_name, type )
work_directory = '/data/groups/comp-astro/bruno/cooling_tools/cloudy_tools/data/uv_{0}_{1}_lux/'.format(uvb_name, type )
if rank == 0: print "Work Directory: ", work_directory
if rank == 0: create_directory(work_directory, print_out=print_out)
# os.chdir( work_directory )
output_dir = work_directory 
if rank == 0: create_directory(output_dir, print_out=print_out)
comm.Barrier()
time.sleep(2)

# cloudy_command = cloudy_dir + 'source/cloudy.exe_shamrock'
# cloudy_command = cloudy_dir + 'source/cloudy.exe_shamrock_puchwein'
cloudy_command = cloudy_dir + 'source/cloudy.exe_lux'

  
  
run_temp_vals = np.logspace( 1, 9, 161 )

run_base_name = 'cooling_run'
run_hden_vals = np.linspace(-10, 4, 29)
# run_redshift_vals = np.array([  0. ])
run_redshift_vals = np.array([  0.,  0.12202,  0.25893,  0.41254,  0.58489,  0.77828,  0.99526,
  1.2387,   1.5119,   1.8184,  2.1623,   2.5481,  2.9811,   3.4668,   4.0119,   4.6234,   5.3096,
  6.0795,    6.9433,   7.9125,   9.,      10.22,    11.589,   13.125,    14.849,   14.8491, ])
  
def get_run_values( run_hden_vals, run_redshift_vals ):  
  n_run = 0
  run_values = {}  
  for redshift_val in run_redshift_vals:
    for hden_val in run_hden_vals:
      run_values[n_run] = {}
      run_values[n_run]['hden'] = hden_val
      run_values[n_run]['redshift'] = redshift_val
      n_run += 1
  return n_run, run_values
  
n_runs, run_vals = get_run_values( run_hden_vals, run_redshift_vals )

if rank == 0:
  print "N dens: {0}".format( len(run_hden_vals) )
  print "N redshift: {0}".format( len(run_redshift_vals) )
  print "N temperature: {0}".format( len(run_temp_vals) )
  print "N runs: {0}".format(n_runs)
comm.Barrier()
time.sleep(2)


n_proc_runs = (n_runs-1)/nprocs + 1

proc_runs = np.array([ rank + i*nprocs for i in range(n_proc_runs) ])
proc_runs = proc_runs[ proc_runs < n_runs ]

if len(proc_runs) == 0: exit()

print "pID: {0}:  {1}".format( rank, proc_runs)
comm.Barrier()
time.sleep(2)


if rank == 0:
  data_out = []
  h = 'hden {0}\n'.format( len(run_hden_vals))
  h += 'redshift {0}\n'.format( len(run_redshift_vals))
  h += 'n_run hden redshift'
  for n_run in range(n_runs):
    data_out.append([ n_run, run_vals[n_run]['hden'], run_vals[n_run]['redshift'] ])
  data_out = np.array( data_out ) 
  out_file_name = output_dir + 'run_values.dat'
  np.savetxt( out_file_name, data_out, header=h, fmt='%d %0.3f  %0.5f' )


for n_run in proc_runs:

  redshift_last = False
  hden = run_vals[n_run]['hden']
  hden_to_cloudy = hden
  
  redshift = run_vals[n_run]['redshift']
  if redshift == run_redshift_vals[-1]: redshift_last = True
  
  if redshift_last: hden_to_cloudy = 5.0 #Set Large Density for Primordial cooling only
  
  # if not redshift_last: continue
  # print n_run
  
  run_cooling_rates = []
  run_heating_rates = []
  run_mmw = []

  print 'Satarting Run : ', n_run
  
  run_directory = output_dir + 'run_{0}/'.format( n_run )
  create_directory( run_directory, print_out=print_out )  
  
  # Check if the run_file already exixts
  run_file = run_directory + 'output.dat'
  if os.path.exists( run_file ): 
    print " Run exists"
    continue
    
  #Change directory to output_dir
  os.chdir( run_directory )
  run_directory = ''
    
  #Copy Cloudy executable to run localy
  cloudy_command_local = 'cloudy.exe'
  # shutil.copyfile( cloudy_command, cloudy_command_local )
  p = Popen(['cp','-p','--preserve',  cloudy_command, cloudy_command_local])
  p.wait()

  
  # exit()
  for T in run_temp_vals:
    if print_out: print ' T = {0:.3e}'.format( T )

    run_parameters = [
    'stop zone 1',
    'iterate to convergence',
    'hden {0}'.format(hden_to_cloudy),
    'constant temperature T = {0:.6e} linear'.format(T),
    ]
    
    # if uvb_name == 'HM12':
    uvb_parameters = [
    'table HM12 redshift {0}'.format(redshift)
    ]
    # 
    # if uvb_name == 'Puchwein18':
    #   uvb_parameters = [
    #   'table Puchwein18 redshift {0}'.format(redshift)
    #   ]
    # 
    
    if redshift_last: uvb_parameters = []
    
    output_parameters = [
    'punch last cooling file = "{0}{1}_run{2}.cooling.temp"'.format(run_directory, run_base_name, n_run),
    'punch last heating file = "{0}{1}_run{2}.heating.temp"'.format(run_directory, run_base_name, n_run),
    'punch last abundance file = "{0}{1}_run{2}.abundance.temp"'.format(run_directory, run_base_name, n_run),
    'punch last ionization means file = "{0}{1}_run{2}.ionization.temp"'.format(run_directory, run_base_name, n_run),
    'punch last physical conditions file = "{0}{1}_run{2}.physical.temp"'.format(run_directory, run_base_name, n_run)
    ]
    
    run_parameters.extend( uvb_parameters )
    run_parameters.extend( composition_parameters  )
    run_parameters.extend( output_parameters  )
    simulation_parameters = run_parameters

    # Write the Cloudy parameter file
    parameter_file =  run_directory + 'params.txt'
    write_parameter_file( simulation_parameters,  parameter_file )

    if print_out: print ' Saved Parameter File: ', parameter_file 

    #Set Cloudy output file
    output_file =  run_directory + 'output.txt'

    start = time.time()
    command = '{0} <{1}> {2}'.format( cloudy_command, parameter_file, output_file) 
    if print_out: print "Running Cloudy:   {0}".format( command )
    call( command , shell=True)
    if print_out: print "Time: ", time.time() - start

    cooling_file = run_directory + '{0}_run{1}.cooling.temp'.format(run_base_name, n_run)
    data_cooling = Load_Cooling_File( cooling_file , print_out=print_out )

    temp = data_cooling['Temp K']
    if np.abs(T-temp)/T > 1e-4:
      print 'ERROR: Temperatures are different: {0}  {1}'.format(temp, T) 
    cooling_rate = data_cooling['Ctot erg/cm3/s']
    heating_rate = data_cooling['Htot erg/cm3/s']

    cooling_factor = (10**hden_to_cloudy)**2
    cooling_rate /= cooling_factor
    heating_rate /= cooling_factor
    
    if redshift_last: heating_rate = 0 #set the heating rate to zero if no uvb

    run_cooling_rates.append( cooling_rate )
    run_heating_rates.append( heating_rate )

    ionization_file = run_directory + '{0}_run{1}.ionization.temp'.format(run_base_name, n_run)
    ionization_frac = Load_Ionization_File( ionization_file, print_out=print_out )
    n_H = 1.0
    n_He = 0.1*n_H
    mu = Get_Mean_Molecular_Weight( n_H, n_He, ionization_frac, print_out=print_out )
    run_mmw.append(mu)
    
    #delete temporal files
    command = 'rm {0}*.temp {0}output.txt {0}params.txt '.format( run_directory ) 
    call( command , shell=True)
    
  
  # Delete Cloudy command
  command = 'rm {0} '.format( cloudy_command_local ) 
  call( command , shell=True)

  # Write the run data
  data_header = ' hden {0:.3} \n'.format( hden )
  data_header += ' redshift {0:.5} \n'.format( redshift )
  data_header += ' Temp Cooling_Rate Heating_Rate MMW'
  data = np.array([ run_temp_vals, np.array(run_cooling_rates), np.array(run_heating_rates) , np.array(run_mmw) ] ).T
  np.savetxt( run_file, data, header=data_header )
  print ' Saved run data: ', run_file



