#!/usr/bin/env python3
import os, sys, gzip
import json
import random

from flask import Flask, render_template, jsonify, abort, make_response
from flask import request, url_for
from flask import send_from_directory

#going to use Flask-SQLAlchemy to interact with the database
from flask_sqlalchemy import SQLAlchemy

# import from the 21 Developer Library
from two1.wallet import Wallet
from two1.bitserv.flask import Payment

app = Flask(__name__)

#DB -- set to test.db

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

#Models
class Variant(db.Model):
	__tablename__ = "variant"
	id = db.Column(db.Integer, primary_key=True)
	chr = db.Column(db.String(100), nullable = False)
	pos = db.Column(db.Integer, nullable = False)
	rsid = db.Column(db.String(100), nullable = False)
	ref = db.Column(db.String(100), nullable = False)
	alt = db.Column(db.String(100), nullable = False)
	AC_AFR = db.Column(db.Integer, nullable = False)
	AN_AFR = db.Column(db.Integer, nullable = False)
	AC_AMR = db.Column(db.Integer, nullable = False)
	AN_AMR = db.Column(db.Integer, nullable = False)
	AC_EAS = db.Column(db.Integer, nullable = False)
	AN_EAS = db.Column(db.Integer, nullable = False)
	AC_FIN = db.Column(db.Integer, nullable = False)
	AN_FIN = db.Column(db.Integer, nullable = False)
	AC_NFE = db.Column(db.Integer, nullable = False)
	AN_NFE = db.Column(db.Integer, nullable = False)
	AC_OTH = db.Column(db.Integer, nullable = False)
	AN_OTH = db.Column(db.Integer, nullable = False)
	AC_SAS = db.Column(db.Integer, nullable = False)
	AN_SAS = db.Column(db.Integer, nullable = False)
	annotation =  db.relationship('Annotation', backref='variant', lazy='dynamic')

class Annotation(db.Model):
	__tablename__ = "annotation"
	id = db.Column(db.Integer, primary_key=True)
	variant_id = db.Column(db.Integer, db.ForeignKey('variant.id'), nullable =False)
	allele = db.Column(db.String(100), nullable = False)
	consequence = db.Column(db.String(50), nullable= False)
	symbol = db.Column(db.String(100), nullable = False)
	gene = db.Column(db.String(100), nullable = False)
	lof = db.Column(db.String(20), nullable = True)
	lof_filter = db.Column(db.String(20), nullable = True)
	lof_flags = db.Column(db.String(20), nullable = True)
#Views
#Wallet
wallet = Wallet()
payment = Payment(app, wallet)

def make_public_variant(variant):
    new_variant = {}
    for field in variant:
        if field == 'id':
            new_variant['uri'] = url_for('get_snp', chromosome=variant['chr'], position = variant['pos'], _external=True)
        else:
            new_variant[field] = variant[field]
    return new_variant

def make_public_phenotype(pheno):
    new_pheno = {}
    for field in pheno:
        if field == 'id':
            new_pheno['uri'] = url_for('get_pheno', phenoid=pheno['id'],  _external=True)
        else:
            new_pheno[field] = pheno[field]
    return new_pheno

@app.route('/variants', methods=['GET'])
def get_variants():
	snpquery = db.session.query(Variant)
	return jsonify(variant_list = [make_public_variant(i.serialize_nogt) for i in snpquery.all()])

@app.route('/phenotypes', methods=['GET'])
def get_phenos():
	snpquery = db.session.query(Phenotype)
	return jsonify(pheno_list = [make_public_phenotype(i.serialize_nov) for i in snpquery.all()])

@app.route('/buyvariant/<chromosome>/<int:position>', methods=['GET'])
@payment.required(1)
def get_snp(chromosome, position):
    	snpquery = db.session.query(Variant).filter(Variant.chr == chromosome).filter(Variant.pos == position)
    	return jsonify(variant_list=[i.serialize for i in snpquery.all()])

@app.route('/buyphenotype/<int:phenoid>', methods=['GET'])
@payment.required(1)
def get_pheno(phenoid):
    	phenoquery = db.session.query(Phenotype).filter(Phenotype.id == phenoid)
    	return jsonify(pheno_list=[i.serialize for i in phenoquery.all()])

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)
