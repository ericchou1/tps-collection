#!/usr/bin/python

import pprint, sys
import requests, json, datetime

# The credential file is separated out for security
# You can also do 'chmod 400 credentials.json' 

with open('<full path to file>/credentials.json', 'r') as f:
    creds = json.loads(f.read())
    username = creds['username']
    password = creds['password']

# hosts and vertual server name
hosts = [sys.argv[1]]
virtualServerName = sys.argv[2]

try:
    for host in hosts:
        base_url = 'https://'+host
        # Acquire athorization token
        auth_headers = {'content-type': 'application/json'}
        auth_payload = {"credentials": {"username": username, "password": password}}
        auth_endpoint = '/axapi/v3/auth'
        url = base_url + auth_endpoint
        r = requests.post(url, data=json.dumps(auth_payload), headers=auth_headers, verify=False)
        signature =  r.json()['authresponse']['signature']

        common_headers = {'Content-type' : 'application/json', 'Authorization' : 'A10 {}'.format(signature)}


        stat_endpoint = '/axapi/v3/slb/virtual-server/'+ virtualServerName + '/stats/'
        url = base_url + stat_endpoint
        r = requests.get(url, headers=common_headers, verify=False)

        for i in r.json()['virtual-server']['port-list']:
            for key,value in i['stats'].items():
                if key == 'total_l7_conn':
                    print(value)

        # Log off
        logoff_endpoing = '/axapi/v3/logoff'
        url = base_url + logoff_endpoing
        r = requests.post(url, headers=common_headers, verify=False)

except Exception as e:
    print("Error: " + str(e))


