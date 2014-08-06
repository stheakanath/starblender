import pyfits
import numpy as np
from numpy import array
import glob
from glob import glob

a=glob('/Users/Sony Theakanath/Desktop/SIP 2013/Allslits0.4N4449.fits.gz')
b=array(a)
for i in b:
    hdu_list=pyfits.open(i)
    table_hdu=hdu_list[1]
    table_header=table_hdu.header
    print "Name of data set: "
    print i
    print "Right Ascension:"
    print table_header['RA_OBJ']
    print "Declination:"
    print table_header['DEC_OBJ']
    print "Coordinate of one end of the slit:"
    print table_header['SLITX0']
    print "Coordinate of the other end of the slit:"
    print table_header['SLITX1']
    print "Position Angle of the slit:"
    print table_header['SLITPA']
    table_data=table_hdu.data
    table_data.field(0)
    print "Position along slit length of a target:"
    print table_data.field('OBJPOS')
    print "coordinate on one end of extraction window:"
    print table_data.field('R1')
    print "coordinate on other end of extraction window:"
    print table_data.field('R2')
    print " "
    print "================================================================"
    print " "
    
