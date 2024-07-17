import json
import redis
import requests
from dotenv import load_dotenv
import os
load_dotenv()
import requests
from requests.adapters import HTTPAdapter
from urllib3.poolmanager import PoolManager
import ssl
import requests
from bs4 import BeautifulSoup
import re


client = redis.Redis(host=os.getenv('REDIS_HOST'), port=os.getenv('REDIS_PORT'), db=2,password=os.getenv('REDIS_PASSWD'))


class SSLAdapter(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        context = ssl.create_default_context()
        context.set_ciphers('DEFAULT@SECLEVEL=1')  # Example to set lower security level, adjust as needed
        kwargs['ssl_context'] = context
        return super(SSLAdapter, self).init_poolmanager(*args, **kwargs)

session = requests.Session()
session.mount('https://', SSLAdapter())

def get_proxy():
    url="http://"+os.getenv('proxyservicehost')+":8000/get_proxy"
    response = requests.get(url)

    proxies = {
        'http': 'socks5h://127.0.0.1:9050',
        'https': 'socks5h://127.0.0.1:9050'
    }

    
    return proxies
    return response.json()

 
def get_last_topic():
    url="https://www.ninisite.com/discussion/topics"
    print(url)

    response = requests.get(url)
    print(response)
    
    if response.status_code==404:
        print("404 http status code recived")
        return 404


    html_content = response.content
    soup = BeautifulSoup(html_content, "html.parser")

    articles=soup.find('div',class_="col-xs-12 category--header p-x-0")
    # a=articles.find('div',class_="col-xs-12  pull-xs-right category--item")
    # b=a.find('div',class_="col-xs-12 col-md-6 pull-xs-right")
    c=articles.find('a')["href"]

    pattern = r'\/discussion\/topic\/(\d*)'
    match = re.search(pattern, c)
    if match:
        extracted_number = match.group(1)
        print(f"Extracted number: {extracted_number}")
    else:
        print("No match found")
    return(int(extracted_number))


def load_json(filename):
    try:
        # Open the file for reading
        with open(filename, 'r') as file:
            # Load JSON data from file
            data = json.load(file)
            return data
    except FileNotFoundError:
        print("File not found.")
    except json.JSONDecodeError:
        print("Error decoding JSON.")
    except Exception as e:
        print(f"An error occurred: {e}")

def write_json_to_file(data, filename):
    try:
        with open(filename, 'w') as file:
            json.dump(data, file, indent=4)  # indent for pretty-printing
        print("JSON data has been written to the file successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")




def checkPageExsitance(disscationid):
    url="https://www.ninisite.com/discussion/topic/"+str(disscationid)
    print(url)
    
    response = session.get(url,proxies=get_proxy())

    #response = requests.get(url,proxies=get_proxy())
    # if response.status_code==403:
    #     response = requests.get(url,proxies=get_proxy())
    
    return response.status_code  


data = load_json("/app/init.json")
print("statrting from page:"+str(data["start_topic_id"]))

start_topic_id=data["start_topic_id"]
last_topic=get_last_topic()

newpagearr=list(range(start_topic_id,last_topic))



pipeline = client.pipeline()
print("pipeline created")
x=0
for key in newpagearr:
    x+=1
    pipeline.set(key, "free")
    if x>=1000:
        pipeline.execute()
        x=0

pipeline.execute()

data["start_topic_id"]=newpagearr[-1]
write_json_to_file(data, 'init.json')

print("All key-value pairs inserted successfully!")



  