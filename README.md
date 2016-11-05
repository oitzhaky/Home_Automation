# **IoT Project - Smart Home**

##Overview
The internet of things is a rapidly expanding reality.
With an expanding number of devices available to help you automate and monitor your home, it has never before been easier to try your hand at home automation.
The Home Automation project aims at providing one platform for accomplishing exactly these things.

##Key features
* Responsive WebApp for iOS, Android, and Windows
* "Press & Keep": save your remotes commands on the web and use the Arduino to send them again by command
* Movement detection - let the Arduino keep your house safe and inform you with push notifications if needed
* Control the lights and play music with just your voice
* Get notified by the web application with the current status of the appliances and important notifications.

## Base Repository, Module
We made this using these technologies:

* [Jquery](https://jquery.com/)
* [SQlite](https://www.sqlite.org)
* [Flask](http://flask.pocoo.org) 
* [Peewee](http://docs.peewee-orm.com/en/latest/)

## Getting Started
Preliminaries :
* Python 3.x
* virtualenv
* Flask

You have to git clone this repository.
```
git clone https://github.com/oitzhaky/Home_Automation.git
```
##Installation 

```
pip install -r requirements.txt
```

##Running
* On the first run, start ```init_db.py``` to initiate the database
* Run ```run.py``` to start the server

