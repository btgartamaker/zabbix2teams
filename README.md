# zabbix2teams - mediatype script for Zabbix and MS Teams

Python script for custom zabbix media type. Script uses MS Teams Webhooks. Would mostly be used with Zabbix versions less than 5.0 as Zabbix introduced a native mediatype for integrating with teams.

## Installation
Copy the `post2teams.py` script into the `AlertScriptsPath` 
directory which is by default `/usr/lib/zabbix/alertscripts` and make it executable:

    $ cd /usr/lib/zabbix/alertscripts
    $ wget https://raw.githubusercontent.com/btgartamaker/zabbix2teams/master/post2teams.py
    $ chmod 755 post2teams.py
    $ pip3 install requests

## Configuration on Teams Channel

To create the webhook link needed for zabbix to create message cards in the channel. Follow the steps below:

1.)Create a new channel in Teams [Team > Add channel]

2.)Add the incoming webhook connector to the channel [Channel > Connectors > Incoming Webhook > Configure]

3.) Configure the connector. Add a name and select an Image to represent the webhook in the channel

4.)Copy the outlook.office.com/webhook link

## Configuration On Zabbix

To forward Zabbix events to MS Teams a new media script needs to be created 
and associated with a user. Follow the steps below as a Zabbix Admin user:

1.) Create a new media type [Admininstration > Media Types > Create Media Type]
```
Name: Zabbix2MSTeams
Type: Script
Script name: post2teams
```

2.) Modify the Media for the Admin user [Administration > Users]
```
Type: MSTeams
Send to: string               <--- this string is not used. It should be replaced with the outlook.office.com/webhook link
When active: 1-7,00:00-24:00
Use if severity: (all)
Status: Enabled
```

3.) Configure Action [Configuration > Actions > Create Action > Action] by adding the following lines to the default message field

```
Zabbix Trigger ID: {TRIGGER.ID}
Zabbix Domain: zabbix.example.com <--- your zabbix domain
Zabbix event ID: {EVENT.ID}
```

Finally, add an operation:
```
Send to Users: Admin
Send only to: MSTeams
```
