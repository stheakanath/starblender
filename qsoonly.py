galu = np.array([])
galz = np.array([])
datau = np.array([])
dataz  = np.array([])
massgal = np.array([])
massdata = np.array([])
for i in range(len(qso['ra'])):
 ra_i = qso['ra'][i]
 dec_i = qso['dec'][i]
 wmatch=(((np.abs(data['RA']-ra_i))<0.00027777)&((np.abs(data['Dec']-dec_i))<0.0002777))
 if np.sum(wmatch) == 1:
    u1 = qso['u'][wmatch][0]
    galu=np.append(galu, u1)
    z1 = qso['z'][wmatch][0]
    galz = np.append(galz,z1)
    u2 = data['u'][wmatch][0]
    datau = np.append(datau,u2)
    z2 = data['z'][wmatch][0]
    dataz=np.append(dataz,z2) 
    mass1 = qso['stellarmass'][wmatch][0]
    massgal = np.append(massgal,mass1)
    mass2 = data['mass'][wmatch][0]
    massdata = np.append(massdata,mass2)

galuf=10**((galu+48.6)/-2.5)
galzf=10**((galz+48.6)/-2.5)
datauf=10**((datau+48.6)/-2.5)
datazf=10**((dataz+48.6)/-2.5)
galuzf = galuf - galzf
datauzf = datauf - datazf
qsouzf = galuzf - datauzf
qsouz = (-2.5*(log10(qsouzf))) - 48.6
