import unittest
from ltohistory import show_catalog_names, get_catdv_textfiles

class LtoHistoryTest(unittest.TestCase):
	"""Tests for ltohistory"""

	def test_show_catalog_names(self):
		"""Test for list of catalog names"""
		self.assertTrue(show_catalog_names)

	def test_get_catdv_textfiles(self):
		"""Test for manual access to CatDV textfile"""
		self.assertTrue(get_catdv_textfiles)

		
if __name__ == '__main__':
	unittest.main()