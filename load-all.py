import sys, os

import run

run.db.create_all()
cmd = "curl ftp://ftp.broadinstitute.org/pub/ExAC_release/release0.3.1/ExAC.r0.3.1.sites.vep.vcf.gz | gunzip - | python3 load-db.py"
print(cmd)
os.system(cmd)
