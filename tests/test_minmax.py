import unittest
import pygal
import driveshare_graph.minmax as minmax

class MinMax(unittest.TestCase):

    def test_minmax_chart(self):
        client = MongoClient('localhost', 27017)
        collection = client['GroupB']['totalStorage']
        graph = minmax.minmax_chart(collection)
        self.assertTrue(isinstance(graph, pygal.Line))

