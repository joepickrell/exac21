# ExAC (v0.3.1) API

# Run:

> python3 load-all.py

> python3 run.py

# Endpoints:

/gene/{id}: get all of the variants in gene with symbol ID that have been annotated by VEP as having LOW, MODERATE, or HIGH predicted effects on the gene

/ensembl-gene/{id}: same as above, except search by Ensembl gene ID

/lof/{id}: get all of the variants in gene with symbol ID that have been annotated by LOTFEE as a high confidence loss-of-function variant
