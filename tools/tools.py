import os, sys
from os import listdir
from os.path import isfile, join


def create_directory( dir, print_out=True ):
  if print_out: print "Creating Directory: ", dir
  indx = dir[:-1].rfind('/' )
  inDir = dir[:indx]
  dirName = dir[indx:].replace('/','')
  dir_list = next(os.walk(inDir))[1]
  if dirName in dir_list: 
      if print_out: print " Directory exists"
  else:
    os.mkdir( dir )
    if print_out: print " Directory created"
    
    

def write_parameter_file( parameters, file_name ):
  file = open( file_name, "w" )
  for param in parameters:
    file.write( param + "\n" )
  file.close()