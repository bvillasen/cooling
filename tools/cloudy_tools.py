import os, sys
from os import listdir
from os.path import isfile, join
import numpy as np


def Load_Cooling_File( cooling_file, print_out=True ):
  if print_out: print ' Loading Cooling/Heating Rates'
  data = {}
  file = open( cooling_file, 'r' )
  lines = file.readlines()
  for line in lines:
    if line[0] == '#':
      line = line.split('\t')[:-1]
      header = line
    else:
      line = line.split('\t')
      for i,name in enumerate(header):
        if name[0] == '#': name = name[1:]
        data[name] = np.float(line[i]) 
  return data
  

def parse_line( line ):
  data_line = []
  for element in line[1:]:
    if element == '(H2)': break
    # print element
    factor = 1
    if element[0] == '-':
      factor = -1
      element = element[1:]
    element = element.split('-')
    if len(element) == 3:
      # print element
      val_1 = np.float( element[0])
      val_2 = np.float( element[1])
      val_3 = np.float( element[2])
      data_line.append( factor * val_1 )
      data_line.append( -1 * val_2 )
      data_line.append( -1 * val_3 )
    if len(element) == 2:
      val_1 = np.float( element[0])
      val_2 = np.float( element[1])
      data_line.append( factor * val_1 )
      data_line.append( -1 * val_2 )
    if len(element) == 1:
      val_1 = np.float( element[0])
      data_line.append( factor * val_1 )
  # print data_line
  return data_line
  
  
def Load_Ionization_File( ionization_file, print_out=True ):  
  if print_out: print ' Loading Ionization Fractions'
  data = {}
  file = open( ionization_file, 'r' )
  lines = file.readlines()
  for line in lines:
    if line[0] == '#': continue
    line = line.split()
    if len(line) == 0: continue
    if line[0] == 'Hydrogen':
      if print_out: print line
      HI, HII, H2 = parse_line(line)
      data['HI'] = HI
      data['HII'] = HII
      if print_out: print data['HI'], data['HII']
    if line[0] == 'Helium':
      if print_out: print line
      data_He = parse_line(line)
      HeI = data_He[0]
      if len(data_He) > 1: HeII = data_He[1]
      else: HeII = -30.0
      if len(data_He) > 2: HeIII = data_He[2]
      else: HeIII = -30.0
      data['HeI'] = HeI
      data['HeII'] = HeII
      data['HeIII'] = HeIII
      if print_out: print data['HeI'], data['HeII'], data['HeIII']
  return data


def Get_Mean_Molecular_Weight( n_H, n_He, ionization_frac,  print_out=True ):

  n_HI = 10**(ionization_frac['HI']) *n_H
  n_HII = 10**(ionization_frac['HII']) *n_H
  n_HeI = 10**(ionization_frac['HeI']) *n_He
  n_HeII = 10**(ionization_frac['HeII']) *n_He
  n_HeIII = 10**(ionization_frac['HeIII']) *n_He
  
  # print n_HI, n_HII, n_HeI, n_HeII, n_HeIII
  
  mu = ( n_HI + n_HII + 4*( n_HeI + n_HeII + n_HeIII) ) / ( n_HI + 2*n_HII + n_HeI + 2*n_HeII + 3*n_HeIII )
  if print_out: print 'MMW= ', mu 
  return mu


composition_metals_on = [ 'no molecules' ]

composition_metals_off = [ 
'element Lithium abundance -30',
'element Beryllium abundance -30',
'element Boron abundance -30',
'element Carbon abundance -30',
'element Nitrogen abundance -30',
'element Oxygen abundance -30',
'element Fluorine abundance -30',
'element Neon abundance -30',
'element Sodium abundance -30',
'element Magnesium abundance -30',
'element Aluminum abundance -30',
'element Silicon abundance -30',
'element Phosphorus abundance -30',
'element Sulphur abundance -30',
'element Chlorine abundance -30',
'element Argon abundance -30',
'element Potassium abundance -30',
'element Calcium abundance -30',
'element Scandium abundance -30',
'element Titanium abundance -30',
'element Vanadium abundance -30',
'element Chromium abundance -30',
'element Manganese abundance -30',
'element Iron abundance -30',
'element Cobalt abundance -30',
'element Nickel abundance -30',
'element Copper abundance -30',
'element Zinc abundance -30',
'element Lithium off',
'element Beryllium off',
'element Boron off',
'element Carbon off',
'element Nitrogen off',
'element Oxygen off',
'element Fluorine off',
'element Neon off',
'element Sodium off',
'element Magnesium off',
'element Aluminum off',
'element Silicon off',
'element Phosphorus off',
'element Sulphur off',
'element Chlorine off',
'element Argon off',
'element Potassium off',
'element Calcium off',
'element Scandium off',
'element Titanium off',
'element Vanadium off',
'element Chromium off',
'element Manganese off',
'element Iron off',
'element Cobalt off',
'element Nickel off',
'element Copper off',
'element Zinc off',
'metals 1e-30',
'no molecules'
]