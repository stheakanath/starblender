;convert_z.pro
;Sony Theakanath

PRO convert_z, struct, newstructname

  ;creating the variables
  zarray = struct.z
  convertedstringarray = STRARR(N_ELEMENTS(zarray))
  tagarray = STRARR(N_ELEMENTS(zarray))

  FOR i = 0, N_ELEMENTS(zarray)-1 DO BEGIN
  	convertedstringarray[i] = STRING(zarray[i]*300000)
	tagarray[i] = 'vel'
  ENDFOR
  
  remove_tags, struct, 'z', b
 
  ;ADD_TAGS, b, j, p, newstructname
  struct_add_field, b, 'vel', convertedstringarray, before=before, after=after $
                      , itag=itag
  return
END

str