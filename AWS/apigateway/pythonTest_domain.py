import requests, json

url = "https://a10-domain"

auth_header = {'content-type': 'application/json', 'x-api-key': ''}

data = {
  "incident-name": "auto_test_81"
}

r = requests.post(url, data=json.dumps(data), headers=auth_header)
print(str(r.status_code) + " " + r.content)


