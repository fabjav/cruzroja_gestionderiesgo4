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
    print(barrios)
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
    try:
        casa = get_object_or_404(Casa, id=casa_id)
        personas = Persona.objects.filter(casa=casa)
        personas_data = []
        for persona in personas:
            padecimientos = persona.padecimientos.all()
            padecimientos_list = [padecimiento.nombre for padecimiento in padecimientos]
            rol_nombre = persona.rol.nombre if persona.rol else None  # Obtener el nombre del rol o None si no hay rol
            personas_data.append({
                'id': persona.id,
                'nombre': persona.nombre,
                'apellido': persona.apellido,
                'fecha_nac': persona.fecha_nac,
                'rol': rol_nombre,
                'casa': {
                    'nombre': persona.casa.nombre,
                    'calle': persona.casa.calle.nombre,
                    'numero': persona.casa.numero,
                    'barrio': persona.casa.barrio.nombre,
                },
                'telefono_emergencia': persona.telefono_emergencia,
                'padecimientos': padecimientos_list,
                'medicamento': persona.medicamento,
                'dosis': persona.dosis,
            })
            print(persona.casa.calle.nombre)
        data = {'message': 'Success', 'personas': personas_data}
        
    except Casa.DoesNotExist:
        data = {'message': 'Casa not found'}
    
    return JsonResponse(data)

def get_all_persona(request):
    try:
        
        personas = Persona.objects.values()
        personas_data = []
        for persona in personas:
            padecimientos = persona.padecimientos.all()
            padecimientos_list = [padecimiento.nombre for padecimiento in padecimientos]
            rol_nombre = persona.rol.nombre if persona.rol else None  # Obtener el nombre del rol o None si no hay rol
            personas_data.append({
                'id': persona.id,
                'nombre': persona.nombre,
                'apellido': persona.apellido,
                'fecha_nac': persona.fecha_nac,
                'rol': rol_nombre,
                'casa': {
                    'nombre': persona.casa.nombre,
                    'calle': persona.casa.calle.nombre,
                    'numero': persona.casa.numero,
                    'barrio': persona.casa.barrio.nombre,
                },
                'telefono_emergencia': persona.telefono_emergencia,
                'padecimientos': padecimientos_list,
                'medicamento': persona.medicamento,
                'dosis': persona.dosis,
            })
            print(persona.casa.calle.nombre)
        data = {'message': 'Success', 'personas': personas_data}
        
    except Casa.DoesNotExist:
        data = {'message': 'Casa not found'}
    
    return JsonResponse(data)

def crear_barrio(request):
    if request.method == 'GET':
        distritos = Distrito.objects.all()

        # Construir las opciones del select
        options = []
        for distrito in distritos:
            options.append(f'<option class="options_form" value="{distrito.id}">{distrito.nombre}</option>')

        # HTML con el select y las opciones
        html_content = f'''
            <h3 style="color: white" >Crear Barrio</h3>
            <input class="cerrar" id="cerrarVentana_1" type="button" value="&times;">
            <div >
                <input class="input_form" type="text" name="nombre_barrio" placeholder="NOMBRE DEL BARRIO">
            </div>
            <div>
                <input class="input_form"  type="text" name="coordenadas_barrio" placeholder="COORDENADAS">
            </div>
            <div>
                
                <select class="form_select" name="distrito" id="id_distrito">
                    <option value="" disabled selected hidden >Selecciona un distrito</option>
                    {''.join(options)}
                </select>
            </div>
            <div id="id_boton_enviar_form" >
                    <button class="btn_form_group" type="submit">Enviar</button>
                </div>
                
        '''

        data = {'message': 'Success', 'html_content': html_content}
        return JsonResponse(data)
    #post
    elif request.method == 'POST':
        print('metodo post')
        nombre_barrio = request.POST.get('nombre_barrio', '')
        coordenadas = request.POST.get('coordenadas_barrio','')
        distrito_id = request.POST.get('distrito','')

        if nombre_barrio and coordenadas and distrito_id:
            try:
                distrito = Distrito.objects.get(pk=distrito_id)
                print(distrito)
            except Distrito.DoesNotExist:
                return JsonResponse({'message': 'Dont Found'}, status=400)
            
            existe_barrio = Barrio.objects.filter(nombre=nombre_barrio, coordenadas=coordenadas).exists()
            if existe_barrio:
                return JsonResponse({'message': 'Exist'}, status=400)
            
            nuevo_barrio = Barrio.objects.create(
                nombre=nombre_barrio,
                coordenadas=coordenadas,
                distrito=distrito
            )    
            message = 'Success'
            return JsonResponse({'message':message}) 
        else:
            message = 'Error'
            return JsonResponse({'message': message})
        

