import unittest
import sqlite3
import project.uptime as uptime

class Uptime(unittest.TestCase):

    def setup(self):
        self.conn = sqlite3.connect('project/test_network.db')
        self.cursor = self.conn.cursor()

    def tearDown(self):
        self.conn.close()

    def test_address_in_db(self):
        test_address = '14wLMb2A9APqrdXJhTQArYLyivmEAf7Y1r'
        value = uptime.address_in_db(self.cursor, test_address)
        self.assertTrue(value)

        test_address = 'asdf'
        value = uptime.address_in_db(self.cursor, test_address)
        self.assertFalse(value)

    def test_average_uptime(self):
        avg_uptime = uptime.compute_average_uptime(self.cursor)
        self.assertTrue(isinstance(avg_uptime, float))


