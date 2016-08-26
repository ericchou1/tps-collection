#!/usr/env/bin python

from __future__ import print_function # Python 2/3 compatibility
import boto3
import json
import decimal
from boto3.dynamodb.conditions import Key, Attr
import pygal
from collections import OrderedDict

# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)


dynamodb = boto3.resource('dynamodb', endpoint_url="https://dynamodb.<region>.amazonaws.com")

table = dynamodb.Table('<table name>')

# In this table, primary key is the device serial number, sorting key is the Time in UTC ISO 8601 format
response = table.query(
        KeyConditionExpression=Key('SerialNumber').eq('<device serial number>') & Key('Time').between('2016-08-26T05:00', '2016-08-26T05:10')
)

# Start to construct graph
line_chart = pygal.Line()
line_chart.title = "TPS4435"

time=[]
dst_egress_packets=[]
dst_egress_bytes=[]
dst_ingress_packets=[]
dst_ingress_bytes=[]

for i in response['Items']:
    dst_egress_packets.append(i['dst_egress_packets'])
    dst_ingress_packets.append(i['dst_ingress_packets'])
    time.append(i['Time'])
    dst_egress_bytes.append(i['dst_egress_bytes'])
    dst_ingress_bytes.append(i['dst_ingress_bytes'])

print("number of datapoints: " + str(len(time)))
line_chart.x_labels = map(str, time)
line_chart.add("dst_egress_packets", dst_egress_packets)
line_chart.add("dst_ingress_packets", dst_ingress_packets)
line_chart.add("dst_egress_bytes", dst_egress_bytes)
line_chart.add("dst_ingress_bytes", dst_ingress_bytes)
#line_chart.render_in_browser()
#line_chart.render_to_file('TPS4435_Graph1.svg')
line_chart.render_to_file('TPS4435_Graph1.html')

# Upload to S3 bucket
s3 = boto3.resource('s3')
data2 = open('TPS4435_Graph1.html', 'r')
s3.Bucket('a10-thunder-tps-stats').put_object(Key='TPS4435_Graph1.html', Body=data2, ContentType='html')


