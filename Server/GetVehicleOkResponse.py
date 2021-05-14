import json
from Server.ServerResponse import ServerResponse


class GetVehicleOkResponse:

    def __init__(self, ok):
        self.ok = ok

    def toJsonString(self):
        newJson = {}
        newJson['ok'] = self.ok
        return json.dumps(newJson)

    @staticmethod
    def fromJsonString(jsonString):
        jsonObj = json.loads(jsonString)
        request = GetVehicleOkResponse(jsonObj["ok"])
        return request