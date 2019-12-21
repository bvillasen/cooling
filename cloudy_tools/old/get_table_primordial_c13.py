import sys, os, time
from subprocess import call
import numpy as np
from tools import create_directory, write_parameter_file
from cloudy_tools import *



composition_parameters = composition_metals_off


work_directory = '/home/bruno/Desktop/Dropbox/Developer/cooling_tools/cloudy_tools/primordial/'
print "Work Directory: ", work_directory
# os.chdir( work_directory )

temp_dir = work_directory + 'temporal_c13/'
create_directory(temp_dir)


cloudy_command = './cloudy_13.exe'
# cloudy_command = './cloudy.exe_shamrock'

cloudy_command_base = '/home/bruno/Desktop/Dropbox/Developer/cooling_tools/cloudy_tools/cloudy_13.exe'



run_base_name = 'cooling_run'
run_hden_vals = np.array([ 1e5 ])

run_temp_vals = np.logspace( 3.8, 9, 120 )


for n_run, hden in enumerate( run_hden_vals ):
  
  
  run_cooling_rates = []
  run_heating_rates = []
  run_mmw = []
  
  print 'Run : ', n_run
  # 
  for T in run_temp_vals:
    print ' T = {0:.3e}'.format( T )
  
    output_directory = temp_dir + 'run_{0}/'.format( n_run )
    create_directory( output_directory )  
    os.chdir( output_directory )
    
    
    #Copy cloudy executable
    command = 'cp {0} cloudy_13.exe'.format(cloudy_command_base)
    call( command, shell=True)
  # 
    run_parameters = [
    'stop zone 1',
    'hden 5',
    'iterate to convergence',
    # 'constant temperature T = {0:.6e} linear'.format(T),
    'coronal equilibrium T = {0:.6e} linear'.format(T),
    ]
  
    output_parameters = [
    'punch last cooling file = "{0}/{1}_run{2}.cooling.temp"'.format(output_directory, run_base_name, n_run),
    'punch last heating file = "{0}/{1}_run{2}.heating.temp"'.format(output_directory, run_base_name, n_run),
    'punch last abundance file = "{0}/{1}_run{2}.abundance.temp"'.format(output_directory, run_base_name, n_run),
    'punch last ionization means file = "{0}/{1}_run{2}.ionization.temp"'.format(output_directory, run_base_name, n_run),
    'punch last physical conditions file = "{0}/{1}_run{2}.physical.temp"'.format(output_directory, run_base_name, n_run)
    ]
  
  
  
    run_parameters.extend( composition_parameters  )
    run_parameters.extend( output_parameters  )
    simulation_parameters = run_parameters
  
  
    # Write the Cloudy parameter file
    parameter_file =  output_directory + 'params.txt'
    write_parameter_file( simulation_parameters,  parameter_file )
  
    print ' Saved Parameter File: ', parameter_file 
  
    #Set Cloudy output file
    output_file =  output_directory + 'output.txt'
  
  
    start = time.time()
    command = '{0} <{1}> {2}'.format( cloudy_command, parameter_file, output_file) 
    print "Running Cloudy:   {0}".format( command )
    call( command , shell=True)
    # call(['ls'])  
    print "Time: ", time.time() - start
  
    cooling_file = output_directory + '{0}_run{1}.cooling.temp'.format(run_base_name, n_run)
    data_cooling = Load_Cooling_File( cooling_file )
  
    temp = data_cooling['Temp K']
    if np.abs(T-temp)/T > 1e-4:
      print 'ERROR: Temperatures are different: {0}  {1}'.format(temp, T) 
    cooling_rate = data_cooling['Ctot erg/cm3/s']
    heating_rate = data_cooling['Htot erg/cm3/s']
  
    cooling_factor = hden**2
    cooling_rate /= cooling_factor
    heating_rate /= cooling_factor
  
    run_cooling_rates.append( cooling_rate )
    run_heating_rates.append( heating_rate )
  
    ionization_file = output_directory + '{0}_run{1}.ionization.temp'.format(run_base_name, n_run)
    ionization_frac = Load_Ionization_File( ionization_file )
    n_H = 1.0
    n_He = 0.1*n_H
    mu = Get_Mean_Molecular_Weight( n_H, n_He, ionization_frac )
    # print mu
    run_mmw.append(mu)
  
  
      
  data_header = ' hden {0:.7e} \n'.format( hden )
  data_header += ' Temp Cooling_Rate Heating_Rate MMW'
  data = np.array([ run_temp_vals, np.array(run_cooling_rates), np.array(run_heating_rates) , np.array(run_mmw) ] ).T
  np.savetxt( output_directory + 'output.dat', data, header=data_header )
  print '\nSaved run data: ', output_directory + 'output.dat'
    # print line



