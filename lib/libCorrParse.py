import os
import sys
import string
from lib.libCorr import Corr

class CorrParser:

    def __init_(self):
        pass

    def corrTest(self,rule,log):
        corr = Corr()
        for i in rule['rule']:
            for b in i.keys():
                if b == 'NIN':
                   try:
                       if not corr.noin(log[i['NIN'][0]],i['NIN'][0]):
                           return True
                   except KeyError:
                           return False
                if b == 'IN':
                   try:
                       if not corr.doin(log[i['IN'][0]],i['IN'][0]):
                           return True
                   except KeyError:
                           return False 
                if b == 'NLIST':
                   try:
                       if not corr.check_not_list(i['ALIST'][1],log[i['ALIST'][0]]):
                           return True
                   except KeyError:
                           return False 
                if b == 'ILIST':
                   try:
                       if not corr.check_a_list(i['ALIST'][1],log[i['ALIST'][0]]):
                           return True
                   except KeyError:
                           return False 
                if b == 'ALIST':
                   try:
                       if corr.add_to_list(i['ALIST'][1],log[i['ALIST'][0]]):
                           return True
                   except KeyError:
                           return False
                if b == "NRANGE":
                   try: 
                      if not corr.nrange(log[i['NRANGE'][0]],i['NRANGE'][1],i['NRANGE'][2]):
                         return False
                   except KeyError:
                      return False
                if b == "IRANGE":
                   try: 
                      if not corr.irange(log[i['IRANGE'][0]],i['IRANGE'][1],i['IRANGE'][2]):
                         return False
                   except KeyError:
                      return False
                if b == "IPCIDR":
                   try: 
                      if not corr.ipcidr(log[i['IPCIDR'][0]],i['IPCIDR'][1]):
                         return False
                   except KeyError:
                      return False
                if b == "NIPRANGE":
                   try: 
                      if not corr.niprange(log[i['NIPRANGE'][0]],i['NIPRANGE'][1],i['NIPRANGE'][2]):
                         return False
                   except KeyError:
                      return False
                if b == "IPRANGE":
                   try: 
                      if not corr.iprange(log[i['IPRANGE'][0]],i['IPRANGE'][1],i['IPRANGE'][2]):
                         return False
                   except KeyError:
                      return False
                if b == "NREX":
                   try: 
                      if not corr.nreq(log[i['NREX'][0]],i['NREX'][1]):
                         return False
                   except KeyError:
                      return False
                if b == "IREX":
                   try: 
                      if not corr.ireq(log[i['IREX'][0]],i['IREX'][1]):
                         return False
                   except KeyError:
                      return False
                if b == "REX":
                   try: 
                      if not corr.req(log[i['REX'][0]],i['REX'][1]):
                         return False
                   except KeyError:
                      return False
                if b == "LE":
                   try: 
                      if not corr.le(log[i['LE'][0]],i['LE'][1]):
                         return False
                   except KeyError:
                      return False
                if b == "LT":
                   try: 
                      if not corr.lt(log[i['LT'][0]],i['LT'][1]):
                         return False
                   except KeyError:
                      return False
                if b == "GE":
                   try: 
                      if not corr.ge(log[i['GE'][0]],i['GE'][1]):
                         return False
                   except KeyError:
                      return False
                if b == "GT":
                   try: 
                      if not corr.gt(log[i['GT'][0]],i['GT'][1]):
                         return False
                   except KeyError:
                      return False
                if b == "NEQ":
                   try: 
                      if not corr.neq(log[i['NEQ'][0]],i['NEQ'][1]):
                         return False
                   except KeyError:
                      return False
                if b == "EQ":
                   try:
                      if not corr.eq(log[i['EQ'][0]],i['EQ'][1]):
                         return False
                   except KeyError:
                      return False
        return True    