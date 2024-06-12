from django.urls import path, include
from . import views

urlpatterns = [
    path('crearUsuario/', views.crearUsuario, name='crearUsuario'),
    path('login/', views.iniciarSesion, name="name_login"),  
    path('configuracion_inicial/', views.configuracion_inicial, name="name_configuracion_inicial"),
    path('validar_datos_login/', views.validar_datos_login, name="validar_datos_login"),
    path('', views.index, name="index"),
]
