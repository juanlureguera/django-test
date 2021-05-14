import json
class ServerResponse:

    def __init__(self, response, responseError, shutdown, softwareID):
        self.response = response
        self.responseError = responseError
        self.shutdown = shutdown
        self.softwareID = softwareID

    def toJsonString(self):
        newJson = {}
        newJson['response'] = self.response
        newJson['Error'] = self.responseError
        newJson['shutdown'] = self.shutdown
        newJson['softwareID'] = self.softwareID
        return json.dumps(newJson)

    @staticmethod
    def fromJsonString(jsonString):
        jsonObj = json.loads(jsonString)
        request = ServerResponse(jsonObj["response"], jsonObj["Error"], jsonObj["shutdown"], jsonObj["softwareID"])
        return request
