pro combine_structs,str1,str2,strsum,structyp=structyp

if n_params() LT 2 then begin 
	print,'-syntax combine_structs,str1,str2,strsum,structyp=structyp'
	return
endif

s1=size(str1)
s2=size(str2)

if s1(1) ne s2(1) then begin
	print,'structure sizes are different'
	return
endif

str=create_struct(name=structyp,str1(0),str2(0))
strsum=replicate(str,s1(1))
copy_struct,str1,strsum
copy_struct,str2,strsum

return
end
