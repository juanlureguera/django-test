import json
import base64
class LoginRequest:

    def __init__(self, userName, password):
        self.userName=userName
        self.password = password

    def toJsonString(self):
        newJson = {}
        newJson['name']=self.userName
        newJson['password']=base64.b64encode(self.password)
        return json.dumps(newJson)

    @staticmethod
    def fromJsonString(jsonString):
        jsonObj = json.load(jsonString)
        password = base64.b64decode(jsonObj["password"])
        request = LoginRequest(jsonObj["name"], password)
        return request
