import re
import os
import sys
import string
import xml.dom.minidom

class Normalize:

	def __init__(self):
		pass

	def buildDataSource(self,r):
		d = {}
		for i in r:
			d[i] = "None"
		return d

		
	def checklog(self,trig,logline):
		d = trig.search(logline)
        if d:
		   return True
		return False

	def checkEvent(self,payload,npayload,logline):	
		d = payload.search(logline)
		if d:	
			if npayload == 'None':
				return True
			else:
				c = npayload.search(logline)
			if c: 
				return False
			else:
				return True
		return False

	def doEvent(self,trig,logline):
		d = trig.search(logline)
		if d:
			return d
		return False

	def pLog(self,triggers,log):
		for c in triggers['triggers']:
			chlog = self.checklog(c,log)
			if chlog:
				return log
		return False

	def pPreRule(self,id,prerule,log):
		if id == prerule['id']:		
			d = prerule['prerule']['regex'].search(log)
			if d:
				return d
		return False

	def pRule(self,id,rules,log):
		for id in rules:
			if id == rules['id']:
				for b in rules['rules']:
					chev = self.checkEvent(rules['rules'][b]['payload'],rules['rules'][b]['npayload'],log)
					if chev:
						return b
		return False
