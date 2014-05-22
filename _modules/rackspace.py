'''
salt-cloud configuration creator for Rackspace Cloud
'''

# Import python libs
import logging
import urllib2
import random
import time
import sys
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

def init(username, api_key, account_id):
    headers = connect(username, api_key)
    return get_images(headers, account_id)
    

def connect(username, api_key):
    url = 'https://identity.api.rackspacecloud.com/v2.0/tokens'
    payload  = {"auth":{"RAX-KSKEY:apiKeyCredentials":{"username": username , "apiKey": api_key }}}
    headers = {'Content-Type': 'application/json'}
    r = requests.post(url, data=json.dumps(payload), headers=headers)
    token = r.json()['access']['token']['id']
    headers = {'X-Auth-Token' : token}
    return headers

def get(url, headers, payload=None):
    r = requests.get(url, data=json.dumps(payload), headers=headers)
    return [r.status_code, r.headers, r.content]

def post(url, headers, payload=None):
    r = requests.post(url, data=json.dumps(payload), headers=headers)
    return [r.status_code, r.headers, r.content]

def put(url, headers, payload=None):
    r = requests.put(url, data=json.dumps(payload), headers=headers)
    return [r.status_code, r.headers, r.content]

def delete(url, headers, payload=None):
    r = requests.delete(url, data=json.dumps(payload), headers=headers)
    return [r.status_code, r.headers, r.content]


def get_images(headers, account_id):
    url = 'https://iad.servers.api.rackspacecloud.com/v2/' + str(account_id) + '/flavors'
    return get(url, headers)
    


if __name__ == "__main__":
    init(sys.argv[1], sys.argv[2], sys.argv[3])
