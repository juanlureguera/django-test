import json
from Server.ServerResponse import ServerResponse


class GetBeneficieResponse:

    def __init__(self, benefice):
        self.benefice = benefice

    def toJsonString(self):
        newJson = {}
        newJson['benefice'] = self.benefice
        return json.dumps(newJson)

    @staticmethod
    def fromJsonString(jsonString):
        jsonObj = json.loads(jsonString)
        request = GetBeneficieResponse(jsonObj["benefice"])
        return request