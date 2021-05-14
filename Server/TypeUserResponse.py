import json

from Server.ServerResponse import ServerResponse


class TypeUserResponse:

    def __init__(self, session):
        self.session = session

    def toJsonString(self):
        newJson = {}
        newJson['session'] = self.session
        return json.dumps(newJson)

    @staticmethod
    def fromJsonString(jsonString):
        jsonObj = json.loads(jsonString)
        request = ServerResponse(jsonObj["session"])
        return request