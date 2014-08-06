;newrebin.pro

PRO newrebin
time0 = systime(1)

;==========================================================================
;Sets the input sav file, the structure restored, and the lambda range
;for normalization 
;Change these to change the input

RESTORE, 'stars.sav', /VERBOSE
allstars  = x
lambda_lo = 7500.0
lambda_hi = 7600.0
;==========================================================================

;==========================================================================
lmin = 6000D
lmax = 10000D
lbin_int = 0.3
nlbin = FIX((lmax-lmin)/lbin_int)
;==========================================================================

;==========================================================================
;Creates new structure 'master' with these added tags, and assigns
;values for the new lambdas(lbin) and the variance (1/ivar)

tags = ['lrshift', 'lbshift','lbin', 'specbinr', 'specbinb', 'ivarbinr', 'ivarbinb', 'varr', 'varb', 'varbinr', 'varbinb', 'z', 'contb', 'contr', 'lrcont', 'lbcont', 'norm']
values = ['DBLARR(4096)', 'DBLARR(4096)','DBLARR(13333)', 'DBLARR(13333)','DBLARR(13333)','DBLARR(13333)','DBLARR(13333)','DBLARR(4096)','DBLARR(4096)','DBLARR(13333)','DBLARR(13333)','0.0','0.0','0.0','0.0','0.0','DBLARR(13333)']
ADD_TAGS, allstars, tags, values, master

master.lbin = lmin+lbin_int*DINDGEN(nlbin)
master.varr = 1.0/master.ivarr
master.varb = 1.0/master.ivarb
master.z = (DOUBLE(master.vel))/300000
;==========================================================================

;==========================================================================
unitflux=replicate(1,nlbin)
;==========================================================================

;==========================================================================
;Begins FOR loop that rebins red/blue for each spectra

FOR i=0, (N_ELEMENTS(master))-1 DO BEGIN
;==========================================================================
   
;==========================================================================
;Prints progress every 50 stars

   IF i MOD 50 EQ 0 then print, (N_ELEMENTS(master))-1-i, ' remaining', ', ',  'Time elapsed: ',$
   FIX((systime(1)-time0)/60), ' minutes'
;==========================================================================

;==========================================================================
;Adjust for doppler shift

   master[i].lrshift=master[i].lambdar/(1.+master[i].z)
   master[i].lbshift=master[i].lambdab/(1.+master[i].z)
;==========================================================================

;==========================================================================
;Rebin red spectra

   x_specrebin, master[i].lrshift, master[i].specr, master[i].lbin, newflux, var=master[i].varr, nwvar=newvar, /SILENT
   x_specrebin, master[i].lrshift, unitflux[master.specr], master[i].lbin, unitbin, var=master[i].varr, nwvar=newvar, /SILENT
   master[i].varbinr = newvar
   master[i].specbinr = newflux/unitbin

   master[i].varbinr(WHERE(master[i].varbinr EQ 0.0)) = -10.0
   master[i].ivarbinr = 1./(master[i].varbinr*unitbin)
   master[i].ivarbinr(WHERE(master[i].ivarbinr LE 0.0)) = 0.0

;==========================================================================

;==========================================================================
;Rebin blue spectra

   x_specrebin, master[i].lbshift, master[i].specb, master[i].lbin, newflux, var=master[i].varb, nwvar=newvar, /SILENT
   x_specrebin, master[i].lbshift, unitflux, master[i].lbin, unitbin, var=master[i].varb, nwvar=newvar, /SILENT
   master[i].varbinb = newvar
   master[i].specbinb = newflux/unitbin

   master[i].varbinb(WHERE(master[i].varbinb EQ 0.0)) = -10.0
   master[i].ivarbinb = 1./(master[i].varbinb*unitbin)
   master[i].ivarbinb(WHERE(master[i].ivarbinb LE 0.0)) = 0.0

;==========================================================================

ENDFOR

STOP

;==========================================================================
;Create new structure 'allstarsrebin', and add tags for combined
;red/blue spectra

newtags = ['spec','ivar','var']
newvalues = ['FLTARR(13333)','FLTARR(13333)','FLTARR(13333)']
ADD_TAGS, master, newtags, newvalues, allstarsrebin
;==========================================================================

;==========================================================================
;Combineds red/blue spectra into a single array, by assigning non-zero
;values of the red side to the spec, and then everywhere else
;assigning blue

FOR i=0, N_ELEMENTS(allstars)-1 DO BEGIN
   FOR j=0, 13332 DO BEGIN
      IF (allstarsrebin[i].specbinr[j] GE -99999 AND allstarsrebin[i].specbinr[j] LE 99999) THEN BEGIN

         allstarsrebin[i].spec[j] = allstarsrebin[i].specbinr[j]
         allstarsrebin[i].ivar[j] = allstarsrebin[i].ivarbinr[j]
         allstarsrebin[i].var[j]  = allstarsrebin[i].varbinr[j]

      ENDIF ELSE BEGIN

         allstarsrebin[i].spec[j] = allstarsrebin[i].specbinb[j]
         allstarsrebin[i].ivar[j] = allstarsrebin[i].ivarbinb[j]
         allstarsrebin[i].var[j]  = allstarsrebin[i].varbinb[j]

      ENDELSE
   ENDFOR
ENDFOR
;==========================================================================

;==========================================================================
;Normalizes spectra and ivar around the specified lambda range
FOR i=0, N_ELEMENTS(allstars)-1 DO BEGIN
   a = allstarsrebin[i].spec
   region = a(WHERE(allstarsrebin[i].lbin GE lambda_lo and allstarsrebin[i].lbin LE lambda_hi))
   med = MEDIAN(region ,/DOUBLE)
   allstarsrebin[i].spec=(allstarsrebin[i].spec)/med
   allstarsrebin[i].ivar=(allstarsrebin[i].ivar)*med*med
ENDFOR
;==========================================================================

allstarsrebin.ivar(WHERE(allstarsrebin.ivar LE -9999 OR allstarsrebin.ivar GE 9999)) = 0

;==========================================================================
;This defines the saving format, change both of these when you change ithe input

cstarsrebin = allstarsrebin
SAVE, cstarsrebin, filename='m31cstarsrebin.sav'
;==========================================================================

print, 'Total time elapsed: ', FIX((systime(1)-time0)/60), ' minutes'
print, string(7B)

END
