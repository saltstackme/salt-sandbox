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
import re

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
    headers = rackspace(username, api_key)
    filters = ['ubuntu', 'centos']
    dcs = ['iad','dfw','ord','hkg','syd']
    return create_profiles(dcs, headers, account_id, filters)
    

def rackspace(username, api_key):
    url = 'https://identity.api.rackspacecloud.com/v2.0/tokens'
    payload  = {"auth":{"RAX-KSKEY:apiKeyCredentials":{"username": username , "apiKey": api_key }}}
    headers = {'Content-Type': 'application/json'}
    r = requests.post(url, data=json.dumps(payload), headers=headers)
    token = r.json()['access']['token']['id']
    headers = {'X-Auth-Token' : token}
    return headers

def _get(url, headers, payload=None):
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


def get_images(dc, headers, account_id, filters):
    url = 'https://'+ dc +'.servers.api.rackspacecloud.com/v2/' + str(account_id) + '/images'
    response = _get(url, headers)
    content = response[2]
    images = json.loads(content)['images']
    image_list = []
    for image in images:
        for filter in filters:
            if filter.lower() in image['name'].lower():
                image_list.append(image['name'])
                break
    return image_list


def get_flavors(dc, headers, account_id):
    url = 'https://' + dc + '.servers.api.rackspacecloud.com/v2/' + str(account_id) + '/flavors'
    response = _get(url, headers)
    content = response[2]
    flavors = json.loads(content)['flavors']
    flavor_list = []
    for flavor in flavors:
        flavor_list.append(flavor['name'])
    return flavor_list

def create_profiles(dcs, headers, account_id, filters):
    for dc in dcs:
        flavors = get_flavors(dc, headers, account_id)
        images = get_images(dc, headers, account_id, filters)
        for flavor in flavors:
            for image in images:
                print flavor, image
        print "----"

if __name__ == "__main__":
    init(sys.argv[1], sys.argv[2], sys.argv[3])
