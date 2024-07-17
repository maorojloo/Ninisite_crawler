import topicCrawler
import redis
from topicCrawler import NinisiteTopicCrawler
from pymongo import MongoClient
import datetime
from dotenv import load_dotenv
import os
import requests    

 
load_dotenv()

class Report():
    def __init__(self):
        self.topicQ = redis.Redis(host=os.getenv('REDIS_HOST'), port=os.getenv('REDIS_PORT'), db=0,password=os.getenv('REDIS_PASSWD'))
        self.userQ = redis.Redis(host=os.getenv('REDIS_HOST'), port=os.getenv('REDIS_PORT'), db=1,password=os.getenv('REDIS_PASSWD'))
        self.topicnewQ = redis.Redis(host=os.getenv('REDIS_HOST'), port=os.getenv('REDIS_PORT'), db=2,password=os.getenv('REDIS_PASSWD'))

        self.topickey=None
        print("mongodb://"+os.getenv('MONGO_USER')+":"+os.getenv('MONGO_PASSWD')+"@"+os.getenv('MONGO_HOST')+":"+os.getenv('MONGO_PORT')+"/")
        self.client = MongoClient("mongodb://"+os.getenv('MONGO_USER')+":"+os.getenv('MONGO_PASSWD')+"@"+os.getenv('MONGO_HOST')+":"+os.getenv('MONGO_PORT')+"/")

        db = self.client["ninisite"]
        self.posts=db.posts

    def send_msg(self,msg, id="-1002204712290", message_thread_id=None):
        token = '7474721644:AAFhGNCwxBwxEgGEwxWgQU7NxUIkRLAMZR0'

        send_message_url = f"https://api.telegram.org/bot{token}/sendMessage"
        payload = {
            "chat_id": id,
            "text": msg
        }
        if message_thread_id:
            payload["message_thread_id"]=message_thread_id


        response = requests.post(send_message_url, json=payload)
        print(response.status_code)
        print(response.json())

        return response.json()


    def redisReport(self):
        db_size_topic = self.topicQ.dbsize()
        db_size_user =self.userQ.dbsize()
        db_size_topicnewQ =self.topicnewQ.dbsize()

        

        #memory_info_topic = self.topicQ.info('memory')['used_memory_human']
        #memory_info_user = self.userQ.info('memory')['used_memory_human']


        repText=f"""
        db_size_topic={db_size_topic}
        db_size_user={db_size_user}
        db_size_topicnewQ={db_size_topicnewQ}
        """

        # memory_info_topic={memory_info_topic}
        # memory_info_user={memory_info_user}
        return repText


    def reportDB(self):
        pipeline = [{"$count": "total_documents"}]
        result = list(self.posts.aggregate(pipeline))
        repText=None
        if result:
            count = result[0]['total_documents']
            repText=f"Total number of documents: {count}"

        return repText

    def sendReport(self):
        txt=f"""
                Ninisite Report:
                {self.redisReport()}
                {self.reportDB()}
        
        """
        self.send_msg(txt, id="-1002204712290", message_thread_id=2)



report = Report()
report.sendReport()














