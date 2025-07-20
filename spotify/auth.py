from urllib.parse import urlencode
import webbrowser
import socket
from base64 import b64encode
import requests
import json
from datetime import datetime, timedelta

# Listens for callback on localhost port 8888
def listenCallback(port):
	sock = socket.socket()
	sock.bind(('', port))
	sock.listen(1)
	conn, address = sock.accept()
	data = conn.recv(1024).decode()
	
	# TODO: Clean up and minimize positional dependencies
	lines = data.splitlines()
	query = lines[0][14:-9]
	if query[:5] != 'code=':
		conn.send('Authorization stage failed. You may close this window.'.encode())
		conn.close()
		sock.close()
		raise Exception('Authorization was not granted')
	conn.send('Authorization stage completed. You may close this window.'.encode())
	conn.close()
	sock.close()
	return query[5:]

# User gives app permission to access playlists
def requestAuthCode(client_id, port):
	params = {
		'client_id': client_id,
		'response_type': 'code',
		'redirect_uri': f'http://localhost:{port}/callback',
		# TODO: Learn about using 'state' to protect against XSRF
		'scope': 'playlist-read-private playlist-read-collaborative playlist-modify-private playlist-modify-public' # Every playlist-related scope
	}

	auth_url = 'https://accounts.spotify.com/authorize?' + urlencode(params)
	webbrowser.open(auth_url)
	return listenCallback(port)

def getBase64AuthString(client_id, client_secret):
	return str(b64encode(f'{client_id}:{client_secret}'.encode('utf-8')), 'utf-8')

def requestAccessToken(b64_auth_string, auth_code, port):
	headers = {
		'Authorization': f'Basic {b64_auth_string}',
		'Content-Type': 'application/x-www-form-urlencoded'
	}
	data = {
		'grant_type': 'authorization_code',
		'code': auth_code,
		'redirect_uri': f'http://localhost:{port}/callback' # Used only for validation on Spotify backend
	}

	resp = requests.post('https://accounts.spotify.com/api/token', data=data, headers=headers)
	if resp.status_code != 200:
		raise Exception(f'Failed to get new access token with status code {resp.status_code}')
	return json.loads(resp.text)

def refreshAccessToken(b64_auth_string, refresh_token):
	headers = {
		'Authorization': f'Basic {b64_auth_string}',
		'Content-Type': 'application/x-www-form-urlencoded'
	}
	data = {
		'grant_type': 'refresh_token',
		'refresh_token': refresh_token
	}

	resp = requests.post('https://accounts.spotify.com/api/token', data=data, headers=headers)
	if resp.status_code != 200:
		raise Exception(f'Failed to refresh access token with status code {resp.status_code}')
	return json.loads(resp.text)

# Spotify will only give you a new refresh token if the current refresh token is expired or does not exist
# If no refresh token is supplied, one must be present in token_info
def simplifyTokenInfo(token_info, refresh_token=None):
	exp_seconds = token_info['expires_in']
	exp_datetime = datetime.now() + timedelta(seconds=exp_seconds)
	return {
		'access_token': token_info['access_token'],
		'expires_datetime': exp_datetime.strftime('%Y-%m-%d %H:%M:%S'),
		'refresh_token': token_info['refresh_token']
	}
