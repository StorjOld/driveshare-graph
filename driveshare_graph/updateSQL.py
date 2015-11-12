import uptime
import settings 
import time
import pymongo
from pymongo import MongoClient
import sqlite3

while True:
	conn = sqlite3.connect(settings.DB)
	cursor = conn.cursor()
	connection = MongoClient('localhost', 27017)
	collection = connection[settings.DBS_NAME][settings.FARMERS_COLLECTION]
	uptime.update_farmers_table(conn, cursor, collection)
	conn.close()
	time.sleep(30)
