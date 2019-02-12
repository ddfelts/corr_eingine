import os
import sys
import string
import re
import time
import struct
import socket
import hashlib
from netaddr import IPAddress, IPNetwork
from lib.redissettings import rServer

class Corr():

    def __init__(self):
        self.test = True
        self.rServer = rServer()

    def __doHash(self,args):
        hsh = ''.join('{}'.format(val.replace(" ","")) for val in args)
        hsh = hashlib.sha1(hsh).hexdigest()
        return hsh

    def _ip2int(self,addr):                                                               
        return struct.unpack("!I", socket.inet_aton(addr))[0]  

    def __setTest(self,test):
        if test == True:
            self.test = True
        else:
            self.test = False

    def neq(self,a,b):
        if a != b:
            return True
        else:
            return False

    def eq(self,a,b):
        if a == b:
               return True
        else:
               return False

    def gt(self,a,b):
        if a > b:
            return True
        else:
            return False

    def ge(self,a,b):
        if a >= b:
            return True
        else:
            return False

    def lt(self,a,b):
        if a < b:
            return True
        else:
            return False
    
    def le(self,a,b):
        if a <= b:
            return True
        else:
            return False

    def req(self,a,b):
        try:
            r = re.compile(b)
            if r.search(a):
                return True
        except re.error:
            return False
            
    def nreq(self,a,b):
        try:
            r = re.compile(b)
            if r.search(a):
                return False
        except re.error:
            return True
    
    def ireq(self,a,b):
        try:
            r = re.compile(b,re.IGNORECASE)
            if r.search(a):
                return True
        except re.error:
            return False

    def irange(self,d,s,e):
        if d in range(s,e):
               return True
        else:
               return False

    def nrange(self,d,s,e):
        if d in range(s,e):
               return False
        else:
               return True        

    def doin(self,a,b):
        if a in b:
            return True
        else:
            return False
    def noin(self,a,b):
        if a in b:
            return False
        else:
            return True

    def ipcidr(self,ip,ips):
        if IPAddress(ip) in IPNetwork(ips):
            return True
        else:
            return False

    def iprange(self,ip,ips,ipe):
           t = self._ip2int(ip)
           s = self._ip2int(ips)
           e = self._ip2int(ipe)
           if int(t) >= int(s) and int(t) <= int(e): 
              return True
           else:
               return False

    def niprange(self,ip,ips,ipe):
           t = self._ip2int(ip)
           s = self._ip2int(ips)
           e = self._ip2int(ipe)
           if int(t) >= int(s) and int(t) <= int(e): 
              return False
           else:
               return True

    def add_to_list(self,w,a):
        try:
            c = self.check_a_list(w,a)
            if c:
                return True
            else:
                self.rServer.setList(w,a)
                return True
        except:
            return False
   
    def check_a_list(self,w,a):
        try:
           c = self.rServer.getList(w)
           if a.encode('UTF-8') in c:
              return True
           else:
              return False
        except:
              return False

    def check_not_list(self,w,a):
        try:
            c = self.rServer.getList(w)
            if a.encode('UTF-8') in c:
                return False
            else:
                return True
        except:
            return True

    def __checkcounter(self,hsh,count,limit,lent):
       if count >= lent:
          self.rServer.incr(hsh)
          return False		
       elif count <= lent: 
          self.rServer.setKey(hsh,limit=count,t=limit)
          return True
       else:
          return False

    def __dcheckcounter(self,hsh,d):
        c = self.rServer.getList(hsh)
        if not c:
            self.rServer.setList(hsh,d)
            return False
        if d in c:
               return False
        else:
               self.rServer.delete(d)  
               return True

    def __docounter(self,k,count,limit):
        c = self.rServer.getKey(k)
        if c == None:  
           self.rServer.setKey(k,limit=limit,t=0)
           return False
        f = self.__checkcounter(k,count,limit,int(c))
        if f == True:
           self.rServer.delete(k) 
           return True
        else:
           return False

    def __dodcounter(self,d,destinct,count,limit):
        hsh = self.__doHash(d)
        f = "{}{}".format('DESTINCT',hsh)
        g = "{}{}".format('EXPIRE',hsh)
        p = self.__docounter(g,count,limit)
        b = self.__dcheckcounter(f,destinct)
        if p == True and b == True:
            return True
        else:
            return False
        
    def NEQ(self,a,b):
        if self.test == False:
            return self
        else:
            c = self.neq(a,b)
            self.__setTest(c)
            return self   

    def EQ(self,a,b):
        if self.test == False:
            return self
        else:
            c = self.eq(a,b)
            self.__setTest(c)
            return self
    #Greater Than    
    def GT(self,a,b):
        if self.test == False:
            return self
        else:
            c =self.gt(a,b)
            self.__setTest(c)
            return self

    #Greater Than Equal To    
    def GE(self,a,b):
        if self.test == False:
            return self
        else:
            c = self.ge(a,b)
            self.__setTest(c)
            return self
    
    #Less Than    
    def LT(self,a,b):
        if self.test == False:
            return self
        else:
            c = self.lt(a,b)
            self.__setTest(c)
            return self
    
    #Less Than Equal To    
    def LE(self,a,b):
        if self.test == False:
            return self
        else:
            c = self.le(a,b)
            self.__setTest(c)
            return self
    
    #Reg Match Pattern   
    def Reg(self,a,b):
        if self.test == False:
            return self
        else:
            c = self.req(a,b)
            self.__setTest(c)
            return self
    
    #No Reg Match   
    def NReg(self,a,b):
       if self.test == False:
            return self
       else:
            c = self.nreq(a,b)
            self.__setTest(c)
            return self  

    #Ignore Case Match Pattern
    def IReg(self,a,b):
         if self.test == False:
            return self
         else:
            c = self.ireq(a,b)
            self.__setTest(c)
            return self
    
    #Test in string or in list
    def IN(self,a,b):
        if self.test == False:
            return self
        else:
            c = self.doin(a,b)
            self.__setTest(c)
            return self

    #IP in Network Range        
    def IPinCIDR(self,ip,ips):  
        if self.test == False:
            return self
        else:
            c = self.ipcidr(ip,ips)
            self.__setTest(c)
            return self
      
    def Counter(self,key,count=5,limit=300):
        if self.test == False:
            return self
        else:
            c = self.__docounter(self.__doHash(key),count,limit)
            self.__setTest(c)
            return self

    def DCounter(self,key,destinct="",count=5,limit=300):
        if self.test == False:
            return self
        else:
            c = self.__dodcounter(key,destinct,count,limit)
            self.__setTest(c)
            return self

    def AddtoList(self,w,d):
        if self.test == False:
            return self
        self.add_to_list(w,d)
        return self

    def CheckInList(self,w,d):
        if self.test == False:
            return self
        else:
            c = self.check_a_list(w,d)
            self.__setTest(c)
            return self
    
    def CheckNotInList(self,w,d):
        if self.test == False:
            return self
        else:
            c = self.check_not_list(w,d)
            self.__setTest(c)
            return self
    
    def OR(self,args):
        if self.test == False:
            return self
        for i in args:
            if i == True:
                self.test = True
                return self
        self.test = False
        return self
            
if __name__ == '__main__':
    b = Corr()
    b.EQ(1,1).OR([b.eq(3,1),b.gt(1,2)]).EQ(1,1)
    print(b.test)
    