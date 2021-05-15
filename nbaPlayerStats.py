'''
Redditor: u/NInjas101

Ask:  I want to be able to track a players points rebounds assists over time and come up 
with last 3 game average, last 5 game average etc

'''

import requests
import datetime 

DaysBack = 21
NumGameAverage = 5

tod = datetime.datetime.now()
d = datetime.timedelta(days = DaysBack) # 3 weeks should be enough
a = tod - d
date = str(a).split(' ')[0]

playerName = input('Player Name? ')
idUrl = 'https://www.balldontlie.io/api/v1/players?search=' + playerName
respID = requests.get(idUrl)
dataID = respID.json()['data'][0]['id']

statsUrl = 'https://www.balldontlie.io/api/v1/stats?start_date='+ date +'&player_ids[]=' + str(dataID)
respStat = requests.get(statsUrl)
data = respStat.json()['data']

assists, mins = [], []
for i in range(0,NumGameAverage):
	assists += [data[i]['ast']]
	mins += [data[i]['min']]

print(playerName, ' scored ', assists, ' assists in the past ', NumGameAverage, 'games.')
print(playerName, ' played ', mins, ' minutes in the past ', NumGameAverage, 'games.')

