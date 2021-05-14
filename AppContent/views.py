from django.http import HttpResponseRedirect

from Client.DeleteMessageRequest import DeleteMessageRequest
from Client.LoginRequest import LoginRequest
from Client.RegisterDriverRequest import RegisterDriverRequest
from Client.RouteGetMessage import RouteGetMessage
from Client.RouteListDriverRequest import RouteListDriverRequest
from Client.RouteOkRequest import RouteOkRequest
from Client.VehicleSetRequest import VehicleSetRequest
from Server import GetIDfromRoute
from Server import GetRouteIDresponse
from Server import VehicleResponse
from Server.CreationMessageResponse import CreationMessageResponse
from Server.CreationPuntuationResponse import CreationPuntuationResponse
from Server.GetBeneficieResponse import GetBeneficieResponse
from Server.GetVehicleOkResponse import GetVehicleOkResponse
from Server.GetRouteIDresponse import GetRouteIDresponse
from Server.GetIDfromRoute import GetIDfromRoute
from Server.MessageListResponse import MessageListResponse
from Server.MessageResponse import MessageResponse
from Server.ProfileGetbyUserName import ProfileGetbyUserName
from Server.RouteListResponse import RouteListResponse
from Server.RouteResponseID import RouteResponseID
from Server.ServerError import ServerError
from Server.TypeUserResponse import TypeUserResponse
from Server.ProfileResponse import ProfileResponse
from Server.VehicleResponse import VehicleResponse
from Server.GetDriverNameResponse import GetDriverNameResponse
from Sockets.MessageType import MessageType as MessageType
from Sockets.Protocol import Protocol
from Client.ProfileSetRequest import ProfileSetRequest
from Client.RouteGetDetails import RouteGetDetails
from Client.ClientRequest import ClientRequest
from Client.CRouteRequest import CRouteRequest
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

import time


@login_required(login_url="/index/")
@csrf_exempt
def saveProfile(request):
    error = ""
    if request.method == 'POST':
        txtname = request.POST['txtname']
        dni = request.POST['dni']
        txtEmail = request.POST['txtEmail']
        txtCuentaB = request.POST['txtCuentaB']
        txtBornDate = request.POST['txtBornDate']
        newPass = request.POST['nPass']
        txtPasswordView = request.POST['txtPasswordView']

        context = {
            'session': request.session['javaSession'],
            'txtname': txtname,
            'dni': dni,
            'txtEmail': txtEmail,
            'txtCuentaB': txtCuentaB,
            'txtPasswordView': txtPasswordView,
            'newPass': newPass,
            'txtBornDate': txtBornDate
        }
        error = doProfileSet(context)

    return HttpResponse(error)


def doProfileSet(context):
    error = ""
    tipoMensaje = MessageType.enum["PROFILESET_NC"]
    profileset = Protocol(tipoMensaje)
    if profileset.tocTocRequest():
        data = ClientRequest(Protocol.clientID, ProfileSetRequest(
            context['session'],
            context['txtname'],
            context['dni'],
            context['txtEmail'],
            context['txtCuentaB'],
            context['txtPasswordView'],
            context['newPass'],
            context['txtBornDate']
        ).toJsonString())

        profileset.sendClientRequest(data.toJsonString())
        response = profileset.getServerResponse()
        mensajeError = ServerError.enum[response.responseError]
        print mensajeError
        errores = {
            ServerError.enum["BAD_AUTH"]: "Error usuario no encontrado",
            ServerError.enum["NO_ERROR"]: "No hubo errores",
            ServerError.enum["PROFILE_SET"]: "Error al cambiar los datos del usuario",
        }

        error = errores[mensajeError]

    return error


@login_required(login_url="/index/")
def viewProfile(request):
    context = {
        'session': request.session['javaSession'],
    }
    # typeUser: false -> no conductor
    # typeUser: true -> conductor
    typeUser = getTypeUser(context)
    response = doProfileGet(request)

    print(typeUser)
    context = {
        'driver': False,
        'isMe': request.user.username == response.loginName,
        'userC': typeUser,
        'loginName': response.loginName,
        'pass': response.passw,
        'name': response.name,
        'email': response.email,
        'bornDate': response.bornDate,
        'dni': response.dni,
        'cuentaBancaria': response.cuentaBancaria,
        'puntuation': response.puntuation
    }

    if typeUser == True:
        vehicle = doVehicleGet(request)

        return render(request, 'AppContent/profile.html', context, { 'vehicle': vehicle })
    elif typeUser == False:

        return render(request, 'AppContent/profile.html', context)



def doProfileGet(request):
    tipoMensaje = MessageType.enum["PRFILEGET_NC"]
    profileget = Protocol(tipoMensaje)
    if profileget.tocTocRequest():
        data = ClientRequest(Protocol.clientID, request.session['javaSession'])
        profileget.sendClientRequest(data.toJsonString())
        responseServer = profileget.getServerResponse()
        mensajeError = ServerError.enum[responseServer.responseError]


    if mensajeError == ServerError.enum["NO_ERROR"]:
        profileresponse = ProfileResponse.fromJsonString(responseServer.response)

    return profileresponse


@login_required(login_url="/index/")
@csrf_exempt
def createRoute(request):
    error = ""
    if request.method == 'POST':
        start = request.POST['start']
        end = request.POST['end']
        distance = request.POST['distance']
        duration = request.POST['duration']
        price = request.POST['price']
        startdate = request.POST['startdate']
        hour = request.POST['hour']
        minutes = request.POST['minutes']


        context = {
            'session': request.session['javaSession'],
            'start': start,
            'end': end,
            'distance': distance,
            'duration': duration,
            'price': price,
            'startdate': startdate,
            'hour': hour,
            'minutes': minutes,
        }
        error = doCeateRoute(context)
    return HttpResponse(error)


def doCeateRoute(context):
    print "doCeateRoute"
    error = ""
    tipoMensaje = MessageType.enum["CREATE_ROUTE"]
    createR = Protocol(tipoMensaje)
    if createR.tocTocRequest():
        data = ClientRequest(Protocol.clientID,
                             CRouteRequest(context['session'], context['start'], context['end'],
                                           context['distance'], context['duration'],
                                           context['price'], context['startdate'],
                                           context['hour'], context['minutes']).toJsonString())
        createR.sendClientRequest(data.toJsonString())
        response = createR.getServerResponse()
        mensajeError = ServerError.enum[response.responseError]
        errores = {
            ServerError.enum["NO_ERROR"]: "No hubo errores",
            ServerError.enum["INVALID_ROUTE"]: "Ruta introducida no es valida.",
        }
        error = errores[mensajeError]
    return error


def doListRoute(context):
    tipoMensaje = MessageType.enum["ROUTE_LIST"]
    routeList = Protocol(tipoMensaje)
    if routeList.tocTocRequest():
        data = ClientRequest(Protocol.clientID, RouteListDriverRequest ( context['sessionID'],context['date']).toJsonString())
        routeList.sendClientRequest(data.toJsonString())
        responseServer = routeList.getServerResponse()
        mensajeError = ServerError.enum[responseServer.responseError]


    if mensajeError == ServerError.enum["NO_ERROR"]:
        routeList = RouteListResponse.fromJsonString(responseServer.response)

    return routeList


@login_required(login_url="http://127.0.0.1:8000")
def Logout(request):
    doLogout(request)

    request.user.delete()
    logout(request)

    return render(request, 'AppContent/logout.html')


def doLogout(request):
    print request.session['javaSession']
    tipoMensaje = MessageType.enum["LOGOUT"]
    logout = Protocol(tipoMensaje)
    if logout.tocTocRequest():
        data = ClientRequest(Protocol.clientID, request.session['javaSession'])
        logout.sendClientRequest(data.toJsonString())


