import farmer_summary
import sqlite3
from pymongo import MongoClient
from time import sleep


while(True):
    conn = sqlite3.connect('summary.db')
    cursor = conn.cursor()
    client = MongoClient('localhost', 27017)
    collection = client['GroupB']['farmers']
    farmer_summary.update_table(conn, cursor, collection)
    sleep(86400)
    conn.close()