def crear_casa(request, barrio_id):
    if request.method == 'GET':
        calles = Calle.objects.all()

        # Construir las opciones del select
        options_calle = []
        for calle in calles:
            options_calle.append(f'<option class="options_form" value="{calle.id}">{calle.nombre}</option>')
        barrio = Barrio.objects.get(pk=barrio_id)
        print(barrio)
        # HTML con el select y las opciones
        html_content = f'''
            <h3 style="color: white" >Crear Casa</h3>
            <h3 style="color: white" >en barrio {barrio}</h3>
            <input class="cerrar" id="cerrarVentana_2" type="button" value="&times;">
            <div >
                <input autocomplete="off" class="input_form" type="text" name="nombre_casa" placeholder="IDENTIFICADOR">
            </div>
            <div>
                <input autocomplete="off" class="input_form"  type="text" name="numero_casa" placeholder="NÚMERO">
            </div>
            
           <div id="autocomplete-suggestions" class="autocomplete-suggestions">
                    <input autocomplete="off" name="calle" class="input_form" type="text" id="autocomplete_input" placeholder="CALLE">
                </div>
            
            <div id="id_boton_enviar_form" >
                    <button class="btn_form_group" type="submit">enviar</button>
                </div>
                 
        '''

        data = {'message': 'Success', 'html_content': html_content}
        return JsonResponse(data)
    #post
    elif request.method == 'POST':
        print('metodo post')
        nombre_casa = request.POST.get ('nombre_casa','')
        numero = request.POST.get('numero_casa','')
        calle = request.POST.get('calle','')
        barrio_id = request.POST.get('barrio','')

        if nombre_casa and numero and calle and barrio_id:
            try:
                
                barrio = Barrio.objects.get(pk=barrio_id)
                print(barrio)
            except Barrio.DoesNotExist:
                return JsonResponse({'message': 'Dont Found'}, status=400)
            try:
                calle = Calle.objects.get(nombre=calle)
                print(calle)
            except Calle.DoesNotExist:
                return JsonResponse({'message': 'Dont Found'}, statu=400)
            existe_casa = Casa.objects.filter(nombre=nombre_casa, numero=numero).exists()
            if existe_casa:
                return JsonResponse({'message': 'Exist'}, status=400)
            
            nueva_casa = Casa.objects.create(
                nombre=nombre_casa,
                numero=numero,
                barrio=barrio,
                calle=calle
            )    
            message = 'Success'
            return JsonResponse({'message':message}) 
        else:
            message = 'Error'
            return JsonResponse({'message': message})
'''
<div>
                                
               <div>
                <select class="form_select" name="calle" id="id_calle">
                    <option value="" disabled selected hidden >Selecciona una calle</option>
                    {''.join(options_calle)}
                </select>            
            </div>
'''

def buscar_calles(request):
    term = request.GET.get('term', '')
    calles = Calle.objects.filter(nombre__icontains=term)[:10]  # Cambia esto por tu lógica de búsqueda
    results = [{'label': calle.nombre, 'value': calle.nombre} for calle in calles]
    return JsonResponse(results, safe=False)