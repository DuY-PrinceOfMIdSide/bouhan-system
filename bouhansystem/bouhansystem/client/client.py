import requests
import json
url='http://0.0.0.0:5000/'

data = { "time1":'19:00', "time2":'20:00', "val":'no human'}

print(json.dumps(data))
response = requests.post(url,data=json.dumps(data))
print(response)
