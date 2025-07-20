import requests
import json

class User:
	# *args passed to callback function to refresh token; I use this to specify the file to write the token information to
	def __init__(self, market, token, refreshCallback, b64_auth_string, refresh_token, *args):
		self.market = market # Overall application I am trying to build may not be possible without market distinction
		self.headers = {
			'Authorization': f'Bearer {token}',
			'Content-Type': 'application/json'
		}

		# Refresh token via callback for modularization
		# Callback must return a JSON with at least 'access_token' and 'refresh_token'
		self.refreshCallback = refreshCallback
		self.b64_auth_string = b64_auth_string
		self.refresh_token = refresh_token
		self.refresh_args = args

	def refreshToken(self):
		token_info = self.refreshCallback(self.b64_auth_string, self.refresh_token, *self.refresh_args)
		token = token_info['access_token']
		self.headers['Authorization'] = f'Bearer {token}'
		self.refresh_token = token_info['refresh_token']

	# Wrapper function to avoid repeating URL
	def getEndpoint(self, endpoint, params):
		url = 'https://api.spotify.com/v1' + endpoint
		return self.getUrl(url, params=params)

	def getUrl(self, url, params=None, refreshed_token=False):
		resp = requests.get(url, params=params, headers=self.headers)	
		if resp.status_code != 200:
			if refreshed_token:
				# Throws exception if request fails again after refreshing expired token
				raise Exception(f'Failed to get {resp.request.url} with status code {resp.status_code} after refreshing token')
			if resp.status_code == 401:
				self.refreshToken() # Calls back to user program
				return self.getUrl(url, params=params, refreshed_token=True) # Trying to avoid infinite recursion
			raise Exception(f'Failed to get {resp.request.url} with status code {resp.status_code}')
		return json.loads(resp.text)

	# For multi-paged responses in which the 'items' key is used, this returns a list of all items
	# resp -- initial response after making endpoint request
	# initial_key -- key in root of JSON response through which 'items' key can be accessed
	def getPageItems(self, resp, initial_key = None):
		items = []
		while (True):
			if initial_key is not None:
				resp = resp[initial_key]
			items.extend(resp['items'])
			next_page = resp['next']
			if next_page is None:
				break
			resp = self.getUrl(next_page)
		return items

	# Gets Spotify category tags
	def getCategories(self):
		# TODO: Allow locale parameter for other languages
		endpoint = '/browse/categories/'
		params = { 'limit': 50 }
		resp = self.getEndpoint(endpoint, params=params)
		return self.getPageItems(resp, initial_key='categories')

	# Get Spotify playlists associated with category tag
	def getCategoryPlaylists(self, category_id):
		endpoint = f'/browse/categories/{category_id}/playlists'
		params = { 'limit': 50 }
		resp = self.getEndpoint(endpoint, params=params)
		return self.getPageItems(resp, initial_key='playlists')
