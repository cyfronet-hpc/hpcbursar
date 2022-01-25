import requests
import pprint
import pymunge


with pymunge.MungeContext() as ctx:
    cred = ctx.encode(b"some other dsfsdf d fsdf sdfsd fsd f")
url = "http://127.0.0.1:8000/grant"
headers = {'hbtoken': cred}
r = requests.get(url, headers=headers)
pprint.pprint(r.text)
