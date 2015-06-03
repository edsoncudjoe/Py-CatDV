import requests
import json
import getpass

class Catdvlib(object):
	"""
	A python wrapper for the CatDV Server REST API service

	"""

	def __init__(self):
		self.url = 'http://192.168.0.101:8080/api/4' # For Local Testing
		self.iv_barcodes = []

	#Generic methods
	def set_url(self):
		"""
		Stores the location of the CatDV server. 
		The user only needs to enter the server domain eg: 'google.com'
		"""
		url_input = raw_input(
			'Enter address of the CatDV Sever (eg. \'localhost:8080\'): ')
		self.url = 'http://' + url_input + '/api/4'
		return self.url

	def set_auth(self, username, password):
		"""Api request with given login info"""
		self.auth = self.url + "/session?usr=" + username + "&pwd=" + password
		return self.auth
	
	def get_auth(self):
		"""Enables the user to login to their CatDV database."""
		print('\nEnter login details for CatDV: ')
		usr = raw_input('Enter username: ')
		pwd = getpass.getpass('Enter password: ')
		self.set_auth(usr, pwd)
		return
		#self.auth = self.url + "/session?usr=" + usr + "&pwd=" + pwd
		#return self.
	
	def get_rsa(self):
		full_key = self.url + '/session/key'
		try:
			full_rsa = requests.get(full_key)
			rsa_data = json.loads(full_rsa.text)
		except:
			raise Exception
		return rsa_data

 	def get_session_key(self):
		"""
		Extracts the session key from login to be used for future API calls.
		"""
		connect_timeout = 0.1
		try:
			response = requests.get(self.auth, 
				timeout=(connect_timeout, 60.0))
			self.status = response.status_code
			keydata = json.loads(response.text)
			self.key = keydata['data']['jsessionid']
			return self.key
		except requests.exceptions.ConnectTimeout as e:
			raise e
			print "The server connection timed-out."
		except requests.exceptions.ConnectionError as e:
			raise e
			print('\nCan\'t access the API.'
				' Please check you have the right domain address')
		except Exception, e:
			print(e)

	def get_catalog_name(self):
		"""Call to get information on all available catalogs."""
		catalogs = requests.get(self.url + "/catalogs;jsessionid="
			+ str(self.key))
		catalog_data = json.loads(catalogs.text)
		self.catalog_names = []
		for i in catalog_data['data']:
			if i['ID'] > 1:
				self.catalog_names.append((i['groupName'], i['ID']))
		return self.catalog_names

	def get_catalog_clips(self, catalog_id):
		"""
		Requests all clips from a client catalog. Filtered by catalog ID.
		"""
		content_raw = requests.get(
			self.url + '/clips;jsessionid=' + self.key + \
			'?filter=and((catalog.id)eq({}))&include=userFields'\
			.format(catalog_id))
		self.content_data = json.loads(content_raw.text)
		return self.content_data

	def clip_search(self):
		"""Returns all clips that match the given search term"""
		entry = raw_input('Enter clip title: ')
		result = requests.get(
			self.url + '/clips;jsessionid=' + self.key + \
			'?filter=and((clip.name)has({}))&include=userFields'\
			.format(entry))
		jdata = json.loads(result.text)
		return jdata['data']['items']

	def clip_id_search(self):
		"""
		Retrieves all data for a clip specified by the unique ID.
		Returns JSON data.
		"""
		clip_id = raw_input('Enter Clip ID \'eg: 480CADB5\': ')
		clip = requests.get(
			self.url + '/clips;jsessionid=' + self.key + \
			'?filter=and((clip.clipref)has({}))'.format(clip_id))
		clip_info = json.loads(clip.text)
		return clip_info['data']['items']

	def delete_session(self):
		"""HTTP delete call to the API"""
		return requests.delete(self.url + '/session')

	#Intervideo Specific
	def iv_clip_search(self): # For Intervideo
		"""Returns all clips that match the given search term"""
		entry = raw_input('Enter clip title: ')
		result = requests.get(
			self.url + '/clips;jsessionid=' + self.key
			+ '?filter=and((clip.name)'
				'has({}))&include=userFields'.format(entry))
		jdata = json.loads(result.text)
		for i in jdata['data']['items']:
			if i['userFields']['U7']:        
				print i['userFields']['U7'], i['name'], i['ID']
			else:
				print i['name'], i['ID']

	def get_iv_numbers(self, data): # Generator.
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

	def collect_iv_numbers(self):
		"""Collects Intervideo barcodes into a list."""
		try:
			iv_gen = self.get_iv_umbers(self.content_data)
			count = 0
			for i in range(len(self.content_data['data']['items'])):
				self.iv_barcodes.append(next(iv_gen))
				count += 1
		except StopIteration:
			print('Collected {} barcode numbers'.format(count))

	def sort_barcodes(self):
		"""Sorts Intervideo barcode numbers and removes duplicates."""
		return sorted(set(self.iv_barcodes))

if __name__ == '__main__':
	user = Catdvlib()
	try:
		user.get_auth()
		user.get_session_key()
		long_key = user.get_rsa()
	except Exception, e:
		print(e)
	finally:
		user.delete_session()

