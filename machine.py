#!/usr/bin/env python3

import requests
import os


address = os.environ['ADDRESS']
url = os.environ['EURL']
name = os.environ['WORKER']

requestX = requests.get(url)

if requestX.status_code != 200:
    print (requestX.status_code)


jsonX = requestX.json()

down = False

print (jsonX)
if jsonX['data']['reportedHashrate'] == 0:
    down = True


print (os.system('pgrep nm'))

if down:
    print ('Machine is down, restart')
    os.system('reboot')
