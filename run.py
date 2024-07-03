import requests
import json

response = requests.get("https://ipapi.com/")
json_data = json.dumps(response.text)
print("json", json_data)