import json
class ProfileResponse:

    def __init__(self, loginName, passw, name, email, bornDate, dni, cuentaBancaria, puntuation):
        self.loginName = loginName
        self.passw = passw
        self.name = name
        self.email = email
        self.bornDate = bornDate
        self.dni = dni
        self.cuentaBancaria = cuentaBancaria
        self.puntuation = puntuation

    def toJsonString(self):
        newJson = {}
        newJson['loginName'] = self.loginName
        newJson['pass'] = self.passw
        newJson['name'] = self.name
        newJson['email'] = self.email
        newJson['bornDate'] = self.bornDate
        newJson['dni'] = self.dni
        newJson['cuentaBancaria'] = self.cuentaBancaria
        newJson['puntuation'] = self.puntuation
        return json.dumps(newJson)

    @staticmethod
    def fromJsonString(jsonString):
        jsonObj = json.loads(jsonString)
        request = ProfileResponse(  jsonObj["loginName"], jsonObj["pass"], jsonObj["name"], jsonObj["email"], 
                                    jsonObj["bornDate"], jsonObj["dni"], jsonObj["cuentaBancaria"], jsonObj["puntuation"])
        return request
