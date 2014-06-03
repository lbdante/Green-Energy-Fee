import cherrypy
from excelparse import *

class Root:

    def lookup(self, **kw):
    	
    	try:
	    	tempdict = dict(kw=kw)
	    	args = tempdict['kw']
	    	filename = 'file.xlsx'
	    	buildingcode = args['code']

	        return buildString(filename, buildingcode)

    	except Exception as e:
    		return "Lookup error."

    lookup.exposed = True

cherrypy.quickstart(Root())

#---TODO---
#load filename from a config file
#config file will also determine hostname
#and port of querying server

#TEAM MEETING FRIDAY AFTER CLASS
#define index in class root
#outside of the definition of index do index.exposed = true
#in the function index, return the return html
