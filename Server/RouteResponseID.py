import json

from Server.ServerResponse import ServerResponse


class RouteResponseID:

    def __init__(self, session, routeID):
        self.session = session
        self.routeID = routeID

    def toJsonString(self):
        newJson = {}
        newJson['session'] = self.session
        newJson['routeID'] = self.routeID
        return json.dumps(newJson)

    @staticmethod
    def fromJsonString(jsonString):
        jsonObj = json.loads(jsonString)
        request = ServerResponse(jsonObj["session"], jsonObj["routeID"])
        return request