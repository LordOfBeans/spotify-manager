from auth import Auth

import requests
import json
import os
import yaml

class User:
    def __init__(self, CONFIG_FILE):
        if not os.path.exists(CONFIG_FILE):
            raise FileNotFoundError(f'Spotify configuration file {CONFIG_FILE} does not exist')
        with open(CONFIG_FILE, 'r') as f:
            self.config = yaml.load(f)
        self.auth = Auth (
            self.config['client_id'],
            self.config['client_secret'],
            self.config['callback_port'],
            self.config['token_path']
        )

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
            resp = self.auth.getUrl(next_page)
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
