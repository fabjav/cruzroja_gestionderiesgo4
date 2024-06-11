from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import json
from django.contrib.auth.models import User
from .models import UsuarioAdmin, CambioContraseña
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.shortcuts import redirect

@login_required
def crearUsuario(request):
    
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        email = request.POST.get('email')
        usuario = request.POST.get('usuario')
        contraseña = request.POST.get('contraseña')
        admin = request.POST.get('admin')

        if not nombre or not apellido or not email or not usuario or not contraseña:
            error_message = 'Faltan datos. Por favor Complete'
            return JsonResponse({'error_message': error_message})
        if User.objects.filter(username=usuario).exists():
            error_message = 'El usuario ya existe.'
            return JsonResponse({'error_message': error_message})
        
        try:
            nuevo_usuario = User.objects.create_user(username=usuario, email=email, password=contraseña)

            nuevo_usuario.first_name = nombre
            nuevo_usuario.last_name = apellido
            nuevo_usuario.save()
            
            if admin:
                cambio_contraseña = CambioContraseña(user=nuevo_usuario, cambio=True, es_admin=True )
                cambio_contraseña.save()
                '''
                contraseña_personal = 'df3r5fr1688'
                contraseña_encriptada = make_password(contraseña_personal)
                crear_contraseña_personal = UsuarioAdmin(user=nuevo_usuario, contraseña_personal=contraseña_encriptada)
                crear_contraseña_personal.save()'''
            else:
                cambio_contraseña = CambioContraseña(user=nuevo_usuario, cambio=True, es_admin=False)
                cambio_contraseña.save()

            succes_message = 'Creado con exito'
            return JsonResponse( {'message': succes_message})

        except Exception as e:
            error_message = f'Error al crear usuario: {str(e)}.'
            return JsonResponse({'error_message': error_message})
         
    else:
        return render(request, 'crearUsuario.html')
    
@ensure_csrf_cookie   
def iniciarSesion(request):
    if request.method == 'POST':
        username = request.POST.get('usuario')
        password = request.POST.get('contraseña')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
    return render(request, 'login.html')
'''
            try:
                cambio_contraseña = CambioContraseña.objects.get(user=user)
                es_admin = cambio_contraseña.es_admin
                cambio = cambio_contraseña.cambio
                
                response_data = {
                    'es_admin': es_admin,
                    'primer_login': cambio,
                }
                return JsonResponse({'data': response_data})

            except CambioContraseña.DoesNotExist:
                error_message = 'Error. Datos no válidos.'
                return JsonResponse({'error_message': error_message})

        error_message = 'Error. Datos no válidos.'
        return JsonResponse({'error_message': error_message})
'''
    

@login_required
def actualizar_contraseña(request):
    if request.method == 'POST':
        nueva_contraseña = request.POST.get('contraseña_nueva')
        confirmar_contra = request.POST.get('confirmar_contraseña_nueva')
        tipo = request.GET.get('tipo')
        print(tipo) 
        return JsonResponse({'tipo': tipo})
    else:
        tipo = request.GET.get('tipo')
        return render(request, 'configuracion.html', {'tipo': tipo})

@login_required
def cambiar_pass_passPersonal(request):
    if request.method == 'POST':

       
       
       print()
    return render(request, 'configuracion.html')