def getRouteDetails(request, rutaID):
    context = {
        'session': request.session['javaSession'],
        'id': rutaID,
    }
    idUser = getidUserFromRoutaID(context)

    print("dasdasd")
    print(idUser.id)
    # ismeroute: false -> ruta no propia
    # ismeroute: true -> ruta propia
    isparticiped = IsMeParticiped(context)
    ismeroute = isMYroute(context)
    # typeUser: false -> no conductor
    # typeUser: true -> conductor

    typeUser = getTypeUser(context)
    response = doRouteGet(context)


    if typeUser:
        isDriverConnected = isConnectedDriver(request)
    else:
        isDriverConnected = False

    if ismeroute:
        duracion = (float)(response.distance) / 60
        distancia = (float)(response.duration) / 1000
        context = {
            'idUser': idUser.id,
            'isDriverConnected': isDriverConnected,
            'isparticiped': isparticiped,
            'ismeroute': ismeroute,
            'id': rutaID,
            'userC': typeUser,
            'start': response.start,
            'destino': response.end,
            'duration': duracion,
            'distancia': distancia,
            'price': response.price,
            'startDate': response.startdate
        }

        return render(request, 'AppContent/routeDetails.html', context)
    elif typeUser:
        duracion = (float)(response.distance) / 60
        distancia = (float)(response.duration) / 1000
        context = {
            'idUser': idUser.id,
            'isDriverConnected': isDriverConnected,
            'isparticiped': isparticiped,
            'ismeroute': ismeroute,
            'id': rutaID,
            'userC': typeUser,
            'start': response.start,
            'destino': response.end,
            'duration': duracion,
            'distancia': distancia,
            'price': response.price,
            'startDate': response.startdate
        }

        return render(request, 'AppContent/routeDetails.html', context)
    else:
        return render(request, 'Errors/404.html')

def doRouteGet(context):
    tipoMensaje = MessageType.enum["GET_ROUTE_DETAILS"]
    routeget = Protocol(tipoMensaje)
    if routeget.tocTocRequest():
        data = ClientRequest(Protocol.clientID, RouteGetDetails(
            context['session'],
            context['id']).toJsonString())
        routeget.sendClientRequest(data.toJsonString())
        responseServer = routeget.getServerResponse()
        mensajeError = ServerError.enum[responseServer.responseError]


    if mensajeError == ServerError.enum["NO_ERROR"]:
        routeResponse = CRouteRequest.fromJsonString(responseServer.response)

    return routeResponse


def getTypeUser(context):
    tipoMensaje = MessageType.enum["GET_TYPE_USER"]
    typeUser = Protocol(tipoMensaje)
    if typeUser.tocTocRequest():
        data = ClientRequest(Protocol.clientID, TypeUserResponse(
            context['session']).toJsonString())
        typeUser.sendClientRequest(data.toJsonString())
        responseServer = typeUser.getServerResponse()
        mensajeError = ServerError.enum[responseServer.responseError]

        if mensajeError == "13":
            return False
        else:
            return True


def isMYroute(context):
    tipoMensaje = MessageType.enum["IS_ROUTE_USER"]
    typeUser = Protocol(tipoMensaje)
    if typeUser.tocTocRequest():
        data = ClientRequest(Protocol.clientID, RouteResponseID(
            context['session'], context['id']).toJsonString())
        typeUser.sendClientRequest(data.toJsonString())
        responseServer = typeUser.getServerResponse()
        mensajeError = ServerError.enum[responseServer.responseError]

        if mensajeError == "13":
            return False
        else:
            return True

@csrf_exempt
def RegisterDriver(request):
    error = ""
    if request.method == 'POST':
        bancR = request.POST['bancR']
        matricula = request.POST['matricula']
        marca = request.POST['marca']
        modelo = request.POST['modelo']
        anios = request.POST['anios']
        km = request.POST['km']

        context = {
            'sessionID': request.session['javaSession'],
            'bancR': bancR,
            'matricula': matricula,
            'marca': marca,
            'modelo': modelo,
            'anios': anios,
            'km': km,
        }
        error = doRegisterDriver(context)
    return HttpResponse(error)

def doRegisterDriver(context):
    tipoMensaje = MessageType.enum["REGISTER_DRIVER"]
    register = Protocol(tipoMensaje)
    if register.tocTocRequest():
        data = ClientRequest(Protocol.clientID,
                             RegisterDriverRequest(context['sessionID'], context['bancR'],context['matricula'],
                             context['marca'], context['modelo'], context['anios'], context['km']).toJsonString())
        register.sendClientRequest(data.toJsonString())
        response = register.getServerResponse()
        mensajeError = ServerError.enum[response.responseError]
        errores = {ServerError.enum["NO_ERROR"]: "No hubo errores",
                   ServerError.enum["CREATE_REGISTER"]: "Error al crear el registro",
                   ServerError.enum["DUP_REGISTER"]: "Nombre de usuario ya existente",
                   ServerError.enum["INVALID_REGISTER"]: "Datos del Registro Errores"}
        error = errores[mensajeError]

    return error

