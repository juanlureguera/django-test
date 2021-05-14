# -*- encoding: utf-8 -*-

import xml.etree.ElementTree as ET

from Client.ClientRequest import ClientRequest as ClientRequest
from Server.ServerResponse import ServerResponse as ServerResponse
from Sockets.InterlocutorType import InterlocutorType as InterlocutorType


class Message:

    def __init__(self, type, interlocutor, content):
        self.type = type
        self.interlocutor = interlocutor
        self.content = content

    def toXMLString(self):
        loginXML = ET.Element('Message')
        loginXML.set("type", self.type)
        loginXML.set("interlocutor", self.interlocutor)
        loginXML.text = self.content
        print ET.tostring(loginXML)
        return ET.tostring(loginXML)

    def isValidRemoteHost(self, hostType, hostId):
        if hostType == InterlocutorType.enum["CLIENT"] or hostType == InterlocutorType.enum["CTRL"] :
            request = ClientRequest.fromJsonString(self.content)
            softID = request.softwareID
        else:
            response = ServerResponse.fromJsonString(self.content)
            softID = response.softwareID
        return softID == hostId



    @staticmethod
    def fromXMLString(xmlString):
        xmlObj = ET.fromstring(xmlString)
        messageType = xmlObj.attrib.get("type")
        interlocutor = xmlObj.attrib.get("interlocutor")
        content = xmlObj.text
        message = Message(messageType, interlocutor, content)
        return message
