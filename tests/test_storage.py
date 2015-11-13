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

    # def test_init_stats_table(self):
    #
    #     client = MongoClient('localhost', 27017)
    #     collection = client['GroupB']['totalStorage']

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
