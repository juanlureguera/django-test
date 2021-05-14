import json


class ClientRequest:

    def __init__(self, softwareID, request=""):
        self.softwareID = softwareID
        self.request = request

    def toJsonString(self):
        newJson = {}
        newJson['softwareID'] = self.softwareID
        newJson['request'] = self.request

        return json.dumps(newJson)

    @staticmethod
    def fromJsonString(jsonString):
        jsonObj = json.load(jsonString)
        request = ClientRequest(jsonObj["softwareID"], jsonObj["request"])
        return request
