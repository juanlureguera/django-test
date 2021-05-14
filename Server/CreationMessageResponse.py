import json
import base64
class CreationMessageResponse:

    def __init__(self, sessionID, type, issue, description, routeID, date):
        self.sessionID = sessionID
        self.type=type
        self.issue = issue
        self.description = description
        self.routeID = routeID
        self.date = date

    def toJsonString(self):
        newJson = {}
        newJson['sessionID'] = self.sessionID
        newJson['type']=self.type
        newJson['issue'] = self.issue
        newJson['description'] = self.description
        newJson['routeID'] = self.routeID
        newJson['date'] = self.date

        return json.dumps(newJson)

    @staticmethod
    def fromJsonString(jsonString):
        jsonObj = json.load(jsonString)

        request = CreationMessageResponse(jsonObj["sessionID"], jsonObj["type"], jsonObj["issue"], jsonObj["description"], jsonObj["routeID"], jsonObj["date"])
        return request
