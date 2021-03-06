# Obscure Api
It is just another rest api library but with the extra feature that I call "obscure". This basically means that you can use a plain HTTP connection (without ssl) but with all contents crypted, so anyone who tries to sniff your communications can't guess anything about your api.

# If ssl can do this, what is the reason of this library?
When you build an api for a mobile phone or game, you cannot control the user device. So even if you are using SSL, the user just have to install a custom certificate and make a MitM to himself and then, all trafic and api methods are exposed.

# What exacly does this library?
Its quite simple. The path, headers and content data are crypted using AES. There is also added a request expire time, so a "valid" request its only valid for a short time. The status code and method are algo crypted in the payload so someone sniffing your communication will always see a response with 200 as status code (and a lot of crypted data). 



#Basic example
The server

```python
from obscure_api import obscure


@obscure.url(name="admin", path="admin")
class Admin(object):
    @obscure.secure()
    @obscure.url(path="index")
    def index(self, request):
        return {"hi": "admin"}


s = obscure.Server(key="123456789qwerty$", jwt_secret="qwertyuiopasdfghjklzxcvbnm123456")

from jose import jwt
token = jwt.encode({'key': 'value'}, 'qwertyuiopasdfghjklzxcvbnm123456', algorithm='HS256')
print("Example auth token:", token)
s.run()

```

The client
```python
import obscure_api.crypto
import requests
import datetime
import json

class HiddenClient(object):

    def __init__(self, cipher, host, request_expirity=10, auth_token=None):
        self.cipher = cipher
        self.request_expirity = request_expirity
        self.host = host
        self.auth_token = auth_token

    def _validity(self, duration):
        headers = {
            "_c": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
            "_d": duration
        }
        if self.auth_token:
            headers["Authorization"] = "Bearer: " + self.auth_token
        return headers

    def get(self, url):
        headers = self._validity(self.request_expirity)

        r = requests.get(self.host + "/" + self.cipher.encrypt(url).decode(), headers={"Headers": self.cipher.encrypt(json.dumps(headers))})
        data = self.cipher.decrypt(r.text)

        r._content = data[3:].encode()
        r.status_code = int(data[:3].encode())

        return r

    def post(self, url, data):
        headers = self._validity(self.request_expirity)
        r = requests.post(self.host + "/" + self.cipher.encrypt(url).decode(),
                          headers={"Headers": self.cipher.encrypt(json.dumps(headers))},
                          data=self.cipher.encrypt(json.dumps(data))
                          )

        data = self.cipher.decrypt(r.text)

        r._content = data[3:].encode()
        r.status_code = int(data[:3].encode())

        return r



c = HiddenClient(obscure_api.crypto.AESCipher("123456789qwerty$"), "http://localhost:4000", auth_token="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJrZXkiOiJ2YWx1ZSJ9.nFkNUmu6iRN2T449AbxPeFm3Bdxx9VRKcKDjiTm0_eY")

r = c.get("/admin/index")
data = r.text
print(r.status_code)
print(data)
```

Or you can check the files server.py and client.py


# TODO
A nice documentation
