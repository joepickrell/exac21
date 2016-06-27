import sys, os

for i in range(1, 25):
	c = str(i)
	if c == "23":
		c = "X"
	elif c == "24":
		c = "Y"
	cmd = "tabix -h ftp://ftp.broadinstitute.org/pub/ExAC_release/release0.3.1/ExAC.r0.3.1.sites.vep.vcf.gz "+c+" | python3 load-db.py"
	print(cmd)
	os.system(cmd)
