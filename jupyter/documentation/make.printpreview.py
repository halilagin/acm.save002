#!/usr/bin/python3.6
"""
Convert notebooks listed in `chapters` into latex and then a PDF.

Note:

 - The notebooks are first copied into the build_pdf directory (with a chapter
   number prepended).
"""

import sys
import re
import subprocess
import glob, os
import time


PDFOUTPUT="acm-book"

#format: [[active,filename]]
chapters=[
[True,"000100-tutorials-000-basics"],
[True,"000100-tutorials-001-dokumantasyon-nasil-yapilir"],
[True,"000100-tutorials-010-python"],
[True,"000100-tutorials-020-latex"],
[True,"000100-tutorials-030-data-wrangling"],
[True,"000100-tutorials-040-data-analyses"],
[True,"000100-tutorials-050-spark"],
[True,"000200-officials-0010-literatur-taramasi"],
[True,"000200-officials-0020-srs"],
[True,"000200-officials-0030-ssdd"],
[False,"01100-appendices"]
]

rootDir= "."
buildDir = './build'
buildPDFDir = buildDir+'/pdf'


def init():
	if not os.path.exists(buildDir):
	    os.makedirs(buildDir)
	if not os.path.exists(buildPDFDir):
	    os.makedirs(buildPDFDir)
	cwd_ = os.getcwd()
	os.chdir(buildPDFDir)
	os.system('mkdir ipython-images')
	os.chdir(cwd_)
	#os.system('cp -r exact_solvers '+build_dir)
	#os.system('cp -r utils '+build_dir)
	#os.system('cp *.html '+build_dir)
	#os.system('cp -r figures '+build_dir)
	#os.system('cp riemann.tplx '+build_dir)
	#os.system('cp *.cls '+build_dir)
	#os.system('cp riemann.bib '+build_dir)


def getChapterFilepaths(rootdir):
	filepaths=[]
	#for file in glob.glob(rootdir+"/*.ipynb"):
	#	filepaths.append(file)
	for chapter in chapters:
		if chapter[0]==True:
			filepaths.append(rootdir+"/"+chapter[1]+".ipynb")

	return filepaths

def fixTurkish_(buildFilepath):
	lines=[]
	with open(buildFilepath, "r", encoding='utf-8', errors='ignore') as source:
		lines = source.readlines()

	with open(buildFilepath,"w", encoding='utf-8', errors='ignore') as output:
		for i,line in enumerate(lines):
			line=line.replace(u"\u0131", "{\\\\i}")
			output.write(line)
	
def removeExtraTurkishPar_():
	filepath = PDFOUTPUT+".tex"
	#filepath = "/home/halil/gitlab/acm/jupyter/documentation/build/pdf/"+PDFOUTPUT+".tex"
	print(filepath)
	lines=[]
	with open(filepath, "r", encoding='utf-8', errors='ignore') as source:
		lines = source.readlines()

	with open(filepath,"w", encoding='utf-8', errors='ignore') as output:
		for i,line in enumerate(lines):
			pass
			line=line.replace("\\{\\i\\}", "{\\i}")
			#line=line.replace("\\}", "}")
			output.write(line)


def nbconvert_():
	pass
	
	filepaths = getChapterFilepaths(rootDir)
	
	for i, filepath in enumerate(filepaths):
		filename = os.path.basename(filepath)
		lines=[]
		with open(filepath, "r", encoding='utf-8', errors='ignore') as source:
			lines = source.readlines()

		buildFilepath = buildPDFDir+"/"+filename
		with open(buildFilepath,"w", encoding='utf-8', errors='ignore') as output:
			for i,line in enumerate(lines):
				output.write(line)
	
		args = ["jupyter", "nbconvert", "--to", "notebook", "--execute",
		    "--ExecutePreprocessor.kernel_name=python3",
		    "--output", filename,
		    "--ExecutePreprocessor.timeout=60", buildFilepath]
		subprocess.check_call(args)

		fixTurkish_(buildFilepath)
		

	#for i, chapter in enumerate(chapters):
	#    filename = chapter + '.ipynb'
	#    with open(filename, "r") as source:
	#	lines = source.readlines()
	#    output_filename = str(i).zfill(2)+'-'+filename
	#    with open(build_dir+output_filename, "w") as output:
	#	for line in lines:
	#	    for j, chapter_name in enumerate(chapters):
	#		# fix cross references to other chapters
	#		line = re.sub(chapter_name+'.ipynb',
	#			  str(j).zfill(2)+'-'+chapter_name+'.ipynb', line)
	#	    line = re.sub(r'from ipywidgets import interact',
	#			  'from utils.snapshot_widgets import interact', line)
	#	    line = re.sub(r'Widget Javascript not detected.  It may not be installed or enabled properly.', 
	#			  '', line)
	#	    output.write(line)
	#    args = ["jupyter", "nbconvert", "--to", "notebook", "--execute",
	#	    "--ExecutePreprocessor.kernel_name=python2",
	#	    "--output", output_filename,
	#	    "--ExecutePreprocessor.timeout=60", build_dir+output_filename]
	#    subprocess.check_call(args)


def bookbook_():
	pass
	os.chdir(buildPDFDir)
	os.system('cp  -rf ../../ipython-images/ . ')
	os.system('cp  -rf ../../images/ . ')
	os.system('rm -rf *.blg; rm -rf *.out; rm -rf *.bbl; rm -rf *.log; rm -rf *.ind; rm -rf *.ilg; rm -rf *.lot; rm -rf *.lof; rm -rf *.ind; rm -rf *.idx; rm -rf *.aux; rm -rf *.toc;rm -f combined.tex; rm -f '+PDFOUTPUT+".pdf;");
	os.system('cp  ../../refs.bib . ')
	os.system('cp  ../../latexdefs.tex . ')
	os.system('cp  ../../thesis.printpreview.tplx thesis.tplx ')
	os.system('cp  ../../*.tex . ')
	os.system('cp  ../../*.cls . ')
	os.system('cp  ../../*.sty . ')
	os.system('python3.6 -m bookbook.latex  --template thesis.tplx --output-file  '+PDFOUTPUT)
	#time.sleep(5)
	removeExtraTurkishPar_()
	os.system('pdflatex '+PDFOUTPUT)
	os.system('bibtex '+PDFOUTPUT)
	os.system('pdflatex '+PDFOUTPUT)
	os.system('pdflatex '+PDFOUTPUT)
	os.system('cp '+PDFOUTPUT +".pdf ../")
	os.chdir('..')

	#os.chdir(build_dir)
	#os.system('python3 -m bookbook.latex --output-file riemann --template riemann.tplx')
	#os.system('pdflatex riemann')
	#os.system('bibtex riemann')
	#os.system('pdflatex riemann')
	#os.system('pdflatex riemann')
	#os.system('cp riemann.pdf ..')
	#os.chdir('..')

def makePDF():
	nbconvert_()
	bookbook_()


init()
makePDF()
sys.exit(0)


