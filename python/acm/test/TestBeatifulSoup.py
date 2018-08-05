#from beautifulsoup4 import beautifulsoup4
from bs4 import BeautifulSoup

import html


## see: https://www.crummy.com/software/BeautifulSoup/bs4/doc/
class TestBeatifulSoup(object):
	
	def __init__(self):
		pass

	def test(self):
		pass
		html_doc = "<p>&pound;682m</p>"
		soup = BeautifulSoup(html_doc, 'html.parser')
		print (soup.get_text().encode("iso8859-1"))

		
		
