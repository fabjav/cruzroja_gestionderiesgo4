from django.urls import path, include
from . import views

urlpatterns = [
    path('crearUsuario/', views.crearUsuario, name='crearUsuario'),
    path('login/', views.iniciarSesion, name="name_login"),  
    path('configuracion_inicial/', views.configuracion_inicial, name="name_configuracion_inicial"),
    path('validar_datos_login/', views.validar__datos_login, name="validar_datos_login"),
    path('', views.index, name="index"),
    path('admin_login/', views.admin_login, name="admin_login"),
    path('validar_datos_admin_login/', views.validar_datos_admin_login, name="validar_datos_admin_login"),
    path('validar_contraseña_personal/', views.validar_contraseña_personal, name="validar_contraseña_personal"),
    path('crear_contraseña_personal/', views.crear_contraseña_personal, name="crear_contraseña_personal"),
    path('confirmar_admin/', views.confirmar_admin, name="confirmar_admin"),
    path('get_pais/', views.get_pais, name="get_pais"),
    path('get_provincia/<int:pais_id>', views.get_provincia, name="get_provincia"),
    path('get_departamento/<int:provincia_id>', views.get_departamento, name='get_departamento'),
    path('get_distrito/<int:departamento_id>', views.get_distrito, name="get_distrito"),
    path('get_barrio/<int:distrito_id>', views.get_barrio, name="get_barrio"),
    path('get_casa/<int:barrio_id>', views.get_casa, name="get_casa"),
    path('get_persona/', views.get_personas, name="get_persona")
]
