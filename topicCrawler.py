import requests
from bs4 import BeautifulSoup
from datetime import datetime
from persiantools.jdatetime import JalaliDate
from datetime import datetime
from persiantools.jdatetime import JalaliDate
import jdatetime
import time


class NinisiteTopicCrawler():
    def __init__(self):
        pass
    def jDateTimeToTP(self,sh_date,sh_time):
        shamsi_parts = sh_date.split("/")
        year = int(shamsi_parts[0])
        month = int(shamsi_parts[1])
        day = int(shamsi_parts[2])

        time_parts = sh_time.split(":")
        hour = int(time_parts[0])
        minute = int(time_parts[1])

        j_date = jdatetime.datetime(year, month, day, hour, minute)
        g_date = j_date.togregorian()
        timestamp = time.mktime(g_date.timetuple())
        
        return int(timestamp)



    
    
    def getTopicData(self,disscationid):
        url="https://www.ninisite.com/discussion/topic/"+disscationid
        print(url)
        response = requests.get(url)
        
        if response.status_code==404:
            print("404 http status code recived")
            return 404


        html_content = response.content
        soup = BeautifulSoup(html_content, "html.parser")

        articles=soup.find_all('article')
        articlesArr=[]
        for article in articles:
            articlesOBJ={}
            articlesOBJ["text"]=article.find('div',class_="post-message topic-post__message col-xs-12 fr-view m-b-1 p-x-1").get_text(strip=True)

            articlesOBJ["meta_data"]={}
            articlesOBJ["meta_data"]["like_count"]=article.find('a', class_='like-count fancy__text')['data-like-count']

            
            date=article.find('span', class_='date').get_text(strip=True)
            time=article.find('span', class_='time').get_text(strip=True)
            articlesOBJ["release_timestamp"]=self.jDateTimeToTP(date,time)

            
            articlesOBJ["owner_username"]=article.find('a', class_=['col-xs-9 col-md-12 text-md-center text-xs-right nickname',"col-xs-9 col-md-12 text-md-center text-xs-right nickname moderator"])["href"].split("/")[2]
            

            articlesOBJ["owner_name"]=article.find('a', class_=['col-xs-9 col-md-12 text-md-center text-xs-right nickname',"col-xs-9 col-md-12 text-md-center text-xs-right nickname moderator"]).get_text(strip=True)


            articlesOBJ["owner_avatar"]=article.find('img', class_="avatar lazy")["data-original"]


            raw_id=article["id"]
            if raw_id =="topic":
                articlesOBJ["id"]=disscationid
            else:
                articlesOBJ["id"]=raw_id.replace("post-","")


            if articlesOBJ["id"]==disscationid:
                articlesOBJ["link"]="https://www.ninisite.com/discussion/topic/"+disscationid
            else:
                article_id=articlesOBJ["id"]
                articlesOBJ["link"]=f"https://www.ninisite.com/discussion/topic/{disscationid}?postId={article_id}"

            articlesOBJ["platform"]:"Ninisite"
            articlesOBJ["penetration_score"]:articlesOBJ["meta_data"]["like_count"]
            
            articlesArr.append(articlesOBJ)

        return articlesArr

            