@csrf_exempt
def LoginDriver(request):
    error = ""
    if request.method == 'POST':
        loginUserName = request.POST['usrname']
        loginPassword = request.POST['psw']

        context = {
            'loginUserName': loginUserName,
            'loginPassword': loginPassword,
        }
        if len(loginUserName) != 0 and len(loginPassword) != 0:

            error = doLogin(context)
        else:
            error = "not"

        if error == True:
            error = "No hubo errores"
        print error

    return HttpResponse(error)

def doLogin(context):
    isLogin = False
    tipoMensaje = MessageType.enum["LOGIN_DRIVER"]
    login = Protocol(tipoMensaje)
    if login.tocTocRequest():
      data = ClientRequest(Protocol.clientID,
                           LoginRequest(context['loginUserName'], context['loginPassword']).toJsonString())
      login.sendClientRequest(data.toJsonString())
      response = login.getServerResponse()
      mensajeError = ServerError.enum[response.responseError]
      errores = {ServerError.enum["NO_ERROR"]: "No hubo errores",
                 ServerError.enum["CREATE_SESSION"]: "Error al crear la sesion",
                 ServerError.enum["BAD_AUTH"]: "Credenciales no validas"}

      if mensajeError == ServerError.enum["NO_ERROR"]:
          isLogin = True

    return isLogin

def doListDriverRoute(context):
    tipoMensaje = MessageType.enum["ROUTE_LIST_DRIVER"]
    routeList = Protocol(tipoMensaje)

    if routeList.tocTocRequest():
        data = ClientRequest(Protocol.clientID, RouteListDriverRequest ( context['sessionID'],context['date']).toJsonString() )

    routeList.sendClientRequest(data.toJsonString())
    responseServer = routeList.getServerResponse()
    mensajeError = ServerError.enum[responseServer.responseError]

    if mensajeError == ServerError.enum["NO_ERROR"]:
        routeList = RouteListResponse.fromJsonString(responseServer.response)

    return routeList

def doVehicleGet(request):
    tipoMensaje = MessageType.enum["PRFILE_VEHICLE"]
    vehicleget = Protocol(tipoMensaje)
    if vehicleget.tocTocRequest():
        data = ClientRequest(Protocol.clientID, request.session['javaSession'])
        vehicleget.sendClientRequest(data.toJsonString())
        responseServer = vehicleget.getServerResponse()
        mensajeError = ServerError.enum[responseServer.responseError]


    if mensajeError == ServerError.enum["NO_ERROR"]:
        vehicleresponse = VehicleResponse.fromJsonString(responseServer.response)

    return vehicleresponse

def DriverHome(request):
    context = {
       'sessionID': request.session['javaSession'],
        'date': time.strftime('%Y-%m-%d')
    }
    response = doListDriverRoute(context)
    if len(response.routeList) == 0:
        emp = True
    else:
        emp = False


    vehicle = doVehicleGet(request)
    vehicleOk = getVehicleOk(request)
    benefice = getBeneficie(request)

    print("dsds")
    print(benefice.benefice)
    DriverAccountON(request)

    return render(request, 'AppContent/driver.html', { 'benefice': benefice.benefice,'emp': emp, 'routes': response.routeList, 'vehicle': vehicle, 'vehicleOk': vehicleOk.ok } )

def sendMessageDriverToClient(request, rutaID):

    context = {
        'sessionID': request.session['javaSession'],
        'type': 1,
        'issue': "Peticion de conductor",
        'description': "Me gustaria llevarte en este trayecto",
        'routeID': rutaID,
        'date': time.strftime('%Y-%m-%d')
    }
    error = doSendMessage(context)

    context = {
        'sessionID': request.session['javaSession'],
        'date': time.strftime('%Y-%m-%d')
    }
    response = doListDriverRoute(context)
    vehicle = doVehicleGet(request)
    return HttpResponseRedirect('http://127.0.0.1:8000/driver-home')
    #return render(request, 'AppContent/driver.html', {'routes': response.routeList, 'vehicle': vehicle})

