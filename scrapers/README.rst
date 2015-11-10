########
GroupB-Scripts
########
Scrapy scripts to scrape TestGroup-B data from switch.driveshare.org/api/total and switch.driveshare.org/api/json into a MongoDB. The sites are crawled every 5 minutes. The data will be used to generate metrics for TestGroup-B. 

Data from switch.driveshare.org/api/json is stored into the farmers collection in the GroupB database.
Data from switch.driveshare.org/api/total is stored into the totalStorage collection in the GroupB database. 

#####
Setup
#####
How to run on MacOSX:
::
	brew install python git 
	git clone https://github.com/Andrew-Kim/GroupB-Scripts.git 
	cd GroupB-Scripts
	pip install -r requirements.txt
	./scrapeAPI.sh

How to run on Ubuntu:
::
	apt-get install python git python-pip python-dev build-essential
	git clone https://github.com/Andrew-Kim/GroupB-Scripts.git
	cd GroupB-Scripts
	pip install -r requirements.txt
	./scrapeAPI.sh
	
#####
Accessing Database
#####
Connecting to database using python:
::
	from pymongo import MongoClient
	connection = MongoClient('localhost', 27017)
	farmers_collection = connection['GroupB']['farmers']
	total_storage_collection = connection['GroupB']['totalStorage']


#####
Copying the Database
##### 

::
	cd ~
	mongodump --db GroupB
This creates a directory named dump in the home directory. Copy the dump directory to the machine on which you want to store the GroupB data. On that machine, run the following command in the same directory that the dump directory is located in:
::
	mongorestore dump 

