#!/usr/env/bin python

import boto3
import pprint

boto3.setup_default_session(region_name='us-east-1')
client = boto3.client('apigateway')

response = client.get_usage_plan_key(
    usagePlanId='',
    keyId=''
)

pprint.pprint(response)

