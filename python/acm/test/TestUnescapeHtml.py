#from beautifulsoup4 import beautifulsoup4
from bs4 import BeautifulSoup

import html

class TestUnescapeHtml(object):
	
	def __init__(self):
		pass

	def test(self):
		pass
		#soup = BeautifulSoup("<p>&pound;682m</p>")
		soup = html.unescape("<p>&pound;682m</p>")
		print (soup.encode("iso8859-1"))
