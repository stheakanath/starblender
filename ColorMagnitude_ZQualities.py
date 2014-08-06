#Sony Theakanath
#Created June 29, 2013 || Updated July 2, 2013

import pyfits
import numpy as np
import matplotlib.pyplot as plt
import idlsave

#Photometric Data Set Up
with open('/Users/Sony/Desktop/data.txt') as f:
    content = f.readlines()  
    
s = idlsave.read('/Users/Sony/Dropbox/Extra Curriculars/UCSC Research Internship/SN Checks + Latest FITS File Photometry/deimoscsetup.sav')

alldata = []
slitname = []
rmag = []
imag = []
for line in content:
    row = line.split()
    alldata.append(row)
for parse in alldata:
    slitname.append(parse[0])
    rmag.append(parse[3])
    imag.append(parse[5])
del rmag[0]
del imag[0]
rmag = [float(i) for i in rmag]
imag = [float(i) for i in imag]

#Fits File
quality = []
actualslits = []
hdulist = pyfits.open('/Users/Sony/Desktop/zspec.4N4449.fits')
tbdata = hdulist[1].data
for eachrow in tbdata:
    quality.append(eachrow[21])
    actualslits.append(eachrow[2])
    print eachrow

#Creating Color and Sizes
size = []
color = []
colormag = []
for line in slitname:
    if line in actualslits:   
        var = actualslits.index(line)
        if(quality[var] == -2):
            color.append([1,0,0,1])
            size.append(5**2) 
        elif(quality[var] == -1):
            color.append(0.6,0,1,1)
            size.append(7**2)
        elif(quality[var] == 0):
            color.append([1,1,0,1])
            size.append(7**2) 
        elif(quality[var] == 3):
            color.append([0,0.2,1,1])
            size.append(10**2) 
        elif(quality[var] == 4):
            color.append([0,1,0,1])
            size.append(10**2)
            print var
        else:
            color.append([0,1,1,1])
            size.append(5**2) 
    else:
        size.append(1**2)
        color.append([0,0,0,.1])
del size[0]
del color[0]
size = np.array(size)
for i in range(len(imag)):
    colormag.append(rmag[i]-imag[i])

#Plotting
plt.xlabel("R-I")
plt.ylabel("I-Magnitude")
plt.scatter(colormag, imag, s=size, c = color, edgecolors='none');
plt.gca().invert_yaxis()
plt.show()