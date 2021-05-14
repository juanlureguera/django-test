import json
import base64
class ProfileSetRequest:

    def __init__(self, sessionId, name, dni, email, banc, passw, newPass, bornDate):
        self.sessionId = sessionId
        self.passw = passw
        self.newPass = newPass
        self.name = name
        self.bornDate = bornDate
        self.dni = dni
        self.banc = banc
        self.email = email

    def toJsonString(self):
        newJson = {}
        newJson['sessionId'] = self.sessionId
        newJson['name'] = self.name
        encoded = base64.b64encode(self.passw)
        newJson['pass'] = encoded
        encoded = base64.b64encode(self.newPass)
        newJson['newPass'] = encoded
        newJson['dni'] = self.dni
        newJson['bornDate'] = self.bornDate
        newJson['cuentaBancaria'] = self.banc
        newJson['email'] = self.email
        return json.dumps(newJson)

    @staticmethod
    def fromJsonString(jsonString):
        jsonObj = json.loads(jsonString)
        password = base64.b64decode(jsonObj["passw"])
        newPass = base64.b64decode(jsonObj["newPass"])
        request = ProfileSetRequest(jsonObj["sessionId"], jsonObj["name"], jsonObj["dni"], jsonObj["email"], jsonObj["cuentaBancaria"],
                                    password, newPass, jsonObj["bornDate"])
        return request
