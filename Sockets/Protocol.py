
import socket

from Client.ClientRequest import ClientRequest
from Server.ServerResponse import ServerResponse
from Sockets.InterlocutorType import InterlocutorType as InterlocutorType
from Sockets.Message import Message as Message

class Protocol:
    appType = InterlocutorType.enum["CLIENT"]
    remoteHost = 'localhost'
    remotePort = 42320
    clientID = "AppClient"
    serverID = "AppServer"


    def __init__(self, messageType ):
        self.messageType = messageType
        self.clientSocket = socket.socket()
        self.clientSocket.connect((Protocol.remoteHost, Protocol.remotePort))

    def tocTocRequest(self):
        request = ClientRequest(Protocol.clientID)
        message = Message(self.messageType, Protocol.appType, request.toJsonString())
        self.clientSocket.send( message.toXMLString() )
        print "primer paso"
        xmlString = self.clientSocket.recv(1500)
        print "segundo paso"
        message = Message.fromXMLString(xmlString)
        print "tercer paso"
        return message.isValidRemoteHost(InterlocutorType.enum["SERVER"], Protocol.serverID)

    def sendClientRequest(self, data):
        message = Message(self.messageType, Protocol.appType, data)
        self.clientSocket.send(message.toXMLString())

    def getServerResponse(self):
        xmlString = self.clientSocket.recv(1500)
        message = Message.fromXMLString(xmlString)
        if message.isValidRemoteHost(InterlocutorType.enum["SERVER"], Protocol.serverID):
            return ServerResponse.fromJsonString(message.content)
        else:
            return None

    def finish(self):
        self.clientSocket.close()
        self = None
