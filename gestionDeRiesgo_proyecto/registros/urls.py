from django.urls import path, include
from . import views

urlpatterns = [
    path('crearUsuario/', views.crearUsuario, name='crearUsuario'),
    path('login/', views.iniciarSesion, name="login"),  
    path('configuracion_inicial/', views.actualizar_contraseña, name="n_configuracion_inicial"),
]
