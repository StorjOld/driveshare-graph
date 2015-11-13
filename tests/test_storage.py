import os
import unittest
from pymongo import MongoClient
import datetime as dt
import time
import sqlite3
import pygal
import driveshare_graph.storage as storage


class Storage(unittest.TestCase):

    def test_avg_gb_farmer(self):
        client = MongoClient('localhost', 27017)
        collection = client['GroupB']['totalStorage']
        avg = storage.avg_gb_farmer(collection)
        self.assertTrue(avg > 0)

    def test_init_stats_table(self):
        conn = sqlite3.connect('data/init_test.db')
        cursor = conn.cursor()
        storage.create_stats_table(conn, cursor)
        client = MongoClient('localhost', 27017)
        collection = client['GroupB']['totalStorage']
        storage.init_stats_table(conn, cursor)
        cursor.execute('SELECT date FROM stats WHERE tb = ? AND farmers = ?',
                       (1515.23, 339))
        data = cursor.fetchall()
        self.assertTrue(len(data) > 0)

    def test_update_stats_table(self):
        conn = sqlite3.connect('data/init_test.db')
        cursor = conn.cursor()
        storage.create_stats_table(conn, cursor)
        client = MongoClient('localhost', 27017)
        collection = client['GroupB']['totalStorage']
        storage.init_stats_table(conn, cursor)
        storage.update_stats_table(cursor, collection)
        cursor.execute('SELECT *  FROM stats')
        data = cursor.fetchall()
        self.assertTrue(len(data) > 1)

    def test_total_storage_graph(self):
        client = MongoClient('localhost', 27017)
        collection = client['GroupB']['totalStorage']
        graph = storage.total_storage_graph(collection)
        self.assertTrue(isinstance(graph, pygal.Line))

    def test_total_farmers_graph(self):
        client = MongoClient('localhost', 27017)
        collection = client['GroupB']['totalStorage']
        graph = storage.total_farmers_graph(collection)
        self.assertTrue(isinstance(graph, pygal.Line))
