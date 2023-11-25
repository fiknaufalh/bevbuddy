import requests
import json

url = "http://bevbuddy.up.railway.app/"
payload = {
    "username": "fiknaufalh", 
    "password": "fiknaufalh"
}
headers = {
    "Content-Type": "application/json",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36"
}

# payload = json.dumps(payload)
# response = requests.post(f"{url}/login", json=payload, headers=headers)
# print(response.status_code)
# print(response.json())

response = requests.get(f"{url}/menus", headers=headers)
print(response.status_code)
print(response.json())