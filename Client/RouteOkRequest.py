import json

class RouteOkRequest:
    def __init__(self, session, id):
        self.session = session
        self.id= id

    def toJsonString(self):
        newJson = {}
        newJson['session'] = self.session
        newJson['id'] = self.id
        return json.dumps(newJson)

    @staticmethod
    def fromJsonString(jsonString):
        jsonObj = json.loads(jsonString)
        request = RouteOkRequest(jsonObj["session"], jsonObj["id"])
        return request