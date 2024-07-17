#import stem
from stem import Signal
from stem.control import Controller
import time
import os
import sys


TOR_CONTROL_PORT=int(9051)
TOR_CONTROL_PASSWORD=os.getenv("12345678")
TOR_RENEWIP_INTERVAL=1

def change_tor_ip(password):
    try:
        with Controller.from_port(port=TOR_CONTROL_PORT) as controller:
            controller.authenticate(password=password)
            controller.signal(Signal.NEWNYM)  # Request a new identity (IP address)
            print("Tor IP address changed successfully")
    except stem.SocketError as e:
        print(f"Unable to connect to the Tor control port: {e}")
    except stem.AuthenticationFailure as e:
        print(f"Authentication failed: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")



#for i in range(0,int(60/TOR_RENEWIP_INTERVAL)):
while True:
    change_tor_ip(TOR_CONTROL_PASSWORD)
    time.sleep(TOR_RENEWIP_INTERVAL)




# sudo nano /etc/tor/torrc 

# ControlPort 9051
# HashedControlPassword 16:426D8B91819A276860B927D54ED9CC996CB66C0EB66EF243CACAA1264A

# tor --hash-password 12345678 



# sudo service tor restart
