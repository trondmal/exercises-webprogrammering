"""
Simple test simulating two players making some moves.

@author: Krisztian Balog
"""

import requests
import time

SERVER = "http://127.0.0.1:5000"

requests.get(SERVER + "/reg/team1")  # register 1st team
time.sleep(0.5)  # wait half a second
requests.get(SERVER + "/reg/team2")  # register 2nd team
time.sleep(0.5)  # wait half a second

requests.get(SERVER + "/move/team1/2,1,right")  # 1st team moves
time.sleep(0.5)  # wait half a second
requests.get(SERVER + "/move/team2/1,2,bottom")  # 2nd team moves
time.sleep(0.5)  # wait half a second
requests.get(SERVER + "/move/team1/2,2,left")
time.sleep(0.5)
requests.get(SERVER + "/move/team2/2,0,top")
time.sleep(0.5)
requests.get(SERVER + "/move/team1/4,0,left")
time.sleep(0.5)
requests.get(SERVER + "/move/team2/1,0,top")
time.sleep(0.5)
requests.get(SERVER + "/move/team1/4,3,top")
time.sleep(0.5)
requests.get(SERVER + "/move/team2/3,2,bottom")
time.sleep(0.5)
requests.get(SERVER + "/move/team1/2,1,bottom")
time.sleep(0.5)
requests.get(SERVER + "/move/team2/5,1,left")
time.sleep(0.5)
requests.get(SERVER + "/move/team1/1,0,right")
time.sleep(0.5)
requests.get(SERVER + "/move/team2/1,1,right")
time.sleep(0.5)
requests.get(SERVER + "/move/team1/2,2,right")
time.sleep(0.5)
requests.get(SERVER + "/move/team2/3,1,top")
time.sleep(0.5)
requests.get(SERVER + "/move/team1/5,2,left")
time.sleep(0.5)
requests.get(SERVER + "/move/team2/3,3,right")
time.sleep(0.5)
requests.get(SERVER + "/move/team1/3,0,top")
time.sleep(0.5)
requests.get(SERVER + "/move/team2/4,0,bottom")
time.sleep(0.5)


# we're not making any more moves, which means that Player 1 (team1) will time out