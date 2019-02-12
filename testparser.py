import os
import sys
import string
import ast
import json
from lib.libCorrParse import CorrParser
from lib.libParser import BuildParsers

'''
with open(sys.argv[1],'r') as input:
     f = BuildParsers(sys.argv[1])
     print(f.results())
     
'''     
with open(sys.argv[1],'r') as input:
     c = ast.literal_eval(input.read())
     d = {"src":"10. 2.0.1","dst":"10.2.0.2"}
     b = CorrParser()
     k = b.corrTest(c,d)
     if k:
         d['rulename'] = c['rulename']
         d['score'] = c['score']
         d['sev'] = c['sev']
         d['pri'] = c['pri']
         print(d)



                    
