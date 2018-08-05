import pandas as pd
import numpy  as np

class Alo185DataSource(object):
	
	def __init__(self, csvPath, sourceType="csv"):
		pass
		if sourceType=="csv":
			self.pandasDataFrameFromCsv(csvPath)
			
	def pandasDataFrameFromCsv(self, csvPath):
		pass
		self.df = pd.read_csv(csvPath, encoding = 'utf-8')
		
		
		
	def numpyArray(self):
		pass

