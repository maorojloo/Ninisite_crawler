import requests
from bs4 import BeautifulSoup
from datetime import datetime
from persiantools.jdatetime import JalaliDate
from datetime import datetime
from persiantools.jdatetime import JalaliDate
import jdatetime
import time
import requests
from requests.adapters import HTTPAdapter
from urllib3.poolmanager import PoolManager
import ssl
from requests.exceptions import Timeout, ConnectionError, HTTPError


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


    def get_with_retry(self,url,proxies, retries=3, backoff_factor=0.3):
        for attempt in range(retries):
            try:
                
                response = requests.get(url,timeout=5)#,proxies=proxies
                print()
                if response.status_code==404:
                    print(f"{url} url not FOUND (404ERR)")
                    return 404

                else:
                    response.raise_for_status()
                

                if response:
                    
                    if response.status_code==404:
                        print(f"{url} url not FOUND (404ERR)")
                        return 404
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

    
    
    def getTopicData(self,disscationid,proxy):
        class SSLAdapter(HTTPAdapter):
            def init_poolmanager(self, *args, **kwargs):
                context = ssl.create_default_context()
                context.set_ciphers('DEFAULT@SECLEVEL=1')  # Example to set lower security level, adjust as needed
                kwargs['ssl_context'] = context
                return super(SSLAdapter, self).init_poolmanager(*args, **kwargs)

        session = requests.Session()
        session.mount('https://', SSLAdapter())

        #response = session.get('https://www.ninisite.com/discussion/topic/51')


        url="https://www.ninisite.com/discussion/topic/"+disscationid
        #print(url)
        #response = session.get(url=url,proxies=proxy,timeout=(5, 5), verify=False)# (connect timeout, read timeout)
        response=self.get_with_retry(url,proxy)

        if response:
            if response==404:
                print("404 http status code recived")
                return 404
            if response==403:
                print("403 http status code recived")
                return 403


            html_content = response.content
            soup = BeautifulSoup(html_content, "html.parser")
            try:
                topic_Title=soup.select_one("html body div.discussion-section div.container.forum-container.text-xs-right div.row div#grid.col-xl-9.col-lg-8.col-md-12.pull-xs-none.pull-md-right article#topic.topic-post.m-b-1.p-b-0.clearfix.topic-owner div.col-xs-12.col-sm-12.col-md-8.col-lg-8.col-xl-9.p-x-0.topic-post__body.p-t-0.direction-rtl.nini-medium div.col-xs-12.m-b-1.p-x-1.forum__topic--header h1.topic-title.pull-xs-right.p-l-2.m-b-0 a").get_text(strip=True)
            except:
                return None

            articles=soup.find_all('article')
            articlesArr=[]
            for article in articles:
                articlesOBJ={}
                articlesOBJ["_"]= "message"
                articlesOBJ["title"]= topic_Title
                articlesOBJ["topic_id"]=disscationid
                
                
                articlesOBJ["text"]=article.find('div',class_="post-message topic-post__message col-xs-12 fr-view m-b-1 p-x-1").get_text(separator=' ',strip=True)

                articlesOBJ["meta_data"]={}
                articlesOBJ["meta_data"]["like_count"]=article.find('a', class_='like-count fancy__text')['data-like-count']


                date=article.find('span', class_='date').get_text(strip=True)#1386/02/18
                time=article.find('span', class_='time').get_text(strip=True)
                
                if date == "دیروز":
                    shamsi_date = jdatetime.date.today() - jdatetime.timedelta(days=1)
                    formatted_date = shamsi_date.strftime('%Y/%m/%d')
                    date=formatted_date
                elif date =="امروز":
                    shamsi_date = jdatetime.date.today()
                    formatted_date = shamsi_date.strftime('%Y/%m/%d')
                    date=formatted_date


                try:
                    articlesOBJ["release_timestamp"]=self.jDateTimeToTP(date,time)
                except:
                    print("faild to parse date "+date+"time"+time)
                    return None
                
                articlesOBJ["owner_id"]=article.find('a', class_=['col-xs-9 col-md-12 text-md-center text-xs-right nickname',"col-xs-9 col-md-12 text-md-center text-xs-right nickname moderator"])["href"].split("/")[2]
                #articlesOBJ["owner_username"]=None

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

        else:
            print("responce is NONE Donnow why?")
            articlesArr=None

        return articlesArr

            



