PRO binall

;Setting up the distance field
ra0 = 187.046261
dec0 = 44.093630
RESTORE, '4N4449streamstarsrebin.sav', /VERBOSE
allstarsrebin = CSTARSREBIN
distances = FLTARR(N_ELEMENTS(allstarsrebin))
FOR i =0, N_ELEMENTS(allstarsrebin)-1 DO BEGIN
   raarray = DOUBLE(STRSPLIT(allstarsrebin[i].ra, ':', /EXTRACT))
   ra = raarray[0]*15 + raarray[1]/4  + raarray[2]/240
   decarray = DOUBLE(STRSPLIT(allstarsrebin[i].dec, ':', ESCAPE='+', /EXTRACT))
   dec = decarray[0]+decarray[1]/60+decarray[2]/3600
   x = sin((ra-ra0)*!PI/180.0)*cos(dec*!PI/180.0)
   y=(sin(dec*!PI/180.0)*cos(dec0*!PI/180.0)-cos(dec*!PI/180.0)*sin(dec0*!PI/180.0)*cos((ra-ra0)*!PI/180.0))
   r = sqrt(x*x+y*y)
   rkpc = r*3820
   distances[i] = rkpc
ENDFOR
struct_add_field, allstarsrebin, 'rkpc', distances

;Getting each bin
FOR i = 0, 16 DO BEGIN
   starsrebin =  allstarsrebin(WHERE(allstarsrebin.rkpc GT i AND allstarsrebin.rkpc LT i+2))
   SAVE, starsrebin, filename = ('allstarsrebin'+i)
   i++
ENDFOR

END
