import redis

rServerconfig = {
    'host': 'localhost',
    'port': 6379,
    'db': 0,
}

class rServer():
    
    def __init__(self):
        self.r = redis.StrictRedis(**rServerconfig)

    def getKey(self,k):
        if self.r.exists(k):
           return self.r.get(k)
        return False

    def setKey(self,k,limit=10,t=300):
        if self.r.exists(k):
            return False
        else:
            self.r.setex(k,limit,t)
        return False

    def setList(self,hsh,d):
         return self.r.rpush(hsh,d)
            
    def getList(self,hsh):
        if self.r.exists(hsh):
            c = self.r.lrange(hsh,0,-1)
            return c
        return False

    def incr(self,hsh):
        self.r.incr(hsh,1)
        return True

    def sub(self,topic):
        d = self.r.pubsub().subscribe(topic)
        return d

    def pub(self,topic,data):
        self.r.publish(topic,data)

    def delete(self,k):
        self.r.delete(k)
