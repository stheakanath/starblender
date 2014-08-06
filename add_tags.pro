;=======================================================================
;add_tags.pro
;=======================================================================
PRO add_tags, struct, tagnames, values, newstr, structyp=structyp

  IF n_params() LT 3 THEN BEGIN 
      print,'Syntax - add_tags, struct, tagnames, values, newstr, structyp=structyp'
      print,'Use doc_library,"add_tags"  for more help.'  
      return
  END
  
  newstr=0
  nt=n_elements(tagnames)
  nv=n_elements(values)
  IF nt NE nv THEN BEGIN 
      print,'Number of tagnames not equal to number of tag values'
      return
  ENDIF 
  IF datatype(tagnames) NE 'STR' THEN BEGIN
      print,'tagnames must be a string array'
      return
  ENDIF 
  IF datatype(values) NE 'STR' THEN BEGIN
      print,'values must be a string array'
      return
  ENDIF 

  n_struct = n_elements(struct)

  tmpstr = mrd_struct(tagnames, values, n_struct)
  IF datatype(tmpstr) EQ 'INT' THEN BEGIN 
      print,'Error: MRD_STRUCT exited with error'
      return
  ENDIF 
  combine_structs,struct,temporary(tmpstr),newstr, structyp=structyp

  return
END
