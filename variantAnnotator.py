#!/usr/bin/python
import re
import pprint
import requests
import json
import ast
from ast import literal_eval
import argparse
import sys,time
import datetime
from datetime import timedelta
from datetime import datetime


# Author: Lalitha Viswanathan
# Email: visu41s@gmail.com
# Date: Mar 19 2018
# Version: 0.1

# Variant Annotator that takes VCF as input and outputs an annotated VCF with below information
# AD Allele Depth
# DP Depth of Coverage
# AF from ExAC
# Other annotations from ExAC-VEP as per SNPEff 
# Percentage of reads supporting variant v/s those supporting reference alleles

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("--inputfile", "-i", type=str, required=True)	
	parser.add_argument("--outputfile", "-o", type=str, required=True)	
	
	# Parse command line arguments
	args = parser.parse_args()

	i=0
	# Read input file 
	f=open(args.inputfile,'r')
	results=open(args.outputfile,'w')

	# list storing variant entry from vcf file 
	variant = [] 
	# list to store header 
	keys=[]

	#create a dict of keys and variant, per line 
	variant_dict={}

	pp=pprint.PrettyPrinter(width=1,indent=4)

	for line in f.readlines():
		# write initial lines to file 
		if  ((line.startswith("##") is True) and (line.startswith("##INFO") is False) and (line.startswith("##FORMAT") is False)):
			results.write(line)

		variant_dict={}

		#set annotation string to null
		annotation_string=""

		# remove trailing carriage return
		line=line.strip().replace('\n','')

		if line.startswith("#CHROM") is True:
			# Write header
			results.write("##INFO=<ID=DP,Number=1,Type=Integer,Description=\"Total depth of coverage from VCF File\">\n")
			results.write("##INFO=<ID=AF,Number=.,Type=Float,Description=\"Estimated allele frequency in the range (0,1] from ExAC\">\n")
			results.write("##INFO=<ID=TYPE,Number=1,Type=String,Description=\"Type of variation from INFO Field of VCF\">\n")
			results.write("##INFO=<ID=AO_BY_RO,Number=1,Type=String,Description=\"Percent of reads supporting variant versus those supporting reference reads\">\n")
			results.write("##INFO=<ID=FILTER,Number=1,Type=String,Description=\"Filter value from ExAC\">\n")
			results.write("##INFO=<ID=ANN,Number=1,Type=String,Description=\"Annotations=Alt-Allele_from_vep|vep_consequence|vep_major_consequence|vep_gene_name|vep_hgnc_id|vep_feature_type|vep_featureId|vep_biotype|vep_HGVSc|vep_HGVSp|vep_CDSPosition|vep_cDNAPosition,Alt-Allele_from_vep|...\">\n")
			results.write("##FORMAT=<ID=DP,Number=1,Type=Integer,Description=\"Depth of coverage including uninformative reads from VCF\">\n")
			results.write("CHROM\tPOS\tREF\tALT\tID\tQUAL\tFILTER\tINFO\n")

			# get the keys
			keys = line.split("\t")

		if line.startswith("#") is False: 
	        	variant=line.split("\t")
		
			# map keys and values
			variant_dict = dict(zip(keys,variant))
			
			# split INFO Field
			infofield=variant_dict['INFO'].replace('\n','').split(";")
			infofielddict = {k:v for k,v in (x.split('=') for x in infofield)}

			# Add Info to variant dictionary
			variant_dict['INFO_DICT']=infofielddict
			#write Chrom, Pos, Ref, Alt, Qual, Filter from I/P VCF File
			results.write(variant_dict['#CHROM']+"\t"+variant_dict['POS']+"\t"+variant_dict['REF']+"\t"+variant_dict['ALT']+"\t"+variant_dict['ID']+"\t"+variant_dict['QUAL']+"\t"+variant_dict['FILTER']+"\t")

			#Make call to ExAC REST API 
			response=requests.get("http://exac.hms.harvard.edu/rest/variant/variant/"+variant_dict['#CHROM']+'-'+variant_dict['POS']+'-'+variant_dict["REF"]+'-'+variant_dict["ALT"])
	

			# exit if response code is not 200
			if (response.status_code != requests.codes.ok):
				print "Unable to connect to Exac\n"
				response.raise_for_status()
				exit()
			# Get response from Exac
			#### BULK QUERIES PRESENTLY RETURNING 405 METHOD NOT ALLOWED MAR 18 2018 ####

			exac_response = response.json()

			# Get AF from ExAC 
			if ("allele_freq" in exac_response):
				annotation_string+="AF="+str(exac_response["allele_freq"])+","
			else:
				annotation_string+=","

			# Get DP from ExAC
			#if ("quality_metrics" in exac_response):
			#	annotation_string+="DP="+str(exac_response["quality_metrics"]["DP"])+","
			#else:
			#	annotation_string+=","
			
			# Get DP from VCF File
			annotation_string+="DP="+variant_dict['INFO_DICT']['DP']+","

			# Get TYPE from INFO Field of VCF
			annotation_string+="TYPE="+variant_dict['INFO_DICT']['TYPE']+","

			# Compute percent of reads supporting alt allele vs those supporting reference allele
			AO_list=variant_dict['INFO_DICT']['AO'].split(',')
			RO_list=variant_dict['INFO_DICT']['RO'].split(',')
			sum_AO=sum(int(entry) for entry in AO_list)
			sum_RO=sum(int(entry) for entry in RO_list)
			if ((int(sum_RO)==0) and (int(sum_AO)!=0)):
				annotation_string+="AO_BY_RO=100,"
			elif ((int(sum_AO)==0) and (int(sum_RO)!=0)):
				annotation_string+="AO_BY_RO=0,"
			else:
				#Add AO entries 
				annotation_string+="AO_BY_RO="+str((int(sum_AO)/int(sum_RO))*100)+","

			# Get FILTER from ExAC Response
			if ("filter" in exac_response):
				annotation_string+="FILTER="+str(exac_response["filter"])+","
			else:
				annotation_string+=","

			# Adding additional annotations from ExAC as per SNPEff
			if ("vep_annotations" in exac_response):
				Allelestrings=[]
				consequencestrings=[]
				majorconsequencestrings=[]
				genenamestrings=[]
				hgncidstrings=[]
				Feature_typestrings=[]
				Featurestrings=[]
				biotypestrings=[]
				exonstrings=[]
				intronstrings=[]
				HGVScstrings=[]	
				HGVSpstrings=[]
				CDSPositionstrings=[]
				cDNAPositionstrings=[]
				proteinPositionstrings=[]
				#As per SnpEff, get 
				#conseqeuence, major consequence
				#HGVSc, HGVSp, 
				#cDNA pos,len, 
				#CDS Pos, len, 
				#Protein pos, len, 
				#exon /intron rank and total
				#######################
				Allelestrings=[li['Allele'] for li in exac_response["vep_annotations"]]
				consequencestrings=[li['Consequence'] for li in exac_response["vep_annotations"]]
				majorconsequencestrings=[li['major_consequence'] for li in exac_response["vep_annotations"]]
				genenamestrings=[li['Gene'] for li in exac_response["vep_annotations"]]
				hgncidstrings=[li['HGNC_ID'] for li in exac_response["vep_annotations"]]
				Feature_typestrings=[li['Feature_type'] for li in exac_response["vep_annotations"]]
				Featurestrings=[li['Feature'] for li in exac_response["vep_annotations"]]
				biotypestrings=[li['BIOTYPE'] for li in exac_response["vep_annotations"]]
				exonstrings=[li['EXON'] for li in exac_response["vep_annotations"]]
				intronstrings=[li['INTRON'] for li in exac_response["vep_annotations"]]
				HGVScstrings=[li['HGVSc'] for li in exac_response["vep_annotations"]]
				HGVSpstrings=[li['HGVSp'] for li in exac_response["vep_annotations"]]
				CDSPositionstrings=[li['CDS_position'] for li in exac_response["vep_annotations"]]
				cDNAPositionstrings=[li['cDNA_position'] for li in exac_response["vep_annotations"]]
				proteinPositionstrings=[li['Protein_position'] for li in exac_response["vep_annotations"]]

				#######################
				#Create Annotation String#
				annotationListStart=zip(to_utf8(Allelestrings),to_utf8(consequencestrings),to_utf8(majorconsequencestrings),to_utf8(genenamestrings),to_utf8(hgncidstrings),to_utf8(Feature_typestrings),to_utf8(Featurestrings),to_utf8(biotypestrings),to_utf8(HGVScstrings),to_utf8(HGVSpstrings),to_utf8(CDSPositionstrings),to_utf8(cDNAPositionstrings))
				finalData=''
				for item in annotationListStart:
					finalData += '|'.join(str(w) for w in item)+','
				finalData = finalData[:-1]
				annotation_string+="ANN="+finalData+"\n"
			else:
				annotation_string+="\n"
		results.write(annotation_string)
		i+=1

def to_utf8(d):
     l = [str(item) for item in d]
     return l

def utf8(d):
	d1 = ast.literal_eval(json.dumps(d))
	return d1

if __name__ == "__main__":
	start_time = datetime.now()
	main()
	end_time = datetime.now()
	print('Duration: {}'.format(end_time - start_time))
