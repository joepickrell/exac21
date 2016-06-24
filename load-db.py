import re, sys, os, gzip

from run import db, Variant, Annotation

db.create_all()

infile = gzip.open(sys.argv[1])
line = infile.readline()
vep_field_names = []
while line:
	line = bytes.decode(line)
	if line[0] == "#":
		print(" ".join([line[:14], "##INFO=<ID=CSQ"]))
		if line[:14] == "##INFO=<ID=CSQ":
			vep_field_names = line.split('Format: ')[-1].strip('">').split('|')
		line = infile.readline()
		continue
	fields = line.strip().split("\t")
	info_field = dict([(x.split('=', 1)) for x in re.split(';(?=\w)', fields[7]) if x.find('=') > -1])
	print(info_field)
	annotations = [dict(zip(vep_field_names, x.split('|'))) for x in info_field['CSQ'].split(',')]
	print(annotations)
	line = infile.readline()
	
