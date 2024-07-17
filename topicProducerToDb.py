import topicCrawler
import redis
from topicCrawler import NinisiteTopicCrawler
from pymongo import MongoClient
import datetime
from dotenv import load_dotenv
import os
import requests    

 
load_dotenv()


class TopicProducer():
    def __init__(self):
        self.topicQ = redis.Redis(host=os.getenv('REDIS_HOST'), port=os.getenv('REDIS_PORT'), db=2,password=os.getenv('REDIS_PASSWD'))
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
        # if value != "free":
        #     key=self.getAtopic()

        self.topicQ.set(key, "not free")
        self.topickey=key
        return key

    def get_proxy(self):
        url="http://"+os.getenv('proxyservicehost')+":8000/get_proxy"
        response = requests.get(url)
        print(response.json())



        return response.json()

    def produceToDb(self):
        topic_id=self.getAtopic()
        if topic_id != "Q is empity":
            ntc=NinisiteTopicCrawler()
            proxy=self.get_proxy()
            topicdata=ntc.getTopicData(topic_id,proxy)
            print("______________________________________________________________________________")
            print(f"FETCHING TOPIC BY {topic_id} ID")
            if topicdata!=404 and topicdata!=None:
                # print("_________________________________________")
                # print(topicdata)
                # print("_________________________________________")
                print(f"fetched data from with post quantuty if {len(topicdata)}")
                for data in topicdata:
                    post_data = {
                        "_id": data ["id"],
                        "data": data,
                        "inserttimestamp": datetime.datetime.now(),
                        "update_count": 0,
                        "isHistory":False,
                        "is_produced_to_kafka": 0
                    }
                    #post_id = self.posts.update_one(post_data).inserted_id
                    # Insert or update the document
                    result = self.posts.update_one(
                        {'_id': post_data['_id']},  # Filter by unique identifier
                        {'$set': post_data},        # Data to be inserted or updated
                        upsert=True                 # Insert document if it does not exist
                    )



                    self.userQ.set(data["owner_id"],"free")
                    print("_________________")
                    print(data["owner_id"]) 
                    print("_________________")

                    #print("Inserted post with ID:", post_id)

                self.topicQ.delete(topic_id)
                print(f"DELETE {topic_id} FROM Q")
                

            if topicdata==404:
                self.topicQ.delete(self.topickey)
                print(self.topickey)
                print("Delettttedd")

            if topicdata==[]:
                self.topicQ.set(self.topickey,"err")

       


    def healthCheck(self):
        with open('/error4healthcheck', 'w') as file:
            file.write("error")



    def __del__(self):
        self.topicQ.close()
        self.userQ.close()
        self.client.close()





TP=TopicProducer()
while True:
    try:
      TP.produceToDb()
    except:
        TP.healthCheck()
    
