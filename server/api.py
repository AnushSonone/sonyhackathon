import requests

url = "https://0myrzet12k.execute-api.us-east-1.amazonaws.com/prod/devices/Aid-80070001-0000-2000-9002-000000000efe/data?key=202504ut&pj=kyoro"

res = requests.get(url)
print(res.json())
