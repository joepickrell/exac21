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
	@property
	def as_dict(self):
		return {c.name: getattr(self, c.name) for c in self.__table__.columns}
	@property
	def as_dict_wannot(self):
		annotlist = [i.as_dict for i in self.annotation]
		toreturn = {c.name: getattr(self, c.name) for c in self.__table__.columns}
		toreturn["annotation_list"] = annotlist
		return toreturn
	@property
	def info(self):
		return {'id': self.id, 'chr': self.chr, 'pos': self.pos, 'rsid': self.rsid, 'ref':self.ref, 'alt':self.alt}

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
	@property
	def as_dict(self):
		return {c.name: getattr(self, c.name) for c in self.__table__.columns}
#Views
wallet = Wallet()
payment = Payment(app, wallet)

@app.route('/variant', methods=['GET'])
def get_variants():
	snpquery = db.session.query(Variant)
	return jsonify(variant_list = [i.info for i in snpquery.all()])

@app.route('/variant/<int:id>', methods=['GET'])
@payment.required(1)
def get_snp(id):
	snpquery = db.session.query(Variant).filter(Variant.id == id)
	annotquery = db.session.query(Annotation).filter(Annotation.variant_id == id)
	return jsonify(annotations=[i.as_dict for i in annotquery.all()], variant_info = [i.as_dict_wannot for i in snpquery.all()])

@app.route('/gene/<id>', methods=['GET'])
@payment.required(1000)
def get_gene_variants(id):
	annotquery = db.session.query(Annotation).filter(Annotation.symbol== id)
	variantids = set()
	for a in annotquery:
		variantids.add(a.variant_id)	
	snpquery = db.session.query(Variant).filter(Variant.id.in_(variantids))
	return jsonify(variant_list = [i.as_dict_wannot for i in snpquery.all()])

@app.route('/ensembl-gene/<id>', methods=['GET'])
@payment.required(1000)
def get_ensembl_gene_variants(id):
        annotquery = db.session.query(Annotation).filter(Annotation.gene== id)
        variantids = set()
        for a in annotquery:
                variantids.add(a.variant_id)
        snpquery = db.session.query(Variant).filter(Variant.id.in_(variantids))
        return jsonify(variant_list = [i.as_dict_wannot for i in snpquery.all()])


@app.route('/lof/<geneid>', methods=['GET'])
@payment.required(1000)
def get_lof_gene_variants(geneid):
        annotquery = db.session.query(Annotation).filter(Annotation.symbol== geneid).filter(Annotation.lof == "HC")
        variantids = set()
        for a in annotquery:
                variantids.add(a.variant_id)
        snpquery = db.session.query(Variant).filter(Variant.id.in_(variantids))
        return jsonify(variant_list = [i.as_dict_wannot for i in snpquery.all()])

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)