def doSendMessage(context):
    isSend = False
    tipoMensaje = MessageType.enum["SEND_MESSAGE"]
    sendMessage = Protocol(tipoMensaje)
    if sendMessage.tocTocRequest():
        data = ClientRequest(Protocol.clientID,
                             CreationMessageResponse (context['sessionID'], context['type'], context['issue'],
                                                      context['description'], context['routeID'], context['date']).toJsonString())
        sendMessage.sendClientRequest(data.toJsonString())
        responseServer = sendMessage.getServerResponse()
        mensajeError = ServerError.enum[responseServer.responseError]
        errores = {ServerError.enum["NO_ERROR"]: "No hubo errores"}


        if mensajeError == ServerError.enum["NO_ERROR"]:
            isSend = True

        return isSend

def ReadMessages(request):
    response = doReadMessages(request)
    context = {
        'session': request.session['javaSession'],
    }
    isDriver = getTypeUser(context)

    return render(request, 'AppContent/messages.html', {'message': response.messageList, 'isDriver': isDriver})

def doReadMessages(request):
    tipoMensaje = MessageType.enum["MESSAGE_LIST"]
    messageList = Protocol(tipoMensaje)
    if messageList.tocTocRequest():
        data = ClientRequest(Protocol.clientID, request.session['javaSession'])
        messageList.sendClientRequest(data.toJsonString())
        responseServer = messageList.getServerResponse()
        mensajeError = ServerError.enum[responseServer.responseError]


    if mensajeError == ServerError.enum["NO_ERROR"]:

        list = MessageListResponse.fromJsonString(responseServer.response)

    return list

def getMessageDetails(request, messageID):
    context = {
        'session': request.session['javaSession'],
        'id': messageID,
    }

    response = doMessageGet(context)

    context = {
        'session': request.session['javaSession'],
        'id': response.idUser
    }
    driverName = doGetDriverName( context )

    typeUser = getTypeUser(context)

    peticion = False
    baja = False
    confirmacion = False
    confirmacionc = False

    if response.type == 1:
        peticion = True
        baja = False
        confirmacion = False
        confirmacionc = False
    elif response.type == 2:
        peticion = False
        baja = True
        confirmacion = False
        confirmacionc = False
    elif response.type == 3:
        peticion = False
        baja = False
        confirmacion = True
        confirmacionc = False
    elif response.type == 4:
        peticion = False
        baja = False
        confirmacion = False
        confirmacionc = True

    context = {
        'session': request.session['javaSession'],
        'id': messageID
    }
    isMeMessage = IsMeMessage(context)
    isPuntuated = isDriverPuntuated(context)

    return render(request, 'AppContent/messageDetails.html', { 'typeUser':typeUser,'isPuntuated': isPuntuated ,'isMeMessage': isMeMessage, 'message': response, 'driverName': driverName.name, 'type1': peticion, 'type2': baja, 'type3': confirmacion, 'type4': confirmacionc } )

def isConnectedDriver(request):
    tipoMensaje = MessageType.enum["IS_CONNECTED_DRIVER"]
    typeUser = Protocol(tipoMensaje)
    if typeUser.tocTocRequest():
        data = ClientRequest(Protocol.clientID, request.session['javaSession'])
        typeUser.sendClientRequest(data.toJsonString())
        responseServer = typeUser.getServerResponse()
        mensajeError = ServerError.enum[responseServer.responseError]

        if mensajeError == "13":
            return False
        else:
            return True

def isDriverPuntuated(context):
    tipoMensaje = MessageType.enum["IS_PUNTUATION"]
    typeUser = Protocol(tipoMensaje)
    if typeUser.tocTocRequest():
        data = ClientRequest(Protocol.clientID, RouteResponseID(
            context['session'], context['id']).toJsonString())
        typeUser.sendClientRequest(data.toJsonString())
        responseServer = typeUser.getServerResponse()
        mensajeError = ServerError.enum[responseServer.responseError]

        if mensajeError == "13":
            return False
        else:
            return True

