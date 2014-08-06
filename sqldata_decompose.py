#calculate outermag

import asciitable, numpy as np, matplotlib.pyplot as plt, math
converters = {'specobjID':[asciitable.convert_numpy(np.int64)],
'objID':[asciitable.convert_numpy(np.int64)]}
total = asciitable.read('qso2.csv', converters = converters)
totalm = total['modelmag_u']
innerm = total['fibermag_u']
totalflux = []
innerflux = []
outerflux = []
outerm = []
for i in range(len(total)):
    totalmag_i = totalm[i]
    innermag_i = innerm[i]
    totalf = 10**((totalmag_i + 48.6)/-2.5)
    innerf = 10**((innermag_i + 48.6)/-2.5)
    totalflux.append(totalf)
    innerflux.append(innerf)
    totalflux_i = totalflux[i]
    innerflux_i = innerflux[i]
    outerf = totalflux_i - innerflux_i
    outerflux.append(outerf)
    outerflux_i = outerflux[i]
    if outerflux_i < 0:
        outer_mag = 100
    else:
        outer_mag = -2.5*(math.log10(outerflux_i))-48.6
    outerm.append(outer_mag)




#calculate decomposed light
totalmag_gal = []
totalmag_qso = []
totalf_qso = []
totalf_gal=[]
for i in range(len(total)):
    outermag = outerm[i]
    innermag = innerm[i]
    magtype = 'u'
    z90 = (total['petroR90_z'])[i]
    z50 = (total['petroR50_z'])[i]
    zconc = z90/z50
    if magtype == 'u':
        A = 13.702
        B = 0.343
        C = -3.536
        D = 2.390
        E = -0.448
        F = 0.022
        G = 1.152
        H = 0.874
    if magtype == 'g' :
        A = 11.805
        B = 0.394
        C = -4.167
        D = 2.609
        E = -0.435
        F = 0.020
        G = 3.446
        H = 0.729
    if magtype == 'r' :
        A = 9.856
        B = 0.486
        C = -4.674
        D =  2.973
        E = -0.509
        F = 0.024
        G = 1.220
        H = 0.862
    if magtype == 'i':
        A = 9.099
        B = 0.520
        C = -4.753
        D =  3.039
        E = -0.525
        F = 0.025
        G =  3.855
        H = 0.707
    if magtype == 'z':
        A = 8.346
        B = 0.559
        C = -4.942
        D = 3.203
        E = -0.565
        F = 0.027
        G = 1.400
        H = 0.855
    c = -48.6
    outerflux = 10.0**(-0.4*(outermag - c))
    innerflux = 10.0**(-0.4*(innermag - c))
    x = 10.0**(-0.4*(A-c+(B*c)-C-(D*zconc)-(E*zconc**2) - (F*zconc**3)))
    q = 10.0**(-0.4*(G-c+(H*c)))
    
            
    loguess = 0
    higuess = outerflux
    count = 0
    for count in range(0,99):
   	midguess = loguess + ((higuess-loguess)/2)
   	eqmid = (q*(midguess**H) + x*(outerflux-midguess)**B) - innerflux
   	if eqmid > 0 :
                higuess = midguess
   	else:
                loguess = midguess
        count = count+1
        if abs(eqmid) <= (10.0**-6)*midguess:
                break
            
    
    outerflux_qso = midguess
    outermag_qso = -2.5*(math.log10(outerflux_qso)) + c
    innerflux_qso = q*(outerflux_qso**H)
    innermag_qso = -2.5*(math.log10(innerflux_qso)) + c
    
    
    if outerflux - outerflux_qso<10**(-30):
        outerflux_gal = 10**(-30)
    else : outerflux_gal = outerflux-outerflux_qso
    
    outermag_gal = -2.5*(math.log10(outerflux_gal)) + c
    
    
    if outerflux > outerflux_qso :
        innerflux_gal = x*(outerflux_gal**B)
    else: 
        innerflux_gal = innerflux-innerflux_qso
    
                    
    innermag_gal = -2.5*(math.log10(innerflux_gal)) + c
    
    cat = [innermag_qso, outermag_qso, innermag_gal, outermag_gal]
    
    innerf_qso = 10**((innermag_qso+48.6)/-2.5)
    outerf_qso = 10**((outermag_qso+48.6)/-2.5)
    totalf_q = innerf_qso + outerf_qso
    totalf_qso.append(totalf_q)
    totalmag_q = -2.5*(math.log10(totalf_q)) - 48.6
    totalmag_qso.append(totalmag_q)
    innerf_gal = 10**((innermag_gal+48.6)/-2.5)
    outerf_gal = 10**((outermag_gal+48.6)/-2.5)
    totalf_g = innerf_gal + outerf_gal
    totalf_gal.append(totalf_gal)
    totalmag_g = -2.5*(math.log10(totalf_g)) - 48.6
    totalmag_gal.append(totalmag_g)

#calculate distance luminosity 
from cosmocalc import cosmocalc
pi = np.pi
theta =(1.5/3600.0)*(2.0*pi)/(360.0)
angulard = []
distancel = []
radius = []
quasarlum = []
quasarlum1=[]
lquaslum = []
n=0
for i in range(len(total)):
    z_i = (total['redshift'])[i]
    d_L  = cosmocalc(z_i)
    angulard.append(d_L['DA_cm'])
    distancel.append(d_L['DL_cm'])
    DA_i= angulard[i]
    dL_i = distancel[i]
    qsof_i = totalf_qso[i]
    r = theta*DA_i
    radius.append(r)
    qlum =(qsof_i)*((4*pi)*((dL_i)**2))
    quasarlum.append(qlum)
    if quasarlum[i]>0:
       quasarlum1.append(quasarlum[i])
    else:
       quasarlum1.append(10**20)
       n = n+1
    logql = math.log10(quasarlum1[i])
    lquaslum.append(logql)



#total scattered light
zmax = 10*(3.08567758 * 10**21)
Lscat = 0
deltaz = (zmax)/10000
Niter = 10000
totlscat = []
fscat = []

for j in range(len(total)):
    quasarlum_j  = quasarlum[j]
    radius_j = radius[j]
    for i in range(1,Niter):
    	 z_i = deltaz*i
       	 Lscat = Lscat + (quasarlum_j*radius_j*deltaz)/((radius_j)**2+(z_i)**2)
    totlscat.append(Lscat)
    lscat_j = totlscat[j]
    dl_j = distancel[j]
    Fs = (0.1*lscat_j)/(4*pi*(dl_j)**2)
    fscat.append(Fs)

#deltam by difference and sum
deltamd = []
deltams = []
for i in range(len(total)):
    totalfgal_i = totalf_gal[i]
    fscat_i = fscat[i]
    if fscat_i>totalfgal_i:
       dmd = -5
    else:
       dmd = -2.5*(math.log10((totalfgal_i/(totalfgal_i-fscat_i)))) 
    dms = -2.5*(math.log10((totalfgal_i + fscat_i)/totalfgal_i))
    deltams.append(dms)
    deltamd.append(dmd)
