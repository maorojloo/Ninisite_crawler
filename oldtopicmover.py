import redis
import topicCrawler
import redis
from topicCrawler import NinisiteTopicCrawler
from pymongo import MongoClient
import datetime
from dotenv import load_dotenv
import os
import requests    

 
load_dotenv()


r2 = redis.Redis(host=os.getenv('REDIS_HOST'), port=os.getenv('REDIS_PORT'), db=2,password=os.getenv('REDIS_PASSWD'))
r0 = redis.Redis(host=os.getenv('REDIS_HOST'), port=os.getenv('REDIS_PORT'), db=0,password=os.getenv('REDIS_PASSWD'))
keys = r2.keys('*')

# Move all key-value pairs from db2 to db0
for key in keys:
    value = r2.dump(key)
    ttl = r2.ttl(key)
    if ttl == -1:
        ttl = 0
    r0.restore(key, ttl, value)
    r2.delete(key)

print("All key-value pairs have been moved from db2 to db0.")
