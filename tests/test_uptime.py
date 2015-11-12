import os
import unittest
from pymongo import MongoClient
import datetime as dt
import time
import sqlite3
import driveshare_graph.uptime as uptime


class Uptime(unittest.TestCase):

    def setup(self):
        self.conn = sqlite3.connect('driveshare_graph/test_network.db')
        self.cursor = self.conn.cursor()
        self.client = MongoClient('localhost', 27017)
        self.collection = self.client['GroupB']['farmers']

    def tearDown(self):
        self.conn.close()

    def test_create_farmers_table(self):
        # conn = sqlite3.connect('test.db')
        # cursor = conn.cursor()
        uptime.create_farmers_table(self.conn, self.cursor)
        dir = os.path.abspath('test.db')
        boolean = os.path.exists(dir)
        self.assertTrue(boolean)

    def test_init_farmers_table(self):
        # conn = sqlite3.connect('driveshare_graph/test_network.db')
        # cursor = conn.cursor()
        # client = MongoClient('localhost', 27017)
        # collection = client['GroupB']['farmers']
        uptime.init_farmers_table(self.conn, self.cursor, self.collection)
        test_date = dt.datetime(2015, 11, 12, 0, 0, 0)
        test_time = float(time.mktime(test_date.timetuple()))
        self.cursor.execute('SELECT address FROM farmers WHERE last_date > ?', (test_time))
        data = self.cursor.fetchall()
        self.assertTrue(len(data) > 0)
        # conn.close()

    def test_address_in_db(self):
        # conn = sqlite3.connect('driveshare_graph/test_network.db')
        # cursor = conn.cursor()
        test_address = '16cyAxo1WaR1A1zJbWEz6hiZaiNbhNqoSf'
        self.assertTrue(uptime.address_in_db(self.cursor, test_address))
        # conn.close()

    def test_uptime_distribution(self):
        # conn = sqlite3.connect('driveshare_graph/test_network.db')
        # cursor = conn.cursor()
        # client = MongoClient('localhost', 27017)
        # collection = client['GroupB']['farmers']
        distribution = payments.uptime_distribution(self.cursor, self.collection)
        self.assertTrue(len(distribution) > 0)
        # conn.close()


