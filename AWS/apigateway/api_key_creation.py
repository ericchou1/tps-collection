#!/usr/env/bin python

import boto3
import pprint

boto3.setup_default_session(region_name='us-east-1')
client = boto3.client('apigateway')

# Create Key
response = client.create_api_key(
    name='customer2',
    description='Test Customer 2',
    enabled=True,
    generateDistinctId=True,
)

keyId = response['id']

# Associate with Usage Plan
response = client.create_usage_plan_key(
    usagePlanId='',
    keyId=keyId,
    keyType='API_KEY'
)


