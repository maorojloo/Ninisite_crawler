import topicCrawler
import redis
from topicCrawler import NinisiteTopicCrawler
from pymongo import MongoClient
import datetime
from dotenv import load_dotenv
import os
import requests    
import requests
from bs4 import BeautifulSoup
from persiantools.jdatetime import JalaliDate
import jdatetime
import time
from requests.exceptions import Timeout, ConnectionError, HTTPError
import traceback
 
load_dotenv()


class TopicProducer():
    def __init__(self):
        self.userQ = redis.Redis(host=os.getenv('REDIS_HOST'), port=os.getenv('REDIS_PORT'), db=1,password=os.getenv('REDIS_PASSWD'))
        self.topickey=None
        print("mongodb://"+os.getenv('MONGO_USER')+":"+os.getenv('MONGO_PASSWD')+"@"+os.getenv('MONGO_HOST')+":"+os.getenv('MONGO_PORT')+"/")
        self.client = MongoClient("mongodb://"+os.getenv('MONGO_USER')+":"+os.getenv('MONGO_PASSWD')+"@"+os.getenv('MONGO_HOST')+":"+os.getenv('MONGO_PORT')+"/")

        db = self.client["ninisite"]
        self.users=db.users


 

    def getAtopic(self):
        key = self.userQ.randomkey().decode()
        if key==None:
            return "Q is empity"
        value = self.userQ.get(key).decode()
        # if value != "free":
        #     key=self.getAtopic()

        self.userQ.set(key, "not free")
        self.topickey=key
        return key

    def get_proxy(self):
        url="http://"+os.getenv('proxyservicehost')+":8000/get_proxy"
        response = requests.get(url)

        proxies = {
            'http': 'socks5h://127.0.0.1:9050',
            'https': 'socks5h://127.0.0.1:9050'
        }

        
        return proxies
        return response.json()
    
    def jDateTimeToTP(self,sh_date):
        shamsi_parts = sh_date.split("/")
        year = int(shamsi_parts[0])
        month = int(shamsi_parts[1])
        day = int(shamsi_parts[2])



        j_date = jdatetime.datetime(year, month, day,)
        g_date = j_date.togregorian()
        timestamp = time.mktime(g_date.timetuple())
        
        return int(timestamp)

    def get_with_retry(self,url,proxies, retries=3, backoff_factor=0.3):
        for attempt in range(retries):
            try:
                
                response = requests.get(url,timeout=5)#,proxies=proxies
                response.raise_for_status()
                if response:
                    if response.status_code==404:
                        print(f"{url} url not FOUND (404ERR)")
                    else:
                        return response
                else:
                    print("responce is None I dont really know why:)")

            except Timeout:
                print('The request timed out')

            except HTTPError as http_err:
                print(f'HTTP error occurred: {http_err}')  # e.g., 404 Not Found

            except requests.exceptions.RequestException as e:
                if attempt < retries - 1:
                    time.sleep(backoff_factor * (2 ** attempt))
                else:
                    pass
                    #raise e


    def getUserData(self,user_id,proxy):

        if self.users.find_one({'_id': user_id}):
            print("user exsist")
            return 404

        url = "https://www.ninisite.com/user/discussion/"+user_id
        response=self.get_with_retry(url,proxy)
        #response = requests.get(url,proxies=proxy)
        #response.raise_for_status()
        print(response)
        if response==None:
            return None
        elif response.status_code==403:
            return 403
        elif response.status_code==404:
            return 404

        soup = BeautifulSoup(response.text, 'html.parser')
        
        name = soup.select_one("html body div.user-section.main-section div.container-fluid.bg-white div.row div.container div.col-xl-3.col-lg-4.col-sm-12.col-xs-12.pull-xs-right.direction-rtl div.about.col-xs-12 div.col-xs-12.m-b-0.profile__name.p-r-0").get_text(strip=True)
        avatar = soup.select_one("html body div.user-section.main-section div.container-fluid div.row div.p-t-0.p-b-1.m-b-2.direction-rtl div.articles__billboard.col-xs-12 div.container div.profile__header.col-xs-12 div.container.position-relative div.pull-lg-right.pull-md-right.pull-sm-right.pull-xs-right.text-xs-center.m-x-2.profile__img a.img-anchor img.img.w-100.lazy")["src"]
        username = user_id
        user_id=user_id
        url=url
        registered_timestamp=soup.select_one("html body div.user-section.main-section div.container-fluid.bg-white div.row div.container div.col-xl-3.col-lg-4.col-sm-12.col-xs-12.pull-xs-right.direction-rtl div.about.col-xs-12 div.col-lg-12.m-b--.p-r-0").get_text(strip=True).replace("عضویت :","")
        registered_timestamp=self.jDateTimeToTP(registered_timestamp)


        data={
                "_": "user",
                "platform": "ninisite",
                "avatar":avatar,
                "username":username,
                "name":name,
                "user_id":user_id,
                "registered_timestamp":registered_timestamp,
                "url":url
            } 

        return data

    def produceToDb(self):
        user_id=self.getAtopic()
        if user_id != "Q is empity":
            proxy=self.get_proxy()
            

            userdata=None
            try:
                userdata=self.getUserData(user_id,proxy)
            except Exception as E:
                print(E)
                traceback.print_exc()

            print("______________________________________________________________________________")
            print(f"FETCHING user BY {user_id} ID")
            if userdata!=404 and userdata!=None and userdata!=403:
                user_data = {
                    "_id": userdata ["user_id"],
                    "data": userdata,
                    "inserttimestamp": datetime.datetime.now(),
                    "update_count": 0,
                    "isHistory":False,
                    "is_produced_to_kafka": 0
                }
                post_id = self.users.insert_one(user_data).inserted_id

                self.userQ.delete(user_id)
                print(f"DELETE {user_id} FROM Q")
                

            if user_id==404:
                self.user_id.delete(self.topickey)

    def healthCheck(self):
        with open('/error4healthcheck', 'w') as file:
            file.write("error")

    def __del__(self):
        self.userQ.close()
        self.client.close()





TP=TopicProducer()
while True:
    try:
        TP.produceToDb()
    except Exception as E:
        print(E)
        traceback.print_exc()
        TP.healthCheck()