def getidUserFromRoutaID(context):
    tipoMensaje = MessageType.enum["GET_IDUSER_ROUTE"]
    vehicleOKget = Protocol(tipoMensaje)
    if vehicleOKget.tocTocRequest():
        data = ClientRequest(Protocol.clientID, RouteResponseID(
            context['session'], context['id']).toJsonString())
        vehicleOKget.sendClientRequest(data.toJsonString())
        responseServer = vehicleOKget.getServerResponse()
        mensajeError = ServerError.enum[responseServer.responseError]

    print(responseServer.response)
    if mensajeError == ServerError.enum["NO_ERROR"]:
        vehicleResponse = GetIDfromRoute.fromJsonString(responseServer.response)

    return vehicleResponse

def IsMeParticiped(context):
    tipoMensaje = MessageType.enum["IS_ME_PARTICIPED"]
    typeUser = Protocol(tipoMensaje)
    if typeUser.tocTocRequest():
        data = ClientRequest(Protocol.clientID, RouteResponseID(
            context['session'], context['id']).toJsonString())
        typeUser.sendClientRequest(data.toJsonString())
        responseServer = typeUser.getServerResponse()
        mensajeError = ServerError.enum[responseServer.responseError]

        if mensajeError == "13":
            return False
        else:
            return True

def IsMeMessage(context):
    tipoMensaje = MessageType.enum["IS_ME_MESSAGE"]
    typeUser = Protocol(tipoMensaje)
    if typeUser.tocTocRequest():
        data = ClientRequest(Protocol.clientID, RouteResponseID(
            context['session'], context['id']).toJsonString())
        typeUser.sendClientRequest(data.toJsonString())
        responseServer = typeUser.getServerResponse()
        mensajeError = ServerError.enum[responseServer.responseError]

        if mensajeError == "13":
            return False
        else:
            return True

def doMessageGet(context):
    tipoMensaje = MessageType.enum["GET_MESSAGE_DETAILS"]
    messageget = Protocol(tipoMensaje)
    if messageget.tocTocRequest():
        data = ClientRequest(Protocol.clientID, RouteGetMessage(
            context['session'],
            context['id']).toJsonString())
        messageget.sendClientRequest(data.toJsonString())
        responseServer = messageget.getServerResponse()
        mensajeError = ServerError.enum[responseServer.responseError]

    if mensajeError == ServerError.enum["NO_ERROR"]:
        messageResponse = MessageResponse.fromJsonString(responseServer.response)

    return messageResponse

def doGetDriverName(context):
    tipoMensaje = MessageType.enum["GET_DRIVER_NAME"]
    nameGet = Protocol(tipoMensaje)
    if nameGet.tocTocRequest():
        data = ClientRequest(Protocol.clientID, RouteGetMessage(
            context['session'],
            context['id']).toJsonString())
        nameGet.sendClientRequest(data.toJsonString())
        responseServer = nameGet.getServerResponse()
        mensajeError = ServerError.enum[responseServer.responseError]


    if mensajeError == ServerError.enum["NO_ERROR"]:
        name = GetDriverNameResponse.fromJsonString(responseServer.response)

    return name

def getUserProfile(request, id):
    context = {
        'session': request.session['javaSession'],
    }
    # typeUser: false -> no conductor
    # typeUser: true -> conductor
    typeUser = getTypeUser(context)

    driver = True
    response = doProfileGetun(request, id)
    context = {
        'driver': driver,
        'isMe': request.user.username == response.loginName,
        'userC': typeUser,
        'loginName': response.loginName,
        'pass': response.passw,
        'name': response.name,
        'email': response.email,
        'bornDate': response.bornDate,
        'dni': response.dni,
        'cuentaBancaria': response.cuentaBancaria,
        'puntuation': response.puntuation
    }

    if typeUser == True:
        vehicle = doVehicleGet(request)

        return render(request, 'AppContent/profile.html', context, { 'vehicle': vehicle })
    elif typeUser == False:

        return render(request, 'AppContent/profile.html', context)

def doProfileGetun(request, id):

    tipoMensaje = MessageType.enum["PRFILEGET_NCun"]
    profileget = Protocol(tipoMensaje)
    if profileget.tocTocRequest():
        data = ClientRequest(Protocol.clientID, ProfileGetbyUserName(request.session['javaSession'], id ).toJsonString())
        profileget.sendClientRequest(data.toJsonString())
        responseServer = profileget.getServerResponse()
        mensajeError = ServerError.enum[responseServer.responseError]


    if mensajeError == ServerError.enum["NO_ERROR"]:
        profileresponse = ProfileResponse.fromJsonString(responseServer.response)

    return profileresponse

