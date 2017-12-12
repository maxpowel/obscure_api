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

