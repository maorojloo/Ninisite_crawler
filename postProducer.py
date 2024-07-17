import topicCrawler
import redis
from topicCrawler import NinisiteTopicCrawler
from pymongo import MongoClient
import datetime
from dotenv import load_dotenv
import os
import requests
from confluent_kafka import Producer
import json
import os,sys
# from dotenv import load_dotenv
from colorama import Fore, Style
import signal
import atexit
import sys
from pathlib import Path
from datetime import datetime
import re
sys.path.append(str(Path(__file__).resolve().parent.parent))
from confluent_kafka import Consumer, KafkaError
import time
from datetime import datetime, timedelta
import traceback



load_dotenv()



class PostProducer():
    def __init__(self):
        print("mongodb://"+os.getenv('MONGO_USER')+":"+os.getenv('MONGO_PASSWD')+"@"+os.getenv('MONGO_HOST')+":"+os.getenv('MONGO_PORT')+"/")
        self.client = MongoClient("mongodb://"+os.getenv('MONGO_USER')+":"+os.getenv('MONGO_PASSWD')+"@"+os.getenv('MONGO_HOST')+":"+os.getenv('MONGO_PORT')+"/")
        db = self.client["ninisite"]
        self.posts=db.posts

    def getDataFromDB(self):
        batch_size = 200


        # twenty_four_hours_ago = datetime.now() - timedelta(hours=24)
        # result = self.posts.update_many({'inserttimestamp': {'$gte': twenty_four_hours_ago}},{'$set': {'is_produced_to_kafka': 0}})
        # print(f"{result.modified_count} documents updated.")
        # time.sleep(100)
    
        documents = list(self.posts.find({'is_produced_to_kafka': 0}).limit(batch_size))

        if len(documents)>=batch_size:
            postsBatch=[]
            for doc in documents:


                post={
                    "_": "message",
                    "text":doc["data"]["text"],
                    "meta_data":{
                        "like_count":int(doc["data"]["meta_data"]["like_count"]),
                        #"dislike_count": INT
                        },
                    "release_timestamp":doc["data"]["release_timestamp"]-12600,#converting time to iran time stamp
                    "owner_id":doc["data"]["owner_id"],
                    "owner_name":doc["data"]["owner_name"],
                    "owner_avatar":doc["data"]["owner_avatar"],
                    "link":doc["data"]["link"],
                    
                    "platform":"ninisite",
                    "id":int(doc["data"]["id"]),
                    "penetration_score":int(doc["data"]["meta_data"]["like_count"]),
                    "title": doc["data"]["title"],
                    "topic_id": int(doc["data"]["topic_id"])


                }
                self.posts.update_one({'_id': doc['_id']}, {'$set': {'is_produced_to_kafka': 1}})


                postsBatch.append(post)
                
            self.prodeuceToKafka(postsBatch)
            postsBatch.clear()
        else:
            print(f"messages are less than {batch_size} we gonna try in next time")

    def prodeuceToKafka(self,msgBatch):
        topic = "forum"
        producer_config= {
                        "bootstrap.servers": "194.168.50.1:19094,194.168.50.1:29094,194.168.50.2:19094,194.168.50.2:29094",
                        "enable.ssl.certificate.verification": "false",
                        "security.protocol": "sasl_ssl",
                        "ssl.ca.location": "./secrets/ca-cert",
                        "ssl.certificate.location": "./secrets/forum-producer-cert.pem",
                        "ssl.key.location": "./secrets/forum-producer-key.pem",
                        "ssl.key.password": "4mP58fUzVvIZ0Qe6KYDQNCOjb68CC7lk",
                        "sasl.username": "forum-producer",
                        "sasl.password": "FhUfbkFkY07I26A9COp1Hgz5Dlpgbde2",
                        "sasl.mechanism": "PLAIN",
                        "auto.offset.reset": "earliest"
                    }

        config = {
                    'bootstrap.servers': '127.0.0.1:9092', 
                    'group.id': 'forum-producer', 
                    'auto.offset.reset': 'earliest',
                    'enable.auto.commit': True,  
                    'session.timeout.ms': 6000,
                    'default.topic.config': {'auto.offset.reset': 'smallest'}
                }


        producer = Producer(producer_config)

    

        producer.produce(topic=topic, key=None, value=json.dumps(msgBatch))
        print(Fore.GREEN + str(len(msgBatch))+" messages successfully produced" + Style.RESET_ALL)
        producer.flush()

    def healthCheck(self):
        with open('/error4healthcheck', 'w') as file:
            file.write("error")

    def __del__(self):
        self.client.close()





PP=PostProducer()
while True:
    try:
        PP.getDataFromDB()
        time.sleep(30)
    except Exception as E:
        print(E)
        traceback.print_exc()
        PP.healthCheck()