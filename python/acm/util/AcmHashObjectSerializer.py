'''
Created on Jan 12, 2018

@author: halil
'''

import json

#a=""
#b=""

class AcmHashObjectSerializer(object):
            #see: https://stackoverflow.com/questions/1305532/convert-python-dict-to-object
	def __init__(self, d):
		global a,b
		for a, b in d.items():
			if isinstance(b, (list, tuple)):
				setattr(self, a, [AcmHashObjectSerializer(x) if isinstance(x, dict) else x for x in b])
		else:
			setattr(self, a, AcmHashObjectSerializer(b) if isinstance(b, dict) else b)


	def test(self):
		print("test")

    
	@staticmethod
	def ofDict(dict_):
		return AcmHashObjectSerializer(json.loads())


