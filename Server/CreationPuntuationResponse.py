import json
import base64
class CreationPuntuationResponse:

    def __init__(self, sessionID, id, puntuation):
        self.sessionID = sessionID
        self.id=id
        self.puntuation = puntuation

    def toJsonString(self):
        newJson = {}
        newJson['sessionID'] = self.sessionID
        newJson['id']=self.id
        newJson['puntuation'] = self.puntuation

        return json.dumps(newJson)

    @staticmethod
    def fromJsonString(jsonString):
        jsonObj = json.load(jsonString)

        request = CreationPuntuationResponse(jsonObj["sessionID"], jsonObj["id"], jsonObj["puntuation"])
        return request
