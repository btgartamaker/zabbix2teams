#!/usr/bin/python3
from sys import argv
import json
import re
import requests


class Zabbix2teams:
    def __init__(self, arguments):
        self.url = arguments[1]
        self.subject = arguments[2]
        self.message = arguments[3]
        self.eventurl = ""
        self.body = {}
    
    def parsebody(self):
        zabbix2msteams = {
            'dynamic': {
                'zabbix_triger_id': '^Zabbix Trigger ID: .*',
                'zabbix_domain': '^Zabbix Domain: .*',
                'zabbix_event_id': '^Zabbix event ID: .*',
            },
            'static' : {

            }
        }

        parsemessage = zabbix2msteams['static']
        for key in zabbix2msteams['dynamic']:
            items=re.findall(zabbix2msteams['dynamic'][key], self.message, re.MULTILINE)
            if len(items) != 1:
                parsemessage[key] = 'Problem with "%s" matching, found %i times' % (zabbix2msteams['dynamic'][key], len(items))
                continue
            else:
                items[0] = items[0].split(':')[1].strip()
                parsemessage[key] = items[0]
        
        self.message = self.message.replace('"','\'').replace('\n','<br>')
        self.eventurl = "https://"+parsemessage['zabbix_domain']+"/tr_events.php?triggerid="+parsemessage['zabbix_triger_id']+"&eventid="+parsemessage['zabbix_event_id']

    
    def createbody(self):
        self.body = { 
            "@context": "https://schema.org/extensions",
            "@type": "MessageCard",
            "potentialAction": [
                {
                    "@type": "OpenUri",
                    "name": "Go to Alert",
                    "targets": [ {
                        "os": "default",
                        "uri": self.eventurl
                        } ]
                } ],
            "sections": [
                {
                    "activityTitle": self.subject,
                    "text": self.message,
                    "markdown": "true" 
                } ],
            "summary": "Zabbix Alert",
            "themeColor": "0072C6"
        }
    
    def send(self):
        requests.post(url = self.url, json = self.body )

post2teams = Zabbix2teams(argv)
post2teams.parsebody()
post2teams.createbody()
post2teams.send()