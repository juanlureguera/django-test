import json
from Server.ServerResponse import ServerResponse


class GetDriverNameResponse:

    def __init__(self, name):
        self.name = name

    def toJsonString(self):
        newJson = {}
        newJson['driverName'] = self.name
        return json.dumps(newJson)

    @staticmethod
    def fromJsonString(jsonString):

        jsonObj = json.loads(jsonString)
        request = GetDriverNameResponse(jsonObj["driverName"])
        return request