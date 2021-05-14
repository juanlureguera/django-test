import json
class ProfileGetRequest:

    def __init__(self,sessionId):
        self.sessionId = sessionId

    def toJsonString(self):
        newJson = {}
        newJson['sessionId'] = self.sessionId
        return json.dumps(newJson)

    @staticmethod
    def fromJsonString(jsonString):
        jsonObj = json.load(jsonString)
        request = ProfileGetRequest(jsonObj["sessionId"])
        return request
