from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import json
from django.contrib.auth.models import User
from .models import UsuarioAdmin, CambioContraseña
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
                es_damin = cambio_contraseña.es_admin
                cambio = cambio_contraseña.cambio

                if es_damin and cambio:
                    tipo = '1'
                elif cambio and not es_damin:
                    tipo = '2'
                elif es_damin and not cambio:
                    tipo = '3'
                
                return redirect(reverse('name_configuracion_inicial') +f'?tipo={tipo}')
            
            except CambioContraseña.DoesNotExist:
                error_message = 'error capo'
                return JsonResponse({'error':error_message})
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
@ensure_csrf_cookie  
def configuracion_inicial (request):
    tipo = request.GET.get('tipo')
    if tipo == '1':
        html_content_pass = '''
                            <h1>por favor cambie su contraseña e establezca una contraseña personal</h1>
                            <div class="form_group">
                                <label for="">nueva contraseña</label>
                                <input type="password" name="name_nueva_contraseña">
                            </div>
                            <div class="form_group">
                                <label for="">confirmar nueva contraseña</label>
                                <input type="password" name="name_confirmar_nueva_contraseña">
                            </div>
                            <div><input name="tipo" type="hidden" id="tipo" value="1"></div>
                            
                            '''
        html_content_pass_p =   '''
                            <div class="form_group">
                                <label for="">contraseña personal</label>
                                <input type="password" name="name_contraseña_personal">
                            </div>
                            <div class="form_group">
                                <label for="">confirmar contraseña personal</label>
                                <input type="password"name="name_confirmar_contraseña_personal">
                            </div>

                            
                            
                        '''
    elif tipo == '2':
        html_content_pass = '''
                            <h1>por favor cambie su contraseña e establezca una contraseña personal</h1>
                            <div class="form_group">
                                <label for="">nueva contraseña</label>
                                <input type="password" name="name_nueva_contraseña">
                            </div>
                            <div class="form_group">
                                <label for="">confirmar nueva contraseña</label>
                                <input type="password" name="name_confirmar_nueva_contraseña">
                            </div>
                            <div><input name="tipo" type="hidden" id="tipo" value="2"></div>'''
        html_content_pass_p = ''''''
    elif tipo == '3':
        return redirect('admin_login')
    return render(request, 'configuracion.html',{'html_content_pass':html_content_pass, 'html_content_pass_p': html_content_pass_p, 'tipo': tipo})

@ensure_csrf_cookie  
def validar_datos_login(request):
    if request.method == 'POST':
        nueva_contraseña = request.POST.get('name_nueva_contraseña', '')
        confirmar_contraseña = request.POST.get('name_confirmar_nueva_contraseña', '')
        contraseña_personal = request.POST.get('name_contraseña_personal', '')
        confirmar_contraseña_personal = request.POST.get('name_confirmar_contraseña_personal', '')
        tipo = request.POST.get ('tipo','')
        print(f'tipo: {tipo}')
        if tipo == '1':
            contraseña = ''
            contraseña_p = ''

            # Validación de la nueva contraseña
            if nueva_contraseña:
                if len(nueva_contraseña) < 7 or not re.search(r'[A-Z]', nueva_contraseña) or not re.search(r'\d', nueva_contraseña):
                    contraseña = 'La contraseña debe tener al menos 8 caracteres y contener al menos 1 número y 1 mayúscula.'
                else:
                    if confirmar_contraseña:
                        if nueva_contraseña != confirmar_contraseña:
                            contraseña = 'No coinciden las contraseñas.'
                        else:
                            contraseña = '''Las contraseñas coinciden.
                                            Contraseña cambiada con exito'''
                            estado_c = '1'
                            user = request.user
                            if user.is_authenticated:
                                user.set_password(nueva_contraseña)
                                user.save()
                                
                                usuario_cambio = CambioContraseña.objects.get(user=user)
                            
                                usuario_cambio.cambio = False
                                usuario_cambio.save()
                                print(usuario_cambio.cambio) 
                            
                    else:
                        contraseña = 'Por favor ingrese una confirmación de contraseña válida.'
                        estado_c = '0'
            else:
                contraseña = 'Por favor ingrese una contraseña válida.'
                estado_c = '0'
                

            # Validación de la contraseña personal
            if contraseña_personal:
                if confirmar_contraseña_personal:
                    if contraseña_personal != confirmar_contraseña_personal:
                        contraseña_p = 'No coinciden las contraseñas personales.'
                    else:
                        contraseña_p = '''Las contraseñas personales coinciden.
                                            Contraseña cambiada con exito'''
                        estado_p = '1'
                        user = request.user
                        contraseña_h = make_password(contraseña_personal)
                        print(f"Contraseña hasheada: {contraseña_h}")
                        usuario_admin = UsuarioAdmin(user=user, contraseña_personal=contraseña_h )
                        usuario_admin.save()
                else:
                    contraseña_p = 'Por favor ingrese una confirmación de contraseña personal válida.'
            else:
                contraseña_p = 'Por favor ingrese una contraseña personal válida.'
                estado_p = '0'
                
            
        elif tipo == '2':
             # Validación de la nueva contraseña
            if nueva_contraseña:
                if len(nueva_contraseña) < 7 or not re.search(r'[A-Z]', nueva_contraseña) or not re.search(r'\d', nueva_contraseña):
                    contraseña = 'La contraseña debe tener al menos 8 caracteres y contener al menos 1 número y 1 mayúscula.'
                    contraseña_p = ''
                else:
                    if confirmar_contraseña:
                        if nueva_contraseña != confirmar_contraseña:
                            contraseña = 'No coinciden las contraseñas.'
                            contraseña_p = ''
                        else:
                            contraseña = 'Las contraseñas coinciden.'
                            contraseña_p = ''
                    else:
                        contraseña = 'Por favor ingrese una confirmación de contraseña válida.'
                        contraseña_p = ''
            else:
                contraseña = 'Por favor ingrese una contraseña válida.'
                contraseña_p = ''
        data = {
            'contraseña': contraseña,
            'contraseña_p': contraseña_p,
        }
        return JsonResponse({'data': data})
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)
   

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
'''
@login_required
def admin_login(request):
    return render(request, 'admin_login.html')




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

def index (request):
    return render(request, 'index.html')

'''
                        contraseña_h = make_password(contraseña_personal)
                        user = request.user
                        if user.is_authenticated:
                            usuario_admin = get_object_or_404(UsuarioAdmin, user=user)
                            usuario_admin.contraseña_personal = (contraseña_h)
                            usuario_admin.save()
                            usuario_cambio = CambioContraseña.objects.get(user=user)
                            
                            usuario_cambio.cambio = False
                            usuario_cambio.save()
                            print(usuario_cambio.cambio)

                            user = request.user
                            if user.is_authenticated:
                                user.set_password(nueva_contraseña)
                                user.save()

'''