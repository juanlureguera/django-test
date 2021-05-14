import json
from Server.ServerResponse import ServerResponse


class RouteGetDetails:

    def __init__(self, session, idR):
        self.session = session
        self.idR= idR

    def toJsonString(self):
        newJson = {}
        newJson['session'] = self.session
        newJson['id'] = self.idR
        return json.dumps(newJson)

    @staticmethod
    def fromJsonString(jsonString):
        jsonObj = json.loads(jsonString)
        request = ServerResponse(jsonObj["session"], jsonObj["id"])
        return request