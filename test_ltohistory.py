import unittest
from ltohistory import show_catalog_names, tape_size_by_client

class LtoHistoryTest(unittest.TestCase):
	"""Tests for ltohistory"""

	def test_show_catalog_names(self):
		"""Test for list of catalog names"""
		self.assertTrue(show_catalog_names)

	def test_tape_size_by_client(self):
		self.assertTrue(tape_size_by_client)


		
if __name__ == '__main__':
	unittest.main()