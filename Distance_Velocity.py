#Sony Theakanath
#Created June 30, 2013 || Updated July 4, 2013

import pyfits
import math
import matplotlib.pyplot as plt
import idlsave

#Constants (Center of NGC4449)
ra0 = 187.046261
dec0 = 44.093630

#Data
velocity = []
distance = []
hdulist = pyfits.open('/Users/Sony/Dropbox/Extra Curriculars/UCSC Research Internship/SN Checks + Latest FITS File Photometry/zspec.4N4449.fits')
s = idlsave.read('/Users/Sony/Dropbox/Extra Curriculars/UCSC Research Internship/SN Checks + Latest FITS File Photometry/deimoscsetup.sav')

for eachrow in s.allstarsrebinc:
    if(eachrow.zquality == 3 or eachrow.zquality == 4):
        ra = [float(i) for i in eachrow.ra.split(':')]
        degreeofarc = ra[0]*15 + ra[1]/4  + ra[2]/240;
        dec = eachrow.dec.split(':')
        dec[0] = dec[0].replace('+', '')
        dec = [float(i) for i in dec]
        decvalue = dec[0] + dec[1]/60 + dec[2]/3600;
        x = math.sin((degreeofarc-ra0)*math.pi/180.0)*math.cos(decvalue*math.pi/180.0);
        y = math.sin(decvalue*math.pi/180.0)*math.cos(dec0*math.pi/180.0)-math.cos(decvalue*math.pi/180.0)*math.sin(dec0*math.pi/180.0)*math.cos((degreeofarc-ra0)*math.pi/180.0);
        r = math.sqrt(x*x+y*y)*3820;
        distance.append(r)
        velocity.append(eachrow[7]*299792.458)
         
tbdata = hdulist[1].data
for eachrow in tbdata:
    if(eachrow[21] == 3 or eachrow[21] == 4):
        ra = [float(i) for i in eachrow[23].split(':')]
        degreeofarc = ra[0]*15 + ra[1]/4  + ra[2]/240;
        dec = eachrow[24].split(':')
        dec[0] = dec[0].replace('+', '')
        dec = [float(i) for i in dec]
        decvalue = dec[0] + dec[1]/60 + dec[2]/3600;
        x = math.sin((degreeofarc-ra0)*math.pi/180.0)*math.cos(decvalue*math.pi/180.0);
        y = math.sin(decvalue*math.pi/180.0)*math.cos(dec0*math.pi/180.0)-math.cos(decvalue*math.pi/180.0)*math.sin(dec0*math.pi/180.0)*math.cos((degreeofarc-ra0)*math.pi/180.0);
        r = math.sqrt(x*x+y*y)*3820;
        distance.append(r)
        velocity.append(eachrow[7]*299792.458)
        
#Plotting
plt.xlabel("Distance (kpc)")
plt.ylabel("Velocity (km/s)")
plt.ylim(150, 350) 
plt.scatter(distance, velocity);
plt.show()