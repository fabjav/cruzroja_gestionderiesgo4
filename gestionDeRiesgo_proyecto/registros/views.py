from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import json
from django.contrib.auth.models import User
from .models import UsuarioAdmin, CambioContraseña, Pais, Provincia, Departamento, Distrito, Barrio, Calle, Casa, Persona
from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
import re

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

            try:
                cambio_contraseña = CambioContraseña.objects.get(user=user)
                
                cambio = cambio_contraseña.cambio

                if cambio:
                    return redirect(reverse('name_configuracion_inicial'))
                else:
                    return redirect(reverse('confirmar_admin'))
            except CambioContraseña.DoesNotExist:
                error_message = 'error capo'
                return JsonResponse({'error':error_message})
        else:
            error = '''El usuario o la contraseña son incorrectos'''
            return render(request, 'login.html',{'error':error})
    error = ''
    return render(request, 'login.html', {'error':error})

@ensure_csrf_cookie  
def configuracion_inicial (request):
    
    html_content_pass = '''
                            <h1>Por favor cambie su contraseña</h1>
                            <div class="form_group">
                                <label for="">nueva contraseña</label>
                                <input type="password" name="name_nueva_contraseña">
                            </div>
                            <div class="form_group">
                                <label for="">confirmar nueva contraseña</label>
                                <input type="password" name="name_confirmar_nueva_contraseña">
                            </div>
                            '''
     #este form se envia a url validar_datos_login
   
    return render(request, 'configuracion.html',{'html_content_pass':html_content_pass})

@login_required
def validar__datos_login(request):
    if request.method == 'POST':
        nueva_contraseña = request.POST.get('name_nueva_contraseña', '')
        confirmar_contraseña = request.POST.get('name_confirmar_nueva_contraseña', '')
        print(nueva_contraseña)
        print(confirmar_contraseña)
        if nueva_contraseña:
            if len(nueva_contraseña) < 7 or not re.search(r'[A-Z]', nueva_contraseña) or not re.search(r'\d', nueva_contraseña):
                html_content_1 = 'La contraseña debe tener al menos 8 caracteres y contener al menos 1 número y 1 mayúscula.'
                estado_confirmar = '0'
            else:
                if confirmar_contraseña:
                    if nueva_contraseña != confirmar_contraseña:
                        html_content_1 = 'Las contraseñas no coinciden'
                        estado_confirmar = '0'
                    else:
                        html_content_1 = 'Las contraseñas coinciden'
                        estado_confirmar = '1'
                        user = request.user
                        if user.is_authenticated:
                            user.set_password(nueva_contraseña)
                            user.save()
                            usuario_cambio = CambioContraseña.objects.get(user=user)
                            usuario_cambio.cambio = False
                            usuario_cambio.save()
                            print(usuario_cambio.cambio)
                else:
                    html_content_1 = 'Por favor ingrese una confirmación de contraseña válida.'
                    estado_confirmar = '0'
        else:
            html_content_1 = 'Por favor ingrese una contraseña válida.'
            estado_confirmar = '0'

        data = {
            'html_content_1': html_content_1,
            'estado_confirmar': estado_confirmar
        }
        return JsonResponse({'data': data})
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)
    
@ensure_csrf_cookie
@login_required
def confirmar_admin(request):
    user = request.user
    if user.is_authenticated:
        usuario_cambio = CambioContraseña.objects.get(user=user)
        es_admin = usuario_cambio.es_admin
        if es_admin:
            personal = UsuarioAdmin.objects.filter(user=user).exists() #busca si tiene contraseña personal
            if personal:
                return redirect(reverse('admin_login'))
                
                
            else:
                return redirect(reverse('crear_contraseña_personal'))
        else:
            return redirect('index')      
                

@ensure_csrf_cookie
@login_required
def crear_contraseña_personal(request):
    html_content_pass = '''<div>
                    <label for="">Contraseña Personal</label>
                    <input name="contraseña_personal" type="password">
                </div>
                <div>
                    <label for="">Confirmar contraseña personal</label>
                    <input name="confirmar_contraseña_personal" type="password">
                </div>'''
    return render(request, 'crear_contraseña_personal.html',{'html_content_pass':html_content_pass})


