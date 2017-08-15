#!/usr/bin/env python3

import requests
import os


address = os.environ['ADDRESS']
url = os.environ['EURL']
name = os.environ['WORKER']


requestX = requests.get(url+address)

if requestX.status_code != 200:
    print (requestX.status_code)


jsonX = requestX.json()

down = False
if jsonX['workers'][name]['reportedHashRate'] == '0H/s':
    down = True


if down:
    print ('Machine is down, restart')
