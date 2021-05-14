from django.conf.urls import include, url
from . import views
from AppPay import views as appPay
from django.conf.urls import (
    handler400, handler403, handler404, handler500
)

handler400 = 'AppWeb.views.bad_request'
handler403 = 'AppWeb.views.permission_denied'
handler404 = 'AppWeb.views.page_not_found'
handler500 = 'AppWeb.views.server_error'

urlpatterns = [
        url(r'^logout/', views.Logout),
        url(r'^profile/', views.viewProfile),
        url(r'^createRoute/', views.createRoute),
        url(r'^saveProfile/', views.saveProfile),
        url(r'^route/(\d+)/$', views.getRouteDetails),
        url(r'^register-driver/', views.RegisterDriver),
        url(r'^driver-home/', views.DriverHome),
        url(r'^login-driver/', views.LoginDriver),
        url(r'^be-driver-message/(\d+)/$', views.sendMessageDriverToClient),
        url(r'^message/(\d+)/$', views.getMessageDetails),
        url(r'^messages-list', views.ReadMessages),
        url(r'^profile-user/(\d+)/$', views.getUserProfile),
        url(r'^acept-route/(\d+)/$', views.AceptRoute),
        url(r'^pay-route/(\d+)/$', appPay.DoPay),
        url(r'^puntuation-driver/$', views.PuntuationDriver),
        url(r'^delete-message/(\d+)/$', views.DeleteMessage),
        url(r'^delete-route/(\d+)/$', views.DeleteRoute),
        url(r'^saveVehicle/$', views.SaveVehicle),
        url(r'^delete-vehicle/$', views.DeleteVehicle),

]