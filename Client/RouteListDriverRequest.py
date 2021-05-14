import json

class RouteListDriverRequest:
    def __init__(self, sessionID, date):
        self.sessionID = sessionID
        self.date = date

    def toJsonString(self):
        newJson = {}
        newJson['sessionID'] = self.sessionID
        newJson['date'] = self.date
        pepe = json.dumps(newJson)
        return json.dumps(newJson)