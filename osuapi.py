import requests as req
from utils import from_json

'''
Adapted from https://github.com/LostPy/osu-api.py, I'm only interested in the get_user function so slimmed everything down around it
'''

base_url ='https://osu.ppy.sh/api'
urls = {
'beatmaps': base_url + '/get_beatmaps?',
'user': base_url + '/get_user?',
'scores': base_url + '/get_scores?',
'user_best': base_url + '/get_user_best?',
'user_recent': base_url + '/get_user_recent?',
'match': base_url + '/get_match?',
'replay': base_url + '/get_replay?'
}

def get_user(key: str, user: int, type_return: str = 'dict', **kwargs):
	"""Retrieve general user information."""
	params = {
	'k': key,
	'u': user,
	'm': kwargs['mode'] if 'mode' in kwargs else 0,
	'type': kwargs['type_'] if 'type_' in kwargs else None,
	'event_days': kwargs['event_days'] if 'event_days' in kwargs else 1}
	r = req.get(urls['user'], params=params)
	return from_json(r.text, type_return)