from lib.libCorr import Corr
import hashlib
import time
import threading

p_lock = threading.Lock()

def c_portscan(d):
    if d['dpt'] == 'None':
        return
    hsh = [d['ips'],d['ipd'],"PortScanner"]
    b = Corr()
    b.OR([b.neq(443,int(d['spt'])),b.neq(80,int(d['spt']))])\
    .DCounter(hsh,destinct=d['spt'],count=20,limit=300)\
    .CheckNotInList("PortScanner",d['ips'])\
    .AddtoList("PortScanner",d['ips'])
    if b.test == True:
        with p_lock:
             print "{}-{}-PortScan from IP address-src:{}".format(int(time.time()),"000001",d['ips'])
             return
    return

def c_tcpdrops(d):
    if d['dpt'] == 'None':
        return
    hsh = [d['ips'],d['aname'],'ExcessiveTCPDrops']
    b = Corr()
    b.EQ("Firewall Deny TCP (no connection)",d['aname'])\
     .CheckNotInList("ExcessiveTCPDrops",d['ips'])\
     .Counter(hsh,count=100)\
     .AddtoList("ExcessiveTCPDrops",d['ips'])
    if b.test == True:
         with p_lock:
              print "{}-{}-Excessive TCP DENYs By Source count 100-src:{}-spt:{}-dst:{}-dpt:{}".format(int(time.time()),"0010",d['ips'],d['spt'],d['ipd'],d['dpt'])
         return
    return

def c_webtraffic(d):
    if d['spt'] == 'None':
        return
    hsh = [d['ips'],d['ipd'],"ExcessiveWebTraffic"]    
    b = Corr()
    b.OR([b.eq(80,int(d['spt'])),b.eq(443,int(d['spt']))])\
      .CheckNotInList("ExcessiveWebRequests",d['ips'])\
      .Counter(hsh,count=400)\
      .AddtoList("ExcessiveWebRequests",d['ips'])
    if b.test == True:
        with p_lock:
            print "{}-{}-Excessive OutBound WebTraffic 300 times-src:{}-spt:{}-dst:{}-dpt:{}".format(int(time.time()),"0011",d['ips'],d['spt'],d['ipd'],d['dpt'])
        return
    return

def c_dns(d):
    if d['dpt'] == 'None':
        return
    hsh = [d['ips'],d['ipd'],d['dpt'],"ExcessiveDNS"]      
    b = Corr()
    b.EQ(53,int(d['dpt']))\
     .EQ("6-302015",d['v_id'])\
     .CheckNotInList("DNSREQUESTERS",d['ips'])\
     .Counter(hsh,count=200)\
     .AddtoList("DNSREQUESTERS",d['ips'])
    if b.test == True:
        with p_lock:
            print "{}-{}-Excesive DNS Triggered 200 times-src:{}-dst:{}-dpt:{}".format(int(time.time()),"0012",d['ips'],d['ipd'],d['dpt'])
        return
    return
    
