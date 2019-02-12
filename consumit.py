import corr_rules
import time
import json
import Queue
import threading
from lib.redissettings import rServer

q = Queue.Queue()

def getLog():
    sub = rServer.sub("logs")
    while True:
        for item in sub.listen():
           if item['data'] != 1:
               q.put(item['data'])
               
               
def correlation():
    while True:
      data = q.get()               
      for i in dir(corr_rules):
        if i.startswith("c"):
           new = getattr(corr_rules,i)
           new(json.loads(data))
      q.task_done()            
                   

def main():
  for x in range(8):
    t = threading.Thread(target=correlation)
    t.daemon = True
    t.start()     
  getLog()
  q.join()

if __name__ == '__main__':   
   main()
