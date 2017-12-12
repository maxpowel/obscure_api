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

