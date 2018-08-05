# -*- coding: utf-8 -*-
import sys,io,html
from io import StringIO
from bs4 import BeautifulSoup
from acm.test.TestBeatifulSoup import TestBeatifulSoup
from acm.test.TestUnescapeHtml import TestUnescapeHtml
from acm.datasource.AcmDataSource import Alo185DataSource
from acm.config.AcmConfigManager import AcmConfigManager
import csv
#import unicodecsv as csv

class VenvAlo185DataAnalysis(object):
	def __init__(self):
		pass
		self.params={
		    "config.file":"alo185dataanalysis.config.yaml"
		    }
		self.configManager = AcmConfigManager(self.params)
		self.configManager.read()
		self.config = self.configManager.config
		#f1,f2,...f54
		self.csvFields = ["f"+str(i+1) for i in range(54)]

	def unescapeHtmlEncode(self, finPath, foutPath):
		text_=None
		with io.open(finPath, 'r', encoding="utf-8") as fin:
		    text_ = fin.read()

		text_ = html.unescape(text_)
		fieldsRow = ";".join(self.csvFields)+"\n"
		#fieldsRow = unicode(fieldsRow,"ascii")
		with io.open(foutPath, 'w', encoding="utf-8") as fout:
		    #fout.write(fieldsRow)
		    fout.write(text_)

	def extractHtmlText(self, finPath, foutPath):#use beatifulsoup to gettext in <p><p> tag
		pass
		

		#this function extracts the text in html tags
		def souper(str_):
			return BeautifulSoup(str_, 'html.parser').get_text()
			

		with open(foutPath, "w", encoding="utf-8") as fout:
			writer = csv.writer(fout, delimiter=';')
			with open(finPath,"r",  encoding='utf-8') as fin:
				reader = csv.reader(fin,delimiter=';')
				#fields = reader.fieldnames
				try:
					for row in reader:
						newrow = [souper(r) for r in row]
						writer.writerow(newrow)
				except Exception as ex:
					print("print error,",ex)
	def createChunks(self,finPath, rowCount):
		#this function extracts the text in html tags

		foutPath = finPath+"."+str(rowCount)
		with open(finPath, "r", encoding="utf-8") as fin, open(foutPath,"w",  encoding='utf-8') as fout:
			reader = csv.reader(fin, delimiter=';')
			writer = csv.writer(fout, delimiter=';')
			try:
				i=0
				for row in reader:
					writer.writerow(row)
					i=i+1
					if i>rowCount:
						break
			except Exception as ex:
				print("print error,",ex)
		return foutPath
					
						
	def convertToXml(self, finPath, foutPath):
		csvFile = finPath
		xmlFile = csvFile+'.xml'
		print ("csfFile:",csvFile)

		reader = csv.reader(open(csvFile, "r",  encoding="utf-8"),delimiter=";")
		xmlData = open(xmlFile, 'w')
		xmlData.write('<?xml version="1.0"?>' + "\n")
		# there must be only one top-level tag
		xmlData.write("<csv_data>\n" )
		for row in reader:
			xmlData.write("\t<row>\n")
			for i,f in enumerate(self.csvFields):
				print(i,f, len(row))
				r_ = row[i].replace(u"\ufeff", "")
				cell=""
				try:				
					cell = """\t\t<%s>%s</%s>\n""" %(f,r_,f)
					xmlData.write(cell)
				except:
					cell = """\t\t<%s>%s</%s>\n""" %(f,"___ERROR___",f)
					xmlData.write(cell)
			xmlData.write("\t</row>\n")
            

		xmlData.write("</csv_data>\n")
		xmlData.close()


	

	def cleanDataSource(self):
		
		#phase010
		phase010_finPath = self.config.acm.datasource.alo.path
		phase010_foutPath = self.config.acm.datasource.alo.path_phase010_htmldecoded
		#self.unescapeHtmlEncode(phase010_finPath, phase010_foutPath)
		
		#phase020
		phase020_finPath = phase010_foutPath
		phase020_foutPath = self.config.acm.datasource.alo.path_phase020_htmltextextracted
		#self.extractHtmlText(phase020_finPath,phase020_foutPath)


		#phase030, prepare data chunks
		#phase030_foutPath = self.createChunks(phase020_foutPath,100)
		
		#phase040, convert to xml for carrot2 analysis
		phase040_finPath = "/home/halil/gitlab/acm/jupyter/data/alo185.20180412/data.phase020.htmltextextracted.csv.100"
		phase040_foutPath = phase040_finPath+".xml"
		self.convertToXml(phase040_finPath,phase040_foutPath)


	def start(self):
		print("started")

		print (self.config.acm.datasource.alo.path)
		ds = Alo185DataSource(self.config.acm.datasource.alo.path10rows, sourceType="csv")
		#print (ds.df)
		print(ds.df.to_string().encode("iso8859-1"))



c_ = VenvAlo185DataAnalysis()
#c_.start()
c_.cleanDataSource()
