import json

class RegisterDriverRequest:

    def __init__(self, sessionID, bancR, matricula, marca, modelo, anios, km):
        self.sessionID=sessionID
        self.bancR = bancR
        self.matricula = matricula
        self.marca = marca
        self.modelo = modelo
        self.anios = anios
        self.km = km

    def toJsonString(self):
        newJson = {}
        newJson['sessionID']=self.sessionID
        newJson['bancR'] = self.bancR
        newJson['matricula'] = self.matricula
        newJson['marca'] = self.marca
        newJson['modelo'] = self.modelo
        newJson['anios'] = self.anios
        newJson['km'] = self.km
        return json.dumps(newJson)

    @staticmethod
    def fromJsonString(jsonString):
        jsonObj = json.load(jsonString)
        request = RegisterDriverRequest(jsonObj["bancR"], jsonObj["matricula"], jsonObj["marca"], jsonObj["modelo"], jsonObj["anios"], jsonObj["km"])

        return request