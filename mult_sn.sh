#for i in 'SN2009F' 'SN2006D'; do
#	python bol_lc.py $i BVRIJH
#done

for i in 'y' 'j' 'h'; do
	python corrs.py mni_lcbol ejm_cur_dm $i nan ni 1
done