@ensure_csrf_cookie
@login_required
def validar_contraseña_personal(request):
    if request.method == 'POST':
        contraseña_personal = request.POST.get('contraseña_personal', '')
        confirmar_contraseña_personal = request.POST.get('confirmar_contraseña_personal', '')

        # Validación de la contraseña personal
        if contraseña_personal:
            if confirmar_contraseña_personal:
                if contraseña_personal != confirmar_contraseña_personal:
                    contraseña_p = 'No coinciden las contraseñas personales.'
                    estado = '0'
                else:
                    contraseña_p = 'Las contraseñas coinciden.'
                    estado = '1'
                    
                    user = request.user
                    contraseña_h = make_password(contraseña_personal)
                    print(f"Contraseña hasheada: {contraseña_h}")
                    usuario_admin = UsuarioAdmin(user=user, contraseña_personal=contraseña_h )
                    usuario_admin.save()
            else:
                contraseña_p = 'Por favor ingrese una confirmación de contraseña personal válida.'
                estado = '0'
        else:
            contraseña_p = 'Por favor ingrese una contraseña personal válida.'
            estado = '0'
           
        data = {
            'estado': estado,
            'contraseña_p': contraseña_p,
        }
        return JsonResponse({'data': data})
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)

                          
@ensure_csrf_cookie
@login_required
def admin_login(request):
    return render(request, 'admin_login.html')

@ensure_csrf_cookie
@login_required
def validar_datos_admin_login(request):
    if request.method == 'POST':
        contraseña_personal = request.POST.get('name_contraseña_personal')
        print(f'contraseña personal: {contraseña_personal}')
        user = request.user
        print(f"Usuario autenticado: {user}")  # Depuración
        if user.is_authenticated:
            try:
                usuario_admin = UsuarioAdmin.objects.get(user=user)
                print(f"Contraseña almacenada (hash): {usuario_admin.contraseña_personal}") # Depuración
                if check_password(contraseña_personal, usuario_admin.contraseña_personal):
                    print(check_password(contraseña_personal, usuario_admin.contraseña_personal))
                    return redirect('index')
                else:
                    print("Contraseña incorrecta")  # Depuración
                    return JsonResponse({'data': 'error'})
            except UsuarioAdmin.DoesNotExist:
                print("UsuarioAdmin no encontrado")  # Depuración
                return JsonResponse({'data': 'error'})
    else:
        return JsonResponse({'data': 'invalid_request'})


@ensure_csrf_cookie
@login_required
def index (request):
    return render(request, 'index.html')

def get_pais(request):
    paises = list(Pais.objects.values())
    if (len(paises)> 0):
        data = {'message':'Success', 'paises': paises}
    else:
        data = {'message': 'Paises not found'}
    
    return JsonResponse(data)

def get_provincia(request, pais_id):
    provincias = list(Provincia.objects.filter(pais=pais_id).values())

    if (len(provincias)>0):
        data = {'message': 'Success', 'provincias': provincias}
    else:
        data = {'message': 'Provincias not found'}
    return JsonResponse(data)

def get_departamento(request, provincia_id):
    departamentos = list(Departamento.objects.filter(provincia_id=provincia_id).values())

    if (len(departamentos)>0):
        data = {'message':'Success', 'departamentos': departamentos}
    else:
        data = {'message': 'Departamentos not found'}
    return JsonResponse(data)

def get_distrito(request, departamento_id):
    distritos = list(Distrito.objects.filter(departamento_id=departamento_id).values())

    if (len(distritos) >0):
        data = {'message':'Success', 'distritos': distritos}
    else:
        data = {'message': 'Distritos not found'}
    return JsonResponse(data)

def get_barrio(request, distrito_id):
    barrios = list(Barrio.objects.filter(distrito_id=distrito_id).values())

    if (len(barrios)>0):
        data = {'message': 'Success', 'barrios':barrios}
    else:
        data = {'message': 'Barrios not found'}
    return JsonResponse(data)

def get_casa(request, barrio_id):
    casas = list(Casa.objects.filter(barrio_id=barrio_id).values())

    if (len(casas)>0):
        data = {'message': 'Success', 'casas': casas}
    else:
        data = {'message': 'Casas not found'}
    return JsonResponse(data)

def get_personas(request, casa_id):
    personas = list(Casa.objects.filter(casa_id=casa_id).values())

    if (len(personas)>0):
        data = {'message': 'Succes', 'personas':personas}
    else:
        data = {'message': 'Personas not found'}
    return JsonResponse(data)