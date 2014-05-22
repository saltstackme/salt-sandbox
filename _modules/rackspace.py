'''
salt-cloud configuration creator for Rackspace Cloud
'''

# Import python libs
import logging
import urllib2
import random
import time

import requests
import json

log = logging.getLogger(__name__)

def test():
    return "hello world"

'''
class Connection(object):

    def __init__(self, username, api_key):
        url = 'https://identity.api.rackspacecloud.com/v2.0/tokens'
        payload  = {"auth":{"RAX-KSKEY:apiKeyCredentials":{"username": username , "apiKey": api_key }}}
        headers = {'Content-Type': 'application/json'}
        r = requests.post(url, data=json.dumps(payload), headers=headers)
        self.token = r.json()['access']['token']['id']
        self.headers = {'X-Auth-Token' : self.token, 'Content-Type': 'application/json', 'Client-ID': 'QClient1'}

    def token(self):
        return self.token

def init(username, api_key, account_id=None):
    con = Connection(username, api_key)
    token = con.token()
    return token
'''

def init(username, api_key):
    url = 'https://identity.api.rackspacecloud.com/v2.0/tokens'
    payload  = {"auth":{"RAX-KSKEY:apiKeyCredentials":{"username": username , "apiKey": api_key }}}
    headers = {'Content-Type': 'application/json'}
    r = requests.post(url, data=json.dumps(payload), headers=headers)
    token = r.json()['access']['token']['id']
    headers = {'X-Auth-Token' : token, 'Content-Type': 'application/json', 'Client-ID': 'QClient1'}
    return token
    


