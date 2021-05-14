import json


class GetIDfromRoute:

    def __init__(self, id):
        self.id = id

    def toJsonString(self):
        newJson = {}
        newJson['id'] = self.id
        return json.dumps(newJson)

    @staticmethod
    def fromJsonString(jsonString):
        jsonObj = json.loads(jsonString)
        request = GetIDfromRoute(jsonObj["id"])
        return request