def AceptRoute(request, id):
    print("acept")
    tipoMensaje = MessageType.enum["ROUTE_OK"]
    routeok = Protocol(tipoMensaje)
    if routeok.tocTocRequest():
        data = ClientRequest(Protocol.clientID, RouteOkRequest(request.session['javaSession'], id).toJsonString())
        routeok.sendClientRequest(data.toJsonString())
        responseServer = routeok.getServerResponse()
        mensajeError = ServerError.enum[responseServer.responseError]

        return render(request, 'AppContent/payOK.html')

@csrf_exempt
def SaveVehicle(request):
    error = ""
    if request.method == 'POST':
        matricula = request.POST['matricula']
        marca = request.POST['marca']
        modelo = request.POST['modelo']
        anio = request.POST['anio']
        km = request.POST['km']

        context = {
            'session': request.session['javaSession'],
            'matricula': matricula,
            'marca': marca,
            'modelo': modelo,
            'anio': anio,
            'km': km,
        }
        error = doVehicleSet(context)

    return HttpResponse(error)

def doVehicleSet(context):
    error = ""
    tipoMensaje = MessageType.enum["VEHICLESET"]
    vehicleSet = Protocol(tipoMensaje)
    if vehicleSet.tocTocRequest():
        data = ClientRequest(Protocol.clientID, VehicleSetRequest(
            context['session'],
            context['matricula'],
            context['marca'],
            context['modelo'],
            context['km'],
            context['anio']
        ).toJsonString())

        vehicleSet.sendClientRequest(data.toJsonString())
        response = vehicleSet.getServerResponse()
        mensajeError = ServerError.enum[response.responseError]
        print mensajeError
        errores = {
            ServerError.enum["BAD_AUTH"]: "Error usuario no encontrado",
            ServerError.enum["NO_ERROR"]: "No hubo errores",
            ServerError.enum["PROFILE_SET"]: "Error al cambiar los datos del usuario",
        }

        error = errores[mensajeError]

    return error

def getBeneficie(request):
    tipoMensaje = MessageType.enum["GET_BENEFICIE"]
    bnget = Protocol(tipoMensaje)
    if bnget.tocTocRequest():
        data = ClientRequest(Protocol.clientID, request.session['javaSession'])
        bnget.sendClientRequest(data.toJsonString())
        responseServer = bnget.getServerResponse()
        mensajeError = ServerError.enum[responseServer.responseError]

    print(responseServer.response)
    if mensajeError == ServerError.enum["NO_ERROR"]:
        beneficeResponse = GetBeneficieResponse.fromJsonString(responseServer.response)

    return beneficeResponse

def getVehicleOk(request):
    tipoMensaje = MessageType.enum["GET_VEHICLE_OK"]
    vehicleOKget = Protocol(tipoMensaje)
    if vehicleOKget.tocTocRequest():
        data = ClientRequest(Protocol.clientID, request.session['javaSession'])
        vehicleOKget.sendClientRequest(data.toJsonString())
        responseServer = vehicleOKget.getServerResponse()
        mensajeError = ServerError.enum[responseServer.responseError]

    print(responseServer.response)
    if mensajeError == ServerError.enum["NO_ERROR"]:
        vehicleResponse = GetVehicleOkResponse.fromJsonString(responseServer.response)

    return vehicleResponse

@csrf_exempt
def PuntuationDriver(request):
    error = ""
    if request.method == 'POST':
        id = request.POST['id']
        puntuation = request.POST['puntuation']


        context = {
            'session': request.session['javaSession'],
            'id': id,
            'puntuation': puntuation,
        }
        error = SendPuntuation(context)

        if error:
            return HttpResponse(error)
        else:
            return HttpResponse(error)

def SendPuntuation(context):
    isSend = False
    tipoMensaje = MessageType.enum["SEND_PUNTUATION"]
    sendPuntuation = Protocol(tipoMensaje)
    if sendPuntuation.tocTocRequest():
        data = ClientRequest(Protocol.clientID,
                             CreationPuntuationResponse(
                                 context['session'],
                                 context['id'],
                                 context['puntuation']
                             ).toJsonString())
        sendPuntuation.sendClientRequest(data.toJsonString())
        responseServer = sendPuntuation.getServerResponse()
        mensajeError = ServerError.enum[responseServer.responseError]


        if mensajeError == ServerError.enum["NO_ERROR"]:
            isSend = True

        return isSend

