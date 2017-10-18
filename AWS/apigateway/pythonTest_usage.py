import requests, json

url = "https://api.a10threatprotection.net/v1/tps/incidents"

auth_header = {'content-type': 'application/json', 'x-api-key': ''}

data = {
  "eric": "chou-test-usage",
  "acos-time": "2017-10-06T23:47:04.771963",
  "attack-type": "Unknown",
}

for i in range(10):
    r = requests.post(url, data=json.dumps(data), headers=auth_header)
    print(str(r.status_code) + " " + r.content)


