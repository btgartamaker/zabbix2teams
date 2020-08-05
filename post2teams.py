from sys import argv
import json
import requests


class Zabbix2teams:
    def __init__(self, arguments):
        self.url = arguments[1]
        self.subject = arguments[2]
        self.message = arguments[3].replace('"','\'').replace('\n','<br>')
        self.eventurl = "https://"+arguments[4]+"/tr_events.php?triggerid="+arguments[5]+"&eventid="+arguments[6]
        self.body = {}
    
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
post2teams.createbody()
post2teams.send()