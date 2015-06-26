import requests
import json
import getpass
import unittest
from pycatdv import Catdvlib

class Test_Catdvlib(unittest.TestCase):

	def setUp(self):
		self.t = Catdvlib()
		self.t.get_auth()

	def tearDown(self):
		self.t.delete_session()

	def test_object_url(self):
		self.assertEqual(self.t.url, "http://192.168.0.101:8080/api/4")




if __name__ == '__main__':
	unittest.main()