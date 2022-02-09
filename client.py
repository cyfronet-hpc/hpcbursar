import requests
import pprint
import pymunge

with pymunge.MungeContext() as ctx:
    cred = ctx.encode(b"plgmattpokora")
url = "http://127.0.0.1:8000/api/v1/user/user_grants_info/plgmattpokora"
headers = {'hbtoken': cred}
r = requests.get(url, headers=headers)
pprint.pprint(r.text)
