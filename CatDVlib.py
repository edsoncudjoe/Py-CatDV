import requests
import json
import getpass

class Cdvlib(object):

	def __init__(self):
		"""A wrapper for the CatDV Server API"""

		self.url = 'http://192.168.0.101:8080/api/4' # For Intervideo Local Testing
		self.iv_barcodes = []

	#Generic methods
	def setUrl(self):
		"""
		Stores the location of the CatDV server. 
		The user only needs to enter the server domain eg: 'google.com'
		"""
		url_input = raw_input('Enter address of the CatDV Sever (eg. \'localhost:8080\'): ')
		self.url = 'http://' + url_input + '/api/4'
		return self.url

	def setAuth(self, username, password):
		"""Api request with given login info"""
		self.auth = self.url + "/session?usr=" + username + "&pwd=" + password
		return self.auth
	
	def getAuth(self):
		"""Enables the user to login to their CatDV database."""
		print('\nEnter login details for CatDV: ')
		usr = raw_input('Enter username: ')
		pwd = getpass.getpass('Enter password: ')
		self.setAuth(usr, pwd)
		return
		#self.auth = self.url + "/session?usr=" + usr + "&pwd=" + pwd
		#return self.auth

	def getSessionKey(self):
		"""Extracts the session key from login to be used for future API calls."""
		connect_timeout = 0.1
		try:
			response = requests.get(self.auth, timeout=(connect_timeout, 60.0))
			self.status = response.status_code
			keydata = json.loads(response.text)
			self.key = keydata['data']['jsessionid']
			return self.key
		except requests.exceptions.ConnectTimeout as e:
			print "The server connection timed-out."
		except requests.exceptions.ConnectionError as e:
			raise e
			print('\nCan\'t access the API.'
				' Please check you have the right domain address')
		except TypeError:
			print('\nYou provided incorrect login details.'
				' Please check and try again.')

	def getCatalogName(self):
		"""Call to get information on all available catalogs."""
		catalogs = requests.get(self.url + "/catalogs;jsessionid=" + str(self.key))
		catalog_data = json.loads(catalogs.text)
		self.catalog_names = []
		for i in catalog_data['data']:
			if i['ID'] > 1:
				self.catalog_names.append((i['groupName'], i['ID']))
		return self.catalog_names

	def getCatalogClips(self, catalog_id):
		"""Requests all clips from a client catalog. Filtered by catalog ID."""
		content_raw = requests.get(
			self.url + '/clips;jsessionid=' + self.key + '?filter=and((catalog.id)eq({}))'
			'&include=userFields'.format(catalog_id))
		self.content_data = json.loads(content_raw.text)
		return self.content_data

	def clipSearch(self):
		"""Returns all clips that match the given search term"""
		entry = raw_input('Enter title: ')
		result = requests.get(
			self.url + '/clips;jsessionid=' + self.key + '?filter=and((clip.name)'
				'has({}))&include=userFields'.format(entry))
		jdata = json.loads(result.text)
		for i in jdata['data']['items']:
			if i['userFields']['U7']:        
				print i['userFields']['U7'], i['name']
			else:
				print i['name']

	def deleteSession(self):
		"""HTTP delete call to the API"""
		return requests.delete(self.url + '/session')

	#Intervideo Specific
	def getIVNumbers(self, data): # Generator.
		"""Generator to identify Intervideo barcode numbers"""
		count = 0
		try:
			for i in data['data']['items']:
				if 'userFields' in i.keys():
					if 'U7' in i['userFields']: #if i['userFields']['U7']??
						count += 1
						yield i['userFields']['U7']
		except:
			print('Possible Error at position {}'.format(count))

	def collectIVNumbers(self):
		"""Collects Intervideo barcodes into a list."""
		try:
			iv_gen = self.getIVNumbers(self.content_data)
			count = 0
			for i in range(len(self.content_data['data']['items'])):
				self.iv_barcodes.append(next(iv_gen))
				count += 1
		except StopIteration:
			print('Collected {} barcode numbers'.format(count))

	def sortBarcodes(self):
		"""Sorts Intervideo barcode numbers and removes duplicates."""
		return sorted(set(self.iv_barcodes))


