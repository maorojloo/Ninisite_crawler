import json
import redis
import requests
from dotenv import load_dotenv
import os

load_dotenv()

client = redis.Redis(host=os.getenv('REDIS_HOST'), port=os.getenv('REDIS_PORT'), db=0,password=os.getenv('REDIS_PASSWD'))

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
    response = requests.get(url)
    
    return response.status_code  

data = load_json("init.json")
print("statrting from page:"+str(data["start_topic_id"]))

start_topic_id=data["start_topic_id"]
newpagearr=[]
while True:
    for i in range(0,50):
        newpagearr.append(start_topic_id)
        start_topic_id+=1
    print(start_topic_id)
    pageStatuscode=checkPageExsitance(start_topic_id)
    if pageStatuscode==404:
        break

    if start_topic_id>500:
        break

pipeline = client.pipeline()

for key in newpagearr:
    pipeline.set(key, "free")

pipeline.execute()

data["start_topic_id"]=newpagearr[-1]
write_json_to_file(data, 'init.json')

print("All key-value pairs inserted successfully!")



  