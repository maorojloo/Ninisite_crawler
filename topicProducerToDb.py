import topicCrawler
import redis
from topicCrawler import NinisiteTopicCrawler
from pymongo import MongoClient
import datetime
from dotenv import load_dotenv
import os

load_dotenv()


class TopicProducer():
    def __init__(self):
        self.topicQ = redis.Redis(host=os.getenv('REDIS_HOST'), port=os.getenv('REDIS_PORT'), db=0,password=os.getenv('REDIS_PASSWD'))
        self.userQ = redis.Redis(host=os.getenv('REDIS_HOST'), port=os.getenv('REDIS_PORT'), db=1,password=os.getenv('REDIS_PASSWD'))
        self.topickey=None
        print("mongodb://"+os.getenv('MONGO_USER')+":"+os.getenv('MONGO_PASSWD')+"@"+os.getenv('MONGO_HOST')+":"+os.getenv('MONGO_PORT')+"/")
        self.client = MongoClient("mongodb://"+os.getenv('MONGO_USER')+":"+os.getenv('MONGO_PASSWD')+"@"+os.getenv('MONGO_HOST')+":"+os.getenv('MONGO_PORT')+"/")

        db = self.client["ninisite"]
        self.posts=db.posts




    def getAtopic(self):
        key = self.topicQ.randomkey().decode()
        if key==None:
            return "Q is empity"
        value = self.topicQ.get(key).decode()
        if value != "free":
            key=getAtopic(self)

        self.topicQ.set(key, "not free")
        self.topickey=key
        return key


    def produceToDb(self):
        topic_id=self.getAtopic()
        if topic_id != "Q is empity":
            ntc=NinisiteTopicCrawler()
            topicdata=ntc.getTopicData(topic_id)
            if topicdata!=404:
                for data in topicdata:
                    post_data = {
                        "_id": data ["id"],
                        "data": data,
                        "inserttimestamp": datetime.datetime.now(),
                        "update_count": 0,
                        "is_produced_to_kafka": 0
                    }
                    post_id = self.posts.insert_one(post_data).inserted_id
                    self.userQ.set(data["owner_username"],"free")
                    print("Inserted post with ID:", post_id)



                self.topicQ.delete(topic_id)

            if topicdata==404:
                self.topicQ.delete(self.topickey)

            if topicdata==[]:
                self.topicQ.set(self.topickey,"err")

       






    def __del__(self):
        self.topicQ.close()
        self.userQ.close()
        self.client.close()





TP=TopicProducer()
while True:
    
    TP.produceToDb()
