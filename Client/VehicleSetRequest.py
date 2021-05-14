import json
class VehicleSetRequest:

    def __init__(self, sessionID, matricula, marca, modelo, km, anios):
        self.sessionID = sessionID
        self.matricula = matricula
        self.marca = marca
        self.modelo = modelo
        self.km = km
        self.anios = anios

    def toJsonString(self):
        newJson = {}
        newJson['sessionID'] = self.sessionID
        newJson['matricula'] = self.matricula
        newJson['marca'] = self.marca
        newJson['modelo'] = self.modelo
        newJson['km'] = self.km
        newJson['anios'] = self.anios
        return json.dumps(newJson)

    @staticmethod
    def fromJsonString(jsonString):
        jsonObj = json.loads(jsonString)
        request = VehicleSetRequest(  jsonObj["sessionID"], jsonObj["matricula"], jsonObj["marca"],
                                    jsonObj["modelo"], jsonObj["km"], jsonObj["anios"])
        return request
