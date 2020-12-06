# Copyright © <2019-2020> Varga Consulting, Toronto, ON info@vargaconsulting.ca
import base64
import requests
import platform
from ..auth.rights import access_token

__url__ = "https://api.h5cluster.ca/cluster/"
__base_headers__ = {
    'Content-Type': 'application/json',
    'User-Agent': 'Python/{}'.format(platform.python_version())
    }

def post(fn, data={}, auth_token='', timeout = 300.0):
    auth = {'Authorization': 'Bearer {}'.format(access_token())}
    headers = {**__base_headers__, **auth}
    return requests.post(url=__url__ + fn, json=data, headers=headers, timeout=timeout)


def get(self, url, params=None, headers=None):
    pass

def create(args):
    r = post('create', args)
    return r.json()