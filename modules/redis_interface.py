import redis
import threading

host = "127.0.0.1"
port = 6379
db = 0

class Listener(threading.Thread):
    def __init__(self, r, channels):
        threading.Thread.__init__(self)
        self.redis = r
        self.pubsub = self.redis.pubsub()
        self.pubsub.subscribe(channels)
    
    def work(self, item):
        print(item['channel'], ":", item['data'])
    
    def run(self):
        for item in self.pubsub.listen():
            self.work(item)

class Publish():
    def __init__(self, host=host, port=port, db=db):
        self.queue = redis.StrictRedis(host=host, port=port, db=db)

    def pub(self, name, value):
        self.queue.publish(name, value)
        

def start_listen_redis(channel):
    r = redis.StrictRedis(host=host, port=port, db=db)
    client = Listener(r, [channel])
    client.start()

def publish_redis(channel, message):
    Publish().pub(channel, message)
    # print(f"Redis published [{channel}, {message}]")

def create_pubsub(channel):
    r = redis.StrictRedis(host=host, port=port, db=db)
    pubsub = r.pubsub()
    return pubsub.subscribe(channel)