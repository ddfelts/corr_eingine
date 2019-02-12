import re
import os
import sys
import string
import xml.dom.minidom
import time
import json
import corr_rules
from lib.libNormalizer import Normalize
from lib.libParser import BuildParsers
from lib.redissettings import rServer


XMLFile = "parsers/parser.xml"	
b = BuildParsers(XMLFile)
norm = Normalize()
details = b.getRuleDetail()
triggers = b.getRuleTriggers(details['rid'])
prer = b.getPreRule(details['rid'])
allrules = b.getRules(details['rid'])

st = time.time()
with open(sys.argv[1],'r') as f:
	mlogs = f.readlines()
	totals = len(mlogs)
	for nlogs in mlogs:
	    d = norm.pLog(triggers,nlogs)
	    if d:
		   c = norm.pRule(details['rid'],allrules,d)
		   if c:
			newsource = norm.buildDataSource(details['rmeta'])			
			prerule = norm.pPreRule(details['rid'],prer,nlogs)		
			if prerule:
				prules = prerule.groupdict()
				for erule in prules:
					newsource[erule] = prules[erule]	
			event = norm.doEvent(allrules['rules'][c]['info'],d)
			if event:
				b = event.groupdict()
				newsource['atype'] = allrules['rules'][c]['atype']
				newsource['aname'] = allrules['rules'][c]['aname']
				for i in b:
					newsource[i] = b[i]
				#
				#print newsource
				r.publish("logs", json.dumps(newsource))
				'''
                for i in dir(corr_rules):
					item = getattr(corr_rules,i)
					if callable(item):
					   item(newsource)
				'''	   
				#print newsource
et = time.time()
dif = et - st
print dif
print totals
