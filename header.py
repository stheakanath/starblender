import pyfits
import numpy as np
from numpy import array
import glob
from glob import glob

a=glob('/Users/Sony/Desktop/zspec.4N4449.fits')
b=array(a)
string = "";
for i in b:
    hdu_list=pyfits.open(i)
    table_hdu=hdu_list[1]
    table_header=table_hdu.header
    string += "\n Name of data set:" 
    print i
    string += "\nRight Ascension:"
    print table_header['MRDFITS']
    string += "\nDeclination:"
    print table_header['FXPOSIT']
    string += "\nCoordinate of one end of the slit:"
    print table_header['FXMOVE']
    string += "\nCoordinate of the other end of the slit:"
    print table_header['MRD_HREAD']
    string += "\nPosition Angle of the slit:"
    print table_header['FXPAR']
    table_data=table_hdu.data
    table_data.field(0)
    string += "\nPosition along slit length of a target:"
    print table_data.field('OBJPOS')
    string += "\ncoordinate on one end of extraction window:"
    print table_data.field('R1')
    string += "\ncoordinate on other end of extraction window:"
    print table_data.field('R2')
    string += "\n "
    string += "\n================================================================"
    string += "\n "
    
