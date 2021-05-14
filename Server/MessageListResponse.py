import json

from Server.MessageResponse import MessageResponse

class MessageListResponse:

	def __init__(self, messageList):
		self.messageList = messageList

	@staticmethod
	def fromJsonString(jsonString):
		jsonObj = json.loads(jsonString)
		size = len(jsonObj)
		messageList = []

		for i in range ( size ):
			list = MessageResponse( jsonObj[i].get('id'), jsonObj[i].get('idClientUser'), jsonObj[i].get('idUser'), jsonObj[i].get('type'), jsonObj[i].get('issue'), jsonObj[i].get('description'), jsonObj[i].get('date'), jsonObj[i].get('idJourney'), jsonObj[i].get('live') )
			messageList.append(list)
		return MessageListResponse( messageList )