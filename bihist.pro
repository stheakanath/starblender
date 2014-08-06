pro bihist

bi_arr = []
for i=0, 36 do begin
   filename= strcompress('./m31mstarsbibin/m31mstarsbibin'+string(i)+'.sav',/remove_all)
   restore, filename, /verbose
   bi_arr = append(bi_arr, mstarsbibin.bi)
endfor
print, n_elements(bi_arr)
save, bi_arr, filename='bi.sav'
end

pro plot_bhist
plothist, bi_arr, yrange=[0,1200]
end
