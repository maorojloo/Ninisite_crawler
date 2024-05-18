import requests
from bs4 import BeautifulSoup
from datetime import datetime
from persiantools.jdatetime import JalaliDate
from datetime import datetime
from persiantools.jdatetime import JalaliDate
import jdatetime
import time


class NinisiteUserCrawler():
    def __init__(self):
        pass
        
    def jDateTimeToTP(self,sh_date):
        shamsi_parts = sh_date.split("/")
        year = int(shamsi_parts[0])
        month = int(shamsi_parts[1])
        day = int(shamsi_parts[2])

        j_date = jdatetime.datetime(year, month, day)
        g_date = j_date.togregorian()
        timestamp = time.mktime(g_date.timetuple())
        
        return int(timestamp)
    
    def getUserData(self,user_id):
        url="https://www.ninisite.com/user/discussion/"+user_id
        print(url)
        response = requests.get(url)
        html_content = response.content
        soup = BeautifulSoup(html_content, "html.parser")


        data={
                "_": "user",
                "avatar":soup.find('img', class_="img w-100 lazy")["data-original"],
                "username":user_id,
                "name":soup.find('div',class_="col-xs-12 m-b-0 profile__name p-r-0").find("h4").get_text(strip=True),
                "user_id":user_id,
                "platform": "Ninisite",
                "registered_timestamp":self.jDateTimeToTP(soup.find("div",class_="col-lg-12 m-b-- p-r-0").find("span").find_all("span")[1].get_text(strip=True)),
                "url":url,
                "following_count":None,
                "follower_count":None,
                "meta_data": {}
            }
        return data


            


# topic_url="408def81-6b8a-46b2-ba2c-0c8fa178c151"
# ntc=NinisiteUserCrawler()
# topicdata=ntc.getUserData(topic_url)
# topicdata
