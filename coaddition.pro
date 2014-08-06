;=======================================================================
;coaddition.pro
;=======================================================================

PRO newcoadd
n_bins = 36

FOR i=0, n_bins DO BEGIN
	PRINT, 'Bin= ', i
	binfile = STRCOMPRESS('m31mstarsbibin'+STRING(i)+'.sav', /REMOVE_ALL)
	RESTORE, binfile, /VERBOSE
	tags = ['clip_ivar']
	values = ['DBLARR(13333)']

	ADD_TAGS, mstarsbibin, tags, values, binstars

	binstars.clip_ivar = binstars.ivar
	coaddstars = {binnum:0, lambda:binstars[0].lbin, spec:DBLARR(13333), ivar:DBLARR(13333), rms:DBLARR(13333), med_flux:DBLARR(13333), clip_spec:DBLARR(13333),clip_ivar:DBLARR(13333), clip_rms:DBLARR(13333)}
	currentbin = binstars(WHERE(binstars.binnum EQ i))
	coaddstars.binnum = i

	FOR j=0, 13332 DO BEGIN
		coaddstars.ivar[j] = TOTAL(currentbin.ivar[j])
		coaddstars.spec[j] = TOTAL(currentbin.ivar[j]*currentbin.spec[j])/(coaddstars.ivar[j])
		coaddstars.med_flux[j] = MEDIAN(currentbin.spec[j])
		coaddstars.rms[j] = SQRT((TOTAL(currentbin.ivar[j]*currentbin.spec[j]*currentbin.spec[j])/coaddstars.ivar[j]-(coaddstars.spec[j]*coaddstars.spec[j]))/(N_ELEMENTS(currentbin)-1))
		
		FOR k=0, N_ELEMENTS(currentbin)-1 DO BEGIN
			n_sigma = ABS(currentbin[k].spec[j]-coaddstars.med_flux[j])*SQRT(currentbin[k].ivar[j])
			currentbin.clip_ivar(WHERE(n_sigma GT 5)) = 0
		ENDFOR
		
		coaddstars.clip_ivar[j] = TOTAL(currentbin.clip_ivar[j])
		coaddstars.clip_spec[j] = TOTAL(currentbin.clip_ivar[j]*currentbin.spec[j])/(coaddstars.clip_ivar[j])
		coaddstars.clip_rms[j] = SQRT((TOTAL(currentbin.clip_ivar[j]*currentbin.spec[j]*currentbin.spec[j])/coaddstars.clip_ivar[j]-(coaddstars.clip_spec[j]*coaddstars.clip_spec[j]))/(N_ELEMENTS(WHERE(currentbin.clip_ivar NE 0))-1))
	ENDFOR

	mstarscoadd = coaddstars
	coaddfile = STRCOMPRESS('stars.sav', /REMOVE_ALL)
	SAVE, mstarscoadd, filename=coaddfile
ENDFOR
END

PRO coaddition

RESTORE,'m31mstarsbibin.sav', /VERBOSE
bibinstars_temporary = mstarsbibin

tags = ['clip_ivar']
values = ['DBLARR(13333)']

ADD_TAGS, bibinstars_temporary, tags, values, bibinstars

bibinstars.clip_ivar = bibinstars.ivar

a = {binnum:0, lambda:bibinstars[0].lambda, spec:DBLARR(13333),  ivar_sum:DBLARR(13333), rms:DBLARR(13333),  med_flux:DBLARR(13333), clip_spec:DBLARR(13333)}

mstarscoadd = REPLICATE(a, MAX(bibinstars.binnum))

binnum = 0

FOR i=0, MAX(bibinstars.binnum)-1 DO BEGIN
   currentbin = bibinstars(WHERE(bibinstars.binnum EQ binnum))
   PRINT, N_ELEMENTS(currentbin)
   mstarscoadd[i].binnum = binnum
   sum = FLTARR(13333)
   wt = FLTARR(13333)

   FOR j=0, N_ELEMENTS(currentbin)-1 DO BEGIN
      sum += currentbin[j].ivar*currentbin[j].spec
      wt += currentbin[j].ivar

   ENDFOR
   mstarscoadd[i].spec = sum/wt

   mstarscoadd[i].ivar_sum = TOTAL(currentbin.ivar)
   mstarscoadd[i].med_flux = MEDIAN(currentbin.spec)
   mstarscoadd[i].rms = 1/SQRT(mstarscoadd.ivar)

   FOR j=0, N_ELEMENTS(currentbin)-1 DO BEGIN
      flux = currentbin[j].spec
      sigma = ABS(flux-mstarscoadd[i].med_flux)*SQRT(currentbin[j].ivar)
      currentbin[j].clip_ivar(WHERE(sigma GT 5)) = 0
   ENDFOR

   sum = FLTARR(13333)
   wt = FLTARR(13333)

   FOR j=0, N_ELEMENTS(currentbin)-1 DO BEGIN
      sum += currentbin[j].clip_ivar*currentbin[j].spec
      wt += currentbin[j].clip_ivar
   ENDFOR
   mstarscoadd[i].clip_spec = sum/wt

   binnum += 1
ENDFOR

SAVE, mstarsbibin, mstarscoadd, filename='starscoadd.sav'
END
