import json
from Server.RouteResponse import RouteResponse
class RouteListResponse:

	def __init__(self, routeList):
		self.routeList = routeList

	@staticmethod
	def fromJsonString(jsonString):
		jsonObj = json.loads(jsonString)
		size = len(jsonObj)
		routeList = []

		for i in range ( size ):
			route = RouteResponse( jsonObj[i].get('id'), jsonObj[i].get('start'), jsonObj[i].get('end'), jsonObj[i].get('day') )
			routeList.append(route)
		return RouteListResponse( routeList )