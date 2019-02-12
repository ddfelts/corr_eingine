import re
import os
import sys
import string
import xml.etree.ElementTree as ET
from lib.libMacros import macros

class BuildParsers:

    def __init__(self,rulef):
        self.rules = {}
        tree = ET.parse(rulef).getroot()
        self.rules['key'] = tree.find("./detail/rkey").text
        self.rules['type'] = tree.find("./detail/rtype").text
        self.rules['id'] = tree.find('./detail/rid').text
        self.rules['triggers'] = []
        self.rules['prerule'] = []
        self.rules['rules'] = []
        for i in tree.find("./triggers"):
            self.rules['triggers'].append(self._Macros(i.text))
        for i in tree.find("./prerules"):
            self.rules['prerule'].append(self._Macros(i.text))
        for i in tree.findall("./rules/rule"):
            c = {}
            c['aname'] = i.get('aname')
            c['atype'] = i.get('atype')
            c['id'] = i.get('id')
            c['payload'] = self._Macros(i.find("payload").text)
            if i.find('npayload').text == "None":
                c['npayload'] = 'None'
            else:
                c['npayload'] = self._Macros(i.find("npayload").text)
            c['info'] = self._Macros(i.find('info').text)
            self.rules['rules'].append(c)  
        
    def results(self):
        return self.rules

    def _DoMacrosList(self,d):
        f = []
        for i in d:
            f.append(re.compile(self._Macros(i)))
        return f

    def _Escape(self,d):
        c = d.replace("$lt","<").replace("$gt",">")
        return c

    def _Macros(self,d):
        for i in macros:
            d = d.replace(i,macros[i])
        return re.compile(d)
