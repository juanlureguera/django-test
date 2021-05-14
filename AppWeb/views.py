# -*- encoding: utf-8 -*-
from django.shortcuts import render
from django.http import Http404
from django.contrib.auth.models import User
from django.shortcuts import render
from Client.ClientRequest import ClientRequest
from Client.LoginRequest import LoginRequest
from Client.ProfileSetRequest import ProfileSetRequest
from Client.RegisterRequest import RegisterRequest
from Client.ProfileGetRequest import ProfileGetRequest
from Server.ProfileResponse import ProfileResponse
from Server.RouteListResponse import RouteListResponse
from Sockets.MessageType import MessageType as MessageType
from Sockets.Protocol import Protocol
from Server.ProfileResponse import ProfileResponse
from Server.ServerError import ServerError
from django.http import HttpResponse
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response
from AppContent.views import doListRoute, getTypeUser, DriverAccountOFF
import time

def Index(request):
    if request.user.is_authenticated():
        # aquí se salta a la vista de men´u principal.
        context = {
            'sessionID': request.session['javaSession'],
            'date': time.strftime('%Y-%m-%d')
        }
        response = doListRoute(context)
        context = {
            'session': request.session['javaSession'],
        }
        isDriver = getTypeUser(context)

        if isDriver:
            DriverAccountOFF(request)

        return render(request, 'AppContent/home.html', { 'routes': response.routeList, 'isDriver': isDriver })
        pass
    else:
        # aquí hay que saltar (ventana/pestaña) con la vista UserLogin.
        return render(request, 'AppWeb/index.html')

@csrf_exempt
def Login(request):
    error = ""
    session = ""
    if request.method == 'POST':
        loginUserName = request.POST['usrname']
        loginPassword = request.POST['psw']

        print "usrname: " + loginUserName
        print "pass: " + loginPassword
        context = {
            'loginUserName': loginUserName,
            'loginPassword': loginPassword,
        }
        if len(loginUserName) != 0 and len(loginPassword) != 0:

            error, session = doLogin(context)
        else:
            error = "not"
        if error == "No hubo errores":
            user = User.objects.create_user(loginUserName, "", loginPassword)
            user.save()
            user = auth.authenticate(username=loginUserName, password=loginPassword)
            auth.login(request, user)

            request.session['javaSession'] = session


    return HttpResponse(error)
    
def doLogin(context):
    print "dologin"
    tipoMensaje = MessageType.enum["LOGIN"]
    print tipoMensaje
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
        error = errores[mensajeError]
        if mensajeError == ServerError.enum["NO_ERROR"]:
            sessionId = response.response
        session = response.response
    return error, session

@csrf_exempt
def Register(request):
    print "register"
    error = ""
    if request.method == 'POST':
        usrnameR = request.POST['usrnameR']
        dniR = request.POST['dniR']
        nameR = request.POST['nameR']
        emailR = request.POST['emailR']
        borndateR = request.POST['borndateR']
        pswR = request.POST['pswR']
        bancR = request.POST['bancR']

        context = {
            'usrnameR': usrnameR,
            'dniR': dniR,
            'nameR': nameR,
            'emailR': emailR,
            'borndateR': borndateR,
            'pswR': pswR,
            'bancR': bancR,
        }
        error = doRegister(context)
    return HttpResponse(error)

def doRegister(context):
    print "doregister"
    tipoMensaje = MessageType.enum["REGISTER"]
    register = Protocol(tipoMensaje)
    if register.tocTocRequest():
        data = ClientRequest(Protocol.clientID,
                             RegisterRequest(context['usrnameR'], context['pswR'],
                                             context['nameR'], context['borndateR'], 
                                             context['dniR'], context['bancR'], 
                                             context['emailR']).toJsonString())
        register.sendClientRequest(data.toJsonString())
        response = register.getServerResponse()
        mensajeError = ServerError.enum[response.responseError]
        errores = {ServerError.enum["NO_ERROR"]: "No hubo errores",
                   ServerError.enum["CREATE_REGISTER"]: "Error al crear el registro",
                   ServerError.enum["DUP_REGISTER"]: "Nombre de usuario ya existente",
                   ServerError.enum["INVALID_REGISTER"]: "Datos del Registro Errores"}
        error = errores[mensajeError]
        if mensajeError == ServerError.enum["NO_ERROR"]:
            sessionId = response.response
    return error