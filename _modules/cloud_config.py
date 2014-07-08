'''
Creates salt-cloud configuration files for cloud vendors

To run manually
python cloud_config.py  "prefix" "username" "api key" "account id" "ubuntu,centos"
'''

# Import python libs
import logging

import sys
import requests
import json
import yaml
import os
import errno
import socket

log = logging.getLogger(__name__)

def _get(url, headers, payload=None):
    r = requests.get(url, data=json.dumps(payload), headers=headers)
    return {'status_code': r.status_code, 'headers': r.headers, 'content': r.content}


def _post(url, headers, payload=None):
    r = requests.post(url, data=json.dumps(payload), headers=headers)
    return {'status_code': r.status_code, 'headers': r.headers, 'content': r.content}


def _put(url, headers, payload=None):
    r = requests.put(url, data=json.dumps(payload), headers=headers)
    return {'status_code': r.status_code, 'headers': r.headers, 'content': r.content}


def _delete(url, headers, payload=None):
    r = requests.delete(url, data=json.dumps(payload), headers=headers)
    return {'status_code': r.status_code, 'headers': r.headers, 'content': r.content}


def init(prefix, username, api_key, account_id, match=None):
    rackspace(prefix, username, api_key, account_id, match)
    

def rackspace(prefix, username, api_key, account_id, match=None):
    '''
    Creates cloud profiles and providers for salt.
    '''
    auth = _rax_auth(username, api_key)
    token = auth['token']

    if match:
        match = match.split(",")

    dcs = auth['regions']

    log.info("Creatig profiles")
    profiles = _rax_create_profiles(prefix, dcs, token, account_id, match)
    log.info("Profiles are created")
    log.info("Creating providers")
    providers = _rax_create_providers(prefix, "salt_master", dcs, username, api_key, account_id)
    log.info("Profiles are created")
    return {"providers": providers, "profiles": profiles}


def _rax_auth(username, api_key):
    '''
    Get authentication token from Rackspace identity service
    '''
    log.info("Getting Rackspace authentication token")
    url = 'https://identity.api.rackspacecloud.com/v2.0/tokens'
    payload  = {"auth":{"RAX-KSKEY:apiKeyCredentials":{"username": username , "apiKey": api_key }}}
    headers = {'Content-Type': 'application/json'}
    r = requests.post(url, data=json.dumps(payload), headers=headers)
    rdic = json.loads(r.content)
    token = rdic['access']['token']['id']
    regions = [str(r['region'].lower()) for r in [service['endpoints'] for service in rdic['access']['serviceCatalog'] if service['name'] == "cloudServersOpenStack"][0]]
    return {'token': token, 'regions': regions}


def _rax_get_images(dc, token, account_id, match):
    '''
    Get all available images in given data center
    '''
    url = 'https://'+ dc +'.servers.api.rackspacecloud.com/v2/' + str(account_id) + '/images'
    headers = {'X-Auth-Token' : token}
    response = _get(url, headers)
    content = response['content']
    images = json.loads(content)['images']
    image_list = []
    for image in images:
        for m in match:
            if m.lower() in image['name'].lower():
                image_list.append(image['name'])
                break
    return image_list


def _rax_get_flavors(dc, token, account_id):
    '''
    Get all flavors in given data center
    '''
    url = 'https://' + dc + '.servers.api.rackspacecloud.com/v2/' + str(account_id) + '/flavors'
    headers = {'X-Auth-Token' : token}
    response = _get(url, headers)
    content = response['content']
    flavors = json.loads(content)['flavors']
    flavor_list = []
    for flavor in flavors:
        flavor_list.append(flavor['name'])
    return flavor_list

def getPublicIp():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('google.com', 0))
    return s.getsockname()[0]

def _rax_create_providers(prefix, salt_master, dcs, username, api_key, account_id):
    '''
    Create provider configuration files under /etc/salt/cloud.providers.d
    '''
    try:
        os.makedirs("/etc/salt/cloud.providers.d")
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise
    providers = []
    for dc in dcs:
        provider = {}
        name = prefix + '-'+ dc
        ip_address = getPublicIp()
        master = {'master': ip_address}
        provider[name] = {
            "apikey": api_key, 
            "protocol": "ipv4", 
            "minion": master , 
            "compute_name": "cloudServersOpenStack", 
            "user": username, 
            "provider": "openstack", 
            "compute_region": dc.upper(), 
            "identity_url": "https://identity.api.rackspacecloud.com/v2.0/tokens", 
            "tenant": account_id
        }
        stream = file('/etc/salt/cloud.providers.d/' + name + '.conf', 'w')
        providers.append('/etc/salt/cloud.providers.d/' + name + '.conf')
        yaml.dump(provider, stream, default_flow_style=False)
    return providers


def _rax_create_profiles(prefix, dcs, token, account_id, match):
    '''
    Create profiles configuration files under /etc/salt/cloud.profiles.d
    '''
    try:
        os.makedirs("/etc/salt/cloud.profiles.d")
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise
    profiles = []
    for dc in dcs:
        flavors = _rax_get_flavors(dc, token, account_id)
        images = _rax_get_images(dc, token, account_id, match)
        profile = {}
        for flavor in flavors:
            for image in images:
                name = prefix + "-" + dc + "-" + flavor.replace(" ", "-") + "-" + image.replace(" ", "-") 
                profile[str(name)] = {
                    "provider": str(prefix) + "-" + dc,
                    "size": str(flavor),
                    "image": str(image)
                }
        stream = file('/etc/salt/cloud.profiles.d/' + prefix + "-" + dc + '.conf', 'w')
        profiles.append('/etc/salt/cloud.profiles.d/' + prefix + "-" + dc + '.conf')
        yaml.dump(profile, stream, default_flow_style=False)
    return profiles
                

if __name__ == "__main__":
    '''
    for testing puroses
    so we can call the cloud_config.py from
    command line
    '''
    init(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
