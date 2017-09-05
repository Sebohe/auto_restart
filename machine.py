#!/usr/bin/env python3

import requests
import os
import smtplib
from email.mime.text import MIMEText

def obtainEnviromentVars():
    
    return {'URL':os.environ['EURL'],
            'GMAIL_EMAIL': os.environ['GMAIL_EMAIL'],
            'GMAIL_PASS':os.environ['GMAILS_PASS'],
            'TO_EMAIL':os.environ['TO_EMAIL']}


def jsonStatus():

    requestX = requests.get(url)

    if requestX.status_code != 200:
        #print (requestX.status_code)
        raise

    jsonX = requestX.json()
    down = False

    #print(jsonX)
    
    try:
        if jsonX['data']['reportedHashrate'] == 0:
            down = True
    except:
        down = True

    return down

def sendRestartEmails():
    pass

def sendRestartEmail():
    pass

def checkUpTime():
   
    with open('/proc/uptime','r') as f:
        line = f.readline()
   
    print (line)
    #the first column of the uptime file is the value we want
    #https://www.centos.org/docs/5/html/5.1/Deployment_Guide/s2-proc-uptime.html
    time = float(line.split(' ')[0])
    print (time)
    time = secondsToTime(time)
    
    print (time)

    return time

def secondsToTime(seconds):

    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    
    return "%d:%02d:%02d" % (h, m, s)


def restart():

    print ('Machine is down, restart')
    os.system('pgrep ethminer | xargs kill')
    os.system('systemctl reboot')


if __name__ == "__main__":


    checkUpTime()

#    enviroment = obtainEnviromentVars()
    
#    status = jsonStatus(enviroment['EURL'])

#    if status:
#        os.sys.exit()
#    else:
#        sendRestartEmails()





