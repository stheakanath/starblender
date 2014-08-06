import math
import numpy
import idlsave
import matplotlib.pyplot as pl

numpy.set_printoptions(threshold=numpy.nan)  #print arrays in their entirety 

directory_path = '/Users/Sony/Desktop/'

def save_txt(binnum, data, sav_name):
# Save the to .txt file
    savfile = directory_path+sav_name+str(binnum)+'.txt'
    f = open(savfile, 'w')
    for i in data:
        f.write(str(i))
        f.write('\n')
    f.close()

def coadd(binnum, filename):
# Calculate (and save and plot) the ivar-weighted coadds
    print binnum  #progress report
    #binfile = '/Users/Sony/Desktop/allstarsrebin'+str(x)+'.sav' change input path/file name
    #binfile = '/Users/Sony/Desktop/allstarsrebin0.sav'
    binfile = filename
    bin = idlsave.read(binfile)
    binstars = bin.t
    n_stars = len(binstars.spec)
    lbin = binstars[0].lbin
    coaddivar = [] #OVERHERE LOL
    for i in range(13333):  #for each lambda value
    # At each lambda value, check if the ivar is a valid float, and if so add it to the ivar sum for that pixel
        a = [] #length of bin
        for j in range(n_stars):  #for each star at each lambda value
            if binstars[j].ivar[i] > -9999:
                a.append(binstars[j].ivar[i])
            else:
                a.append(0)
        coaddivar.append(math.fsum(a))
    
    coaddspec = []
    for i in range(13333):
    # At each lambda value, if the ivar is not 0, calculate the sum of spec*ivar
    # and where that value is actually a value, divide by the sum of the ivars
        if coaddivar[i] == 0:
            coaddspec.append('NaN')
        else:
            a = []
            for j in range(n_stars):
                if binstars[j].spec[i] > -9999:  #if the spec is a number
                    a.append(binstars[j].spec[i]*binstars[j].ivar[i])
                else:
                    a.append(0)
            print "before a"
            print len(a)
            b = a
            a = []
            for j in b:
                if j > -9999:
                    a.append(j)
            print "after a"
            print len(a)
            coaddspec.append(math.fsum(a)/coaddivar[i])
    
    #ONTOTHIS
    coaddrms = []
    for i in range(13333):
    #rms
        if coaddivar[i] == 0:
            coaddrms.append('NaN')
        else:
            a = []
            for j in range(n_stars):
                if binstars[j].spec[i] > -9999:  #if the spec is a number
                    a.append(binstars[j].spec[i]*binstars[j].spec[i]*binstars[j].ivar[i]) # spec^2 * ivar
                else: a.append(0)
            b = a
            a = []
            for j in b:
                if j > -9999:
                    a.append(j)
            if (math.fsum(a)/coaddivar[i]-(coaddspec[i]*coaddspec[i])) < 0:
                coaddrms.append('NaN')
            else:
               # print numpy.sqrt(math.fsum(a)/coaddivar[i]-(coaddspec[i]*coaddspec[i]))/ (len(a)-1)
                coaddrms.append(numpy.sqrt(math.fsum(a)/coaddivar[i]-(coaddspec[i]*coaddspec[i]))/ (len(a)-1))

    save_txt(binnum, coaddspec, '4N4449starscoadd')
    save_txt(binnum, coaddivar, '4N4449tarscoaddivar')
    save_txt(binnum, coaddrms, '4N4449starscoaddrms')
    a = coaddspec
    coaddspec = []
    for i in a:
        if type(i) is float:
            coaddspec.append(i+(binnum*3))
        else:
            coaddspec.append(i) 
        
    pl.plot(lbin[3000:10000], coaddspec[3000:10000])
    pl.axvline(x=8504)
    pl.axvline(x=8548)
    pl.axvline(x=8669)
    pl.draw()

if __name__ == "__main__":
    #for x in range(1,2):
     #   filename = '/Users/Sony/Desktop/Data/allstarsrebin' + str(x*2)+'.sav'
    filename = '/Users/Sony/Dropbox/Extra Curriculars/UCSC Research Internship/SN Checks + Latest FITS File Photometry/zquality3stars.sav'
     #   coadd(x, filename)
    coadd(0,filename)
    pl.show()
