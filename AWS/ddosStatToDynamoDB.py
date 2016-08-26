#!/usr/env/bin python

# ericc@a10networks.com

import boto3, pprint
import requests, json, datetime

# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)


# Basic infomation
hosts = ['192.168.199.152', '192.168.199.151']

# DynamoDB definition
# Table is already crated via console. The hash key is device serial number
# sorting key is the Timestamp in ISO 8601 UTC
dynamodb = boto3.resource('dynamodb', endpoint_url="https://dynamodb.<region>.com")
table = dynamodb.Table("<table name>")

try:
    for host in hosts:
        base_url = 'https://'+host
        # Acquire athorization token
        auth_headers = {'content-type': 'application/json'}
        auth_payload = {"credentials": {"username": "admin", "password": "a10"}}
        auth_endpoint = '/axapi/v3/auth'
        url = base_url + auth_endpoint
        r = requests.post(url, data=json.dumps(auth_payload), headers=auth_headers, verify=False)
        signature =  r.json()['authresponse']['signature']

        common_headers = {'Content-type' : 'application/json', 'Authorization' : 'A10 {}'.format(signature)}


        # serial number of device
        version_endpoint = '/axapi/v3/version/oper'
        url = base_url + version_endpoint
        r = requests.get(url, headers=common_headers, verify=False)
        serialNumber =  r.json()['version']['oper']['serial-number']

        timeInUTC = datetime.datetime.utcnow().isoformat()

        Item = {"SerialNumber": serialNumber, "Time": timeInUTC}

        version_endpoint = '/axapi/v3/ddos/brief/stats'
        url = base_url + version_endpoint
        r = requests.get(url, headers=common_headers, verify=False)
        stats = r.json()['brief']['stats']
        for key, value in stats.items():
            Item[key] = value


        # Log off
        logoff_endpoing = '/axapi/v3/logoff'
        url = base_url + logoff_endpoing
        r = requests.post(url, headers=common_headers, verify=False)

        #pprint.pprint(Item)
        #dump to DynamoDB
        response = table.put_item(Item=Item)
        #print(json.dumps(response, indent=4, cls=DecimalEncoder))

except Exception as e:
    print("Error: " + str(e))

