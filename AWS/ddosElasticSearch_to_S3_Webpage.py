import requests, pprint, json
import boto3, pygal
import time

base_es = '<your instance>.es.amazonaws.com/'

# GET Request
response = requests.get(base_es+'a10_colocation_stat_brief/_search?q=SerialNumber:TH30A53313370032&pretty')

#print(response.json()['hits']['hits'])
for i in response.json()['hits']['hits']:
    pprint.pprint(i['_source']['SerialNumber'])
    pprint.pprint(i['_source']['Time'])

# POST Request
headers = {'Content-Type': 'application/json'}
post_body = {
    "query": {
        "range": {
            "@timestamp": {
                "gte": "2016-09-09T04:00:00",
                "lt": "2016-09-09T07:00:00"
            }
        }
    }
}

# Start to construct graph
line_chart = pygal.Line()
line_chart.title = "TPS4435 TH44113014060008 Elastic Search Test"

graphTime=[]
dst_egress_packets=[]
dst_egress_bytes=[]
dst_ingress_packets=[]
dst_ingress_bytes=[]

response = requests.post(base_es+'a10_colocation_stat_brief/_search?q=SerialNumber:TH44113014060008&pretty', headers=headers, data=json.dumps(post_body))
for i in response.json()['hits']['hits']:
    dst_egress_packets.append(i['_source']['dst_egress_packets'])
    dst_ingress_packets.append(i['_source']['dst_ingress_packets'])
    graphTime.append(i['_source']['Time'])
    dst_egress_bytes.append(i['_source']['dst_egress_bytes'])
    dst_ingress_bytes.append(i['_source']['dst_ingress_bytes'])

print("number of datapoints: " + str(len(graphTime)))
line_chart.x_labels = map(str, graphTime)
line_chart.add("dst_egress_packets", dst_egress_packets)
line_chart.add("dst_ingress_packets", dst_ingress_packets)
line_chart.add("dst_egress_bytes", dst_egress_bytes)
line_chart.add("dst_ingress_bytes", dst_ingress_bytes)
#line_chart.render_in_browser()
#line_chart.render_to_file('TPS4435_Graph1.svg')
line_chart.render_to_file('TPS4435_Graph2.html')

# Upload to S3 bucket
s3 = boto3.resource('s3')
data2 = open('TPS4435_Graph2.html', 'r')
s3.Bucket('a10-thunder-tps-stats').put_object(Key='TPS4435_Graph2.html', Body=data2, ContentType='html')