def DeleteMessage(request, id):
    isSend = False
    tipoMensaje = MessageType.enum["DELETE_MESSAGE"]
    deleteMessage = Protocol(tipoMensaje)
    if deleteMessage.tocTocRequest():
        data = ClientRequest(Protocol.clientID,
                             DeleteMessageRequest(request.session['javaSession'], id).toJsonString())
        deleteMessage.sendClientRequest(data.toJsonString())
        responseServer = deleteMessage.getServerResponse()
        mensajeError = ServerError.enum[responseServer.responseError]


        if mensajeError == ServerError.enum["NO_ERROR"]:
            isSend = True

        return HttpResponseRedirect('http://127.0.0.1:8000/messages-list')
def DeleteRoute(request, id):
    isSend = False
    tipoMensaje = MessageType.enum["DELETE_ROUTE"]
    deleteRoute = Protocol(tipoMensaje)
    if deleteRoute.tocTocRequest():
        data = ClientRequest(Protocol.clientID,
                             DeleteMessageRequest(request.session['javaSession'], id).toJsonString())
        deleteRoute.sendClientRequest(data.toJsonString())
        responseServer = deleteRoute.getServerResponse()
        mensajeError = ServerError.enum[responseServer.responseError]


        if mensajeError == ServerError.enum["NO_ERROR"]:
            isSend = True

        return HttpResponseRedirect('http://127.0.0.1:8000/home')

def DeleteVehicle(request):
    isSend = False
    tipoMensaje = MessageType.enum["DELETE_VEHICLE"]
    deleteVehicle = Protocol(tipoMensaje)
    if deleteVehicle.tocTocRequest():
        data = ClientRequest(Protocol.clientID, request.session['javaSession'])
        deleteVehicle.sendClientRequest(data.toJsonString())
        responseServer = deleteVehicle.getServerResponse()
        mensajeError = ServerError.enum[responseServer.responseError]


        if mensajeError == ServerError.enum["NO_ERROR"]:
            isSend = True

    return HttpResponseRedirect('http://127.0.0.1:8000/driver-home')

def doGetRouteID(context):
    tipoMensaje = MessageType.enum["GET_ROUTE_ID"]
    routeGetget = Protocol(tipoMensaje)
    if routeGetget.tocTocRequest():
        data = ClientRequest(Protocol.clientID, RouteResponseID(
            context['session'], context['id']).toJsonString())
        routeGetget.sendClientRequest(data.toJsonString())
        responseServer = routeGetget.getServerResponse()
        mensajeError = ServerError.enum[responseServer.responseError]

    print(responseServer.response)
    if mensajeError == ServerError.enum["NO_ERROR"]:
        routeIDResponse = GetRouteIDresponse.fromJsonString(responseServer.response)

    return routeIDResponse

def DriverAccountON(request):
    tipoMensaje = MessageType.enum["DRIVER_ACOUNT_ON"]
    vehicleOKget = Protocol(tipoMensaje)
    if vehicleOKget.tocTocRequest():
        data = ClientRequest(Protocol.clientID, request.session['javaSession'])
        vehicleOKget.sendClientRequest(data.toJsonString())
        responseServer = vehicleOKget.getServerResponse()
        mensajeError = ServerError.enum[responseServer.responseError]

    if mensajeError == ServerError.enum["NO_ERROR"]:
        return True
    else:
        return False

def DriverAccountOFF(request):
    tipoMensaje = MessageType.enum["DRIVER_ACOUNT_OFF"]
    vehicleOKget = Protocol(tipoMensaje)
    if vehicleOKget.tocTocRequest():
        data = ClientRequest(Protocol.clientID, request.session['javaSession'])
        vehicleOKget.sendClientRequest(data.toJsonString())
        responseServer = vehicleOKget.getServerResponse()
        mensajeError = ServerError.enum[responseServer.responseError]

    if mensajeError == ServerError.enum["NO_ERROR"]:
        return True
    else:
        return False