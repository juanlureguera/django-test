import json
class MessageResponse:

	def __init__(self, id, idClientUser, idUser, type,  issue, description, date, idJourney, live ):
		self.id = id
		self.idClientUser = idClientUser
		self.idUser = idUser
		self.type = type
		self.issue = issue
		self.description = description
		self.date = date
		self.idJourney = idJourney
		self.live = live

	def toJsonString(self):
		newJson = {}
		newJson['id'] = self.id
		newJson['idClientUser'] = self.idClientUser
		newJson['idUser'] = self.idUser
		newJson['type'] = self.type
		newJson['issue'] = self.issue
		newJson['description'] = self.description
		newJson['date'] = self.date
		newJson['idJourney'] = self.idJourney
		newJson['live'] = self.live
		return json.dumps(newJson)

	@staticmethod
	def fromJsonString(jsonString):
		jsonObj = json.loads(jsonString)
		request = MessageResponse(jsonObj["id"], jsonObj["idClientUser"], jsonObj["idUser"], jsonObj["type"],
								  jsonObj["issue"], jsonObj["description"], jsonObj["date"], jsonObj["idJourney"], jsonObj["live"])
		return request
