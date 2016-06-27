import re, sys, os, gzip

import run

run.db.create_all()

#infile = gzip.open(sys.argv[1])
infile = sys.stdin
line = infile.readline()
vep_field_names = []
index = 0
while line:
	#line = bytes.decode(line)
	if line[0] == "#":
		print(" ".join([line[:14], "##INFO=<ID=CSQ"]))
		if line[:14] == "##INFO=<ID=CSQ":
			vep_field_names = line.split('Format: ')[-1].strip('">').split('|')
		line = infile.readline()
		continue
	fields = line.strip().split("\t")
	if fields[6] != "PASS":
		line = infile.readline()
		continue
	info_field = dict([(x.split('=', 1)) for x in re.split(';(?=\w)', fields[7]) if x.find('=') > -1])
	#print(info_field)
	annotations = [dict(zip(vep_field_names, x.split('|'))) for x in info_field['CSQ'].split(',')]
	#print(annotations)
	v = run.Variant(chr = fields[0], pos = fields[1], rsid = fields[2], ref= fields[3], alt = fields[4], AC_AFR = info_field['AC_AFR'], AN_AFR = info_field['AN_AFR'], AC_AMR = info_field['AC_AMR'], AN_AMR = info_field['AN_AMR'], AC_EAS = info_field['AC_EAS'], AN_EAS = info_field['AN_EAS'], AC_FIN = info_field['AC_FIN'], AN_FIN = info_field['AN_FIN'], AC_NFE = info_field['AC_NFE'], AN_NFE = info_field['AN_NFE'], AC_OTH =  info_field['AC_OTH'], AN_OTH = info_field['AN_OTH'], AC_SAS = info_field['AC_SAS'], AN_SAS = info_field['AN_SAS'])
	run.db.session.add(v)
	run.db.session.flush()
	for annot in annotations:
		a = run.Annotation(variant_id = v.id, allele = annot['Allele'], consequence = annot['Consequence'], symbol = annot['SYMBOL'], gene = annot['Gene'], lof = annot["LoF"], lof_filter = annot['LoF_filter'], lof_flags = annot['LoF_flags'])
		run.db.session.add(a)
	run.db.session.commit()
	if index % 1000 ==0:
		print ("READ "+str(index)+" VARIANTS")
		print ("CHR "+fields[0]+" POS "+fields[1])
	index = index+1
	line = infile.readline()
	
