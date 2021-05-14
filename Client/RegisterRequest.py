import json
import base64
class RegisterRequest:

    def __init__(self, usrnameR, pswR, nameR, borndateR, dniR, bancR, emailR):
        self.usrnameR=usrnameR
        self.pswR = pswR
        self.nameR = nameR
        self.borndateR = borndateR
        self.dniR = dniR
        self.bancR = bancR
        self.emailR = emailR

    def toJsonString(self):
        newJson = {}
        newJson['loginName']=self.usrnameR
        encoded = base64.b64encode(self.pswR)
        print "pass encode"
        print base64.b64encode(self.pswR)
        newJson['pass'] = encoded
        newJson['name'] = self.nameR
        newJson['bornDate'] = self.borndateR
        newJson['dni'] = self.dniR
        newJson['cuentaBancaria'] = self.bancR
        newJson['email'] = self.emailR
        return json.dumps(newJson)

    @staticmethod
    def fromJsonString(jsonString):
        jsonObj = json.load(jsonString)
        password = base64.b64decode(jsonObj["pswR"])
        request = RegisterRequest(jsonObj["loginName"], password, jsonObj["name"], jsonObj["bornDate"], jsonObj["dni"], jsonObj["cuentaBancaria"], jsonObj["emailR"])
        return request
