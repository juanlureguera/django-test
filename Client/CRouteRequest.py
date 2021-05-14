import json

class CRouteRequest:

    def __init__(self, sessionID, start, end, distance, duration, price, startdate, hour, minutes):
        self.sessionID = sessionID
        self.start = start
        self.end = end
        self.distance = distance
        self.duration = duration
        self.price = price
        self.startdate = startdate
        self.hour = hour
        self.minutes = minutes

    def toJsonString(self):
        newJson = {}
        newJson['sessionID'] = self.sessionID
        newJson['start'] = self.start
        newJson['end'] = self.end
        newJson['startDate'] = self.startdate
        newJson['distance'] = self.distance
        newJson['duration'] = self.duration
        newJson['price'] = self.price
        newJson['hour'] = self.hour
        newJson['minutes'] = self.minutes
        return json.dumps(newJson)

    @staticmethod
    def fromJsonString(jsonString):
        jsonObj = json.loads(jsonString)
        request = CRouteRequest(  jsonObj["sessionID"], jsonObj["start"], jsonObj["end"], 
                                    jsonObj["distance"], jsonObj["duration"],
                                    jsonObj["price"], jsonObj["startDate"], jsonObj["hour"], jsonObj["minutes"])
        return request
