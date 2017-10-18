import requests, json

url = "https://someing.execute-api.us-east-1.amazonaws.com/path"

auth_header = {'content-type': 'application/json', 'x-api-key': ''}

data = {
  "acos-time": "2017-10-06T23:47:04.771963",
  "attack-type": "Unknown",
  "auto_detected": "1",
}

r = requests.post(url, data=json.dumps(data), headers=auth_header)
print(str(r.status_code) + " " + r.content)


