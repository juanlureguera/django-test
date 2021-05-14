import paypalrestsdk
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import RedirectView
from Sockets.MessageType import MessageType as MessageType

from AppContent.views import doRouteGet, AceptRoute, doGetRouteID

from AppWeb import settings





#permanent = False
from Client.ClientRequest import ClientRequest
from Server import GetRouteIDresponse
from Server import ServerError
from Server.RouteResponseID import RouteResponseID
from Sockets import MessageType
from Sockets.Protocol import Protocol


def DoPay(request, idMessage):
    context = {
        'session': request.session['javaSession'],
        'id': idMessage,
    }

    idRoute = doGetRouteID(context)
    context = {
        'session': request.session['javaSession'],
        'id': idRoute.id,
    }
    response = doRouteGet(context)

    duracion = (float)(response.distance) / 60
    distancia = (float)(response.duration) / 1000
    context = {
        'id': idRoute,
        'start': response.start,
        'destino': response.end,
        'duration': duracion,
        'distancia': distancia,
        'price': response.price,
        'startDate': response.startdate
    }
    paypalrestsdk.configure({
        "mode": "sandbox",  # sandbox or live
        "client_id": "-",
        "client_secret": "-"})

    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "redirect_urls":
        {
            "return_url": "http://return_URL_here",
            "cancel_url": "http://cancel_URL_here"
        },
        "payer":
        {
            "payment_method": "paypal"
        },
        "transactions": [
            {
                "amount":
            {
                "total": context['price'],
                "currency": "EUR"
        },
        "description": "This is the payment transaction description."}]})

    if payment.create():

        return HttpResponseRedirect('http://127.0.0.1:8000/acept-route/'+idMessage)
    else:
        print(payment.error)

        return render(request, 'AppContent/home.html')
