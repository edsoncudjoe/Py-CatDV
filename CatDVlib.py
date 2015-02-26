import requests
import json

class Cdvlib(object):

	def __init__(self):

		pass
		self.url = 'http://192.168.0.101:8080/api/4' # For Intervideo Local Testing
		self.iv_barcodes = []
	#Generic methods
	def getUrl(self):

		url_input = raw_input('Enter URL of the CatDV Sever (eg. \'localhost:8080\'): ')
		self.url = url_input + '/api/4'
		return self.url

	def getAuth(self):

		usr = raw_input('Enter username: ')
		pwd = raw_input('Enter password: ')
		self.auth = self.url + "/session?usr=" + usr + "&pwd=" + pwd
		return self.auth

	def getSessionKey(self):

		try:
			response = requests.get(self.auth)
			keydata = json.loads(response.text)
			self.key = keydata['data']['jsessionid']
			return self.key
		except:
			raise ValueError('Unable to retrieve data.')

	def getCatalogName(self):

		catalogs = requests.get(self.url + "/catalogs;jsessionid=" + str(self.key))
		catalog_data = json.loads(catalogs.text)
		#self.catalog_names = [(i['groupName'], i['ID']) for i in catalog_data['data'] if i['ID'] > 1]
		self.catalog_names = []
		for i in catalog_data['data']:
			if i['ID'] > 1:
				self.catalog_names.append((i['groupName'], i['ID']))
		return self.catalog_names

	def getCatalogClips(self, catalog_id):
		"""Requests all clips from the client catalog. Filtered by catalog ID."""
		content_raw = requests.get(
			self.url + '/clips;jsessionid=' + self.key + '?filter=and((catalog.id)eq({}))'
			'&include=userFields'.format(catalog_id))
		self.content_data = json.loads(content_raw.text)
		return self.content_data


		
	def setCatalogID(self): # NOT IN USE
		pass
		#self.getCatalogClips(self.catalog_names[0][1]) # Classic Media

	def deleteSession(self):
		return requests.delete(self.url + '/session')

	#Intervideo Specific
	def getIVNumbers(self, data): # Generator.
		
		count = 0
		try:
			for i in data['data']['items']:
				if 'userFields' in i.keys():
					if 'U7' in i['userFields']:
						count += 1
						yield i['userFields']['U7']
		except:
			print('Possible Error at position {}'.format(count))

	def collectIVNumbers(self):

		try:
			iv_gen = self.getIVNumbers(self.content_data)
			count = 0
			for i in range(len(self.content_data['data']['items'])):
				self.iv_barcodes.append(next(iv_gen))
				count += 1
		except StopIteration:
			print('Collected {} barcode numbers'.format(count))

	def sortBarcodes(self):
		return sorted(set(self.iv_barcodes))

try:
	a = Cdvlib()
	#a.getUrl()
	a.getAuth()
	a.getSessionKey()

	a.getCatalogName()
	a.getCatalogClips(a.catalog_names[0][1]) 
	a.collectIVNumbers()
	a.sortBarcodes()
except ValueError:
	print('There was a server error. Please try again in a few moments.')
finally:
	a.deleteSession()


