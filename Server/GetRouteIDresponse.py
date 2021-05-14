import json


class GetRouteIDresponse:

    def __init__(self, id):
        self.id = id

    def toJsonString(self):
        newJson = {}
        newJson['id'] = self.id
        return json.dumps(newJson)

    @staticmethod
    def fromJsonString(jsonString):
        jsonObj = json.loads(jsonString)
        request = GetRouteIDresponse(jsonObj["id"])
        return request