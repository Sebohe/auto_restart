#!/usr/bin/env python3

import requests
import os
import smtplib
from email.mime.text import MIMEText


def checkClientStatus():
    
    pids = [pid for pid in os.listdir('/proc') if pid.isdigit()]

    for pid in pids:
        try:
            print (open(os.path.join('/proc', pid, 'cmline'), 'rb').read())
        except:
            continue



def obtainEnviromentVars():
    
    return {'EURL':os.environ['EURL'],
            'GMAIL_EMAIL': os.environ['GMAIL_EMAIL'],
            'GMAIL_PASS':os.environ['GMAIL_PASS'],
            'TO_EMAIL':os.environ['TO_EMAIL']}


def jsonStatusDown(url):

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

def sendRestartSuccesfulEmails(recipients, sender, password):

    body = 'Succesfuly restarted machine.'
    subject = 'Restart succesful'
    emailBuilder(recipients, sender, password, body, subject)


def sendMachineDownEmails(recipients, sender, password):
    
    body = 'Machine is down, restarting machine.'
    subject = 'Machine down'
    emailBuilder(recipients, sender, password, body, subject)


def emailBuilder(recipients, sender, password, body, subject):

    #TODO, add raise exception and log it in the scenario that
    #smtp fails
    smtpServer = smtplib.SMTP('smtp.gmail.com', 587)
    smtpServer.ehlo()
    smtpServer.starttls()
    smtpServer.ehlo()
    smtpServer.login(sender, password)
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = recipients
    smtpServer.sendmail(sender, recipients, msg.as_string())
    smtpServer.quit()

def checkUpTime():
   
    with open('/proc/uptime','r') as f:
        line = f.readline()
   
    #the first column of the uptime file is the value we want
    #https://www.centos.org/docs/5/html/5.1/Deployment_Guide/s2-proc-uptime.html
    time = float(line.split(' ')[0])
    time = secondsToTime(time)

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


    checkClientStatus()

    hours, minutes, seconds =  checkUpTime().split(':')
    if hours == '0' and minutes < '3':
        #sendRestartSuccesfulEmails()
        os.sys.exit()

    envVars = obtainEnviromentVars()
    
    status = jsonStatusDown(envVars['EURL'])

    if status:
        sendMachineDownEmails(envVars['TO_EMAIL'], envVars['GMAIL_EMAIL'],
                                envVars['GMAIL_PASS'])

       #####restart()
        pass
    else:

        os.sys.exit()




