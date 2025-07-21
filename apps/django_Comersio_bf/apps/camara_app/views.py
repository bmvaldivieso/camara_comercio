# proyectoUno/views.py
from django.shortcuts import render
import logging
from django.contrib.auth.decorators import login_required

from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.permissions import BasePermission

from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.db.models import Prefetch

from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import redirect, render
from django.contrib import messages
from .forms import SocioPersonalForm, SocioBusinessForm, SocioActivityContactForm, InformacionSeguroSocioForm
from .forms import SolicitudSeguroVidaForm, DeclaracionSaludForm, DeporteActividadForm, BeneficiarioForm

from django.contrib.auth import logout as auth_logout
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponse


from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login








"""
# Esto te da el endpoint para obtener el token al hacer login
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['is_superuser'] = self.user.is_superuser
        return data
    
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class IsSuperUser(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_superuser


"""























@csrf_protect
def logout_view(request):
    if request.method == "POST":
        auth_logout(request)
        response = redirect('/login')
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        return response
    return HttpResponse(status=400)




def login(request):
    logging.warning("Login requestttttt")
    
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Login de sesión clásica
            auth_login(request, user)

            # Crear token JWT usando RefreshToken
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            is_superuser = user.is_superuser

            context = {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "is_superuser": is_superuser
            }
            print(context)
            return redirect('/categorias')

        else:
            logging.warning("Usuario o contraseña incorrectos.")
            messages.error(request, "Usuario o contraseña incorrectos.")

    return render(request, 'auth/login/login.html')





def register(request):
    logging.warning("Register requestttttt")
    
    if request.method == "POST":
        nombres = request.POST.get("nombres")
        apellidos = request.POST.get("apellidos")
        cedula = request.POST.get("cedula")
        usuario = request.POST.get("usuario")
        contrasena = request.POST.get("contrasena")
        correo = request.POST.get("correo")
        imagen = request.FILES.get("imagen")
        
        user = User.objects.create_user(username=usuario, password=contrasena, first_name=nombres, last_name=apellidos, email=correo)
        user.is_superuser = False
        user.is_staff = False
        user.is_active = True
        user.save()
        perfil_usuario = PerfilUsuario.objects.create(user=user, cedula=cedula,imagen=imagen)
        perfil_usuario.save()

        user = authenticate(request, username=usuario, password=contrasena)

        if user is not None:
            auth_login(request, user)

            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            is_superuser = user.is_superuser

            context = {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "is_superuser": is_superuser
            }
            print(context)
            messages.success(request, "Usuario creado exitosamente.")
            return redirect('/present_Socio')

        else:
            logging.warning("Usuario no creado.")
            messages.error(request, "Usuario no creado.")

    return render(request, 'auth/register/register.html')



# Create your views here.
def index(request):
    return render(request, 'index.html')






@login_required(login_url='/login')
def ser_socio(request):
    logging.warning("Ser Socio requestttttt")
    if request.method == 'POST':
        personal_form = SocioPersonalForm(request.POST)
        business_form = SocioBusinessForm(request.POST)
        activity_contact_form = SocioActivityContactForm(request.POST)
        seguro_form = InformacionSeguroSocioForm(request.POST)

        all_forms_valid = personal_form.is_valid() and business_form.is_valid() and activity_contact_form.is_valid() and seguro_form.is_valid()

        if all_forms_valid:
            logging.warning("Todos los formularios son válidos. Recopilando datos...")

            beneficiario = BeneficiarioSeguro.objects.create(nombre_completo=seguro_form.cleaned_data['nombre_beneficiario'], porcentaje=seguro_form.cleaned_data['porcentaje_beneficiario'])
            beneficiario.save()
            info_seguro = InformacionSeguroSocio.objects.create(nombre_titular=seguro_form.cleaned_data['nombre_titular'], telefono_titular=seguro_form.cleaned_data['telefono_titular'], fecha_nacimiento_titular=seguro_form.cleaned_data['fecha_nacimiento_titular'], cedula_titular=seguro_form.cleaned_data['cedula_titular'], firma_titular=seguro_form.cleaned_data['firma_titular'], id_beneficiario=beneficiario)
            info_seguro.save()
            socio = Socio.objects.create(
                razon_social=personal_form.cleaned_data['razon_social'],
                nombre_comercial=personal_form.cleaned_data['nombre_comercial'],
                ruc_cedula=personal_form.cleaned_data['ruc_cedula'],
                email_principal=personal_form.cleaned_data['email_principal'],
                redes_sociales=personal_form.cleaned_data['redes_sociales'],
                cedula_representante=business_form.cleaned_data['cedula_representante'],
                apellidos_nombres_representante=business_form.cleaned_data['apellidos_nombres_representante'],
                direccion_principal=business_form.cleaned_data['direccion_principal'],
                calle=business_form.cleaned_data['calle'],
                numero=business_form.cleaned_data['numero'],
                interseccion=business_form.cleaned_data['interseccion'],
                referencia=business_form.cleaned_data['referencia'],
                parroquia=business_form.cleaned_data['parroquia'],
                ciudad=business_form.cleaned_data['ciudad'],
                pais=business_form.cleaned_data['pais'],
                pagina_web=business_form.cleaned_data['pagina_web'],
                email_empresa=business_form.cleaned_data['email_empresa'],
                telefono1=business_form.cleaned_data['telefono1'],
                telefono2=business_form.cleaned_data['telefono2'],
                celular=business_form.cleaned_data['celular'],
                tipo_negocio=activity_contact_form.cleaned_data['tipo_negocio'],
                actividad_especifica=activity_contact_form.cleaned_data['actividad_especifica'],
                representante_contacto=activity_contact_form.cleaned_data['representante_contacto'],
                propietario_contacto=activity_contact_form.cleaned_data['propietario_contacto'],
                id_seguro=info_seguro
            )
            socio.save()
            logging.warning(f"Socio creado exitosamente: {socio}")
            return redirect('categorias')

        else:
            logging.error("Algunos formularios no son válidos. Errores:")
            if personal_form.errors:
                logging.error(f"Errores en Personal Form: {personal_form.errors}")
            if business_form.errors:
                logging.error(f"Errores en Business Form: {business_form.errors}")
            if activity_contact_form.errors:
                logging.error(f"Errores en Activity/Contact Form: {activity_contact_form.errors}")
            if seguro_form.errors:
                logging.error(f"Errores en Seguro Form: {seguro_form.errors}")

            context = {'personal_form': personal_form,'business_form': business_form,'activity_contact_form': activity_contact_form,'seguro_form': seguro_form,}
            return render(request, 'components/socio/registerSocio/ser_socio.html', context)

    else: 
        personal_form = SocioPersonalForm()
        business_form = SocioBusinessForm()
        activity_contact_form = SocioActivityContactForm()
        seguro_form = InformacionSeguroSocioForm()

        context = {'personal_form': personal_form,'business_form': business_form,'activity_contact_form': activity_contact_form,'seguro_form': seguro_form,}
    return render(request, 'components/socio/registerSocio/mainSocio.html', context) 






#faltan 3 cosas arregla tercera aunque sea el fin de semana priemro lugar fecha y segundo no s emarcan en true las
#preguntas.
def solicitud_seguro_form(request):
    logging.warning("Solicitud de formulario de seguro")
    
    if request.method == 'POST':
        form_solicitud = SolicitudSeguroVidaForm(request.POST)
        form_salud = DeclaracionSaludForm(request.POST)
        form_deporte = DeporteActividadForm(request.POST)
        form_beneficiario = BeneficiarioForm(request.POST)

        forms_valid = True
        
        if not form_solicitud.is_valid():
            forms_valid = False
            logging.error(f"Errores en Solicitud: {form_solicitud.errors}")
            
        if not form_salud.is_valid():
            forms_valid = False
            logging.error(f"Errores en Salud: {form_salud.errors}")
            
        if not form_deporte.is_valid():
            forms_valid = False
            logging.error(f"Errores en Deporte: {form_deporte.errors}")
            
        if not form_beneficiario.is_valid():
            forms_valid = False
            logging.error(f"Errores en Beneficiario: {form_beneficiario.errors}")
    
        
        if forms_valid:

            logging.warning("Todos los formularios son válidos. Recopilando datos...")
               # ===== SECCIÓN I: DATOS DEL SOLICITANTE =====
            seccion1 = {
                'tipo_identificacion': form_solicitud.cleaned_data['tipo_identificacion'],
                'numero_identificacion': form_solicitud.cleaned_data['numero_identificacion'],
                'nombres': form_solicitud.cleaned_data['nombres'],
                'apellidos': form_solicitud.cleaned_data['apellidos'],
                'fecha_nacimiento': form_solicitud.cleaned_data['fecha_nacimiento'],
                'estado_civil': form_solicitud.cleaned_data['estado_civil'],
                'direccion_domicilio': form_solicitud.cleaned_data['direccion_domicilio'],
                'correo_domicilio': form_solicitud.cleaned_data['correo_domicilio'],
                'telefono_domicilio': form_solicitud.cleaned_data['telefono_domicilio'],
                'celular_domicilio': form_solicitud.cleaned_data['celular_domicilio'],
                'nombre_empresa': form_solicitud.cleaned_data['nombre_empresa'],
                'direccion_trabajo': form_solicitud.cleaned_data['direccion_trabajo'],
                'correo_trabajo': form_solicitud.cleaned_data['correo_trabajo'],
                'telefono_trabajo': form_solicitud.cleaned_data['telefono_trabajo'],
                'ocupacion': form_solicitud.cleaned_data['ocupacion'],
                'envio_correspondencia': form_solicitud.cleaned_data['envio_correspondencia'],
                'otros_seguros_vida': form_solicitud.cleaned_data['otros_seguros_vida'],
                'especifique_companias_otros_seguros': form_solicitud.cleaned_data['especifique_companias_otros_seguros'],
                'es_usted': form_solicitud.cleaned_data['es_usted'],
                'lugar_firma': form_solicitud.cleaned_data['lugar_firma'],
                'firma_electronica_generada': form_solicitud.cleaned_data['firma_electronica_generada']
            }
            
            # ===== SECCIÓN II: DECLARACIÓN DE SALUD =====
            seccion2 = {
                'peso_kg': form_salud.cleaned_data['peso_kg'],
                'estatura_cm': form_salud.cleaned_data['estatura_cm'],
                'tension_arterial_sistolica': form_salud.cleaned_data['tension_arterial_sistolica'],
                'tension_arterial_diastolica': form_salud.cleaned_data['tension_arterial_diastolica'],
                'peso_ha_cambiado': form_salud.cleaned_data['peso_ha_cambiado'],
                'cuanto_peso_cambio': form_salud.cleaned_data['cuanto_peso_cambio'],
                'peso_cambio_intencional': form_salud.cleaned_data['peso_cambio_intencional'],
                'causa_peso_cambio': form_salud.cleaned_data['causa_peso_cambio'],
                'fuma': form_salud.cleaned_data['fuma'],
                'cantidad_fumada': form_salud.cleaned_data['cantidad_fumada'],
                'consume_alcohol': form_salud.cleaned_data['consume_alcohol'],
                'cuales_alcohol': form_salud.cleaned_data['cuales_alcohol'],
                'cuanto_diariamente_alcohol': form_salud.cleaned_data['cuanto_diariamente_alcohol'],
                'uso_estupefacientes': form_salud.cleaned_data['uso_estupefacientes'],
                'cuales_estupefacientes': form_salud.cleaned_data['cuales_estupefacientes'],
                'hasta_cuando_estupefacientes': form_salud.cleaned_data['hasta_cuando_estupefacientes'],
                'toma_anticonceptivos': form_salud.cleaned_data['toma_anticonceptivos'],
                'esta_embarazada': form_salud.cleaned_data['esta_embarazada'],
                'cuantos_meses_embarazo': form_salud.cleaned_data['cuantos_meses_embarazo'],
                'enfermedad_ginecologica': form_salud.cleaned_data['enfermedad_ginecologica'],
                'medico_cabecera': form_salud.cleaned_data['medico_cabecera'],
                'medico_ultima_vez': form_salud.cleaned_data['medico_ultima_vez'],
                'cuando_ultima_vez': form_salud.cleaned_data['cuando_ultima_vez'],
                'motivo_ultima_vez': form_salud.cleaned_data['motivo_ultima_vez'],
                'otra_declaracion_salud': form_salud.cleaned_data['otra_declaracion_salud'],
            }

            # ===== SECCIÓN III: DEPORTES Y ACTIVIDADES =====
            seccion3 = {
                'nombre_actividad': form_deporte.cleaned_data['nombre_actividad'],
                'con_competicion': form_deporte.cleaned_data['con_competicion'],
                'es_piloto': form_deporte.cleaned_data['es_piloto'],
                'paracaidismo': form_deporte.cleaned_data['paracaidismo']
            }

            # ===== SECCIÓN IV: BENEFICIARIOS =====
            seccion4 = {
                'nombres_completos': form_beneficiario.cleaned_data['nombres_completos'],
                'direccion': form_beneficiario.cleaned_data['direccion'],
                'fecha_nacimiento': form_beneficiario.cleaned_data['fecha_nacimiento'],
                'parentesco': form_beneficiario.cleaned_data['parentesco'],
                'cedula_identidad': form_beneficiario.cleaned_data['cedula_identidad'],
                'porcentaje': form_beneficiario.cleaned_data['porcentaje']
            }
            
            # ===== SECCIÓN V: DECLARACIONES =====
            
            logging.warning("\n=== SECCIÓN V: DECLARACIONES ===")
            logging.warning("Declaraciones legales aceptadas")
            logging.warning(f"Lugar de firma: {seccion1['lugar_firma']}")
            logging.warning(f"Fecha de firma: {form_solicitud.instance.obtener_fecha_actual()}")
            logging.warning(f"Firma electrónica generada: {'Sí' if seccion1['firma_electronica_generada'] else 'No'}")
        

            solicitud = SolicitudSeguroVida.objects.create(**seccion1)
            solicitud.save()
            perfil = request.user.perfil
            perfil.id_solicitud = solicitud
            perfil.save()

            seccion2['solicitud'] = solicitud
            declaracion_salud = DeclaracionSalud.objects.create(**seccion2)
            declaracion_salud.save()
            deport = DeporteActividad.objects.create(solicitud=solicitud, **seccion3)
            deport.save()
            beneficiario = Beneficiario.objects.create(solicitud=solicitud, **seccion4)
            beneficiario.save()

            return redirect('categorias')
            
        else:
            messages.error(request, "Por favor complete todos los campos requeridos correctamente.")
            
        context = {'form_solicitud': form_solicitud,'declaracion_salud_form': form_salud,'deporte_actividad_form': form_deporte,'beneficiario_form': form_beneficiario}
        return render(request, 'components/forms/solicitud_seguro_form.html', context)

    else:
        context = {'form_solicitud': SolicitudSeguroVidaForm(),'declaracion_salud_form': DeclaracionSaludForm(),'deporte_actividad_form': DeporteActividadForm(),'beneficiario_form': BeneficiarioForm()}
        return render(request, 'components/forms/solicitud_seguro_form.html', context)



@login_required(login_url='/login')
def present_Socio(request):
    return render(request, 'components/socio/present_Socio.html')









@login_required(login_url='/login')
def categorias(request):
    return render(request, 'components/categories/categorias.html')
    
@login_required(login_url='/login')
def servicios(request):
    logging.warning("Servicios requestttttt")
    return render(request, 'components/services/servicios.html')
@login_required(login_url='/login')
def subservicios(request):
    logging.warning("Subservicios requestttttt")
    return render(request, 'components/subservicios/subservicios.html')
@login_required(login_url='/login')
def masteradmin(request):
    return render(request, 'admin/master/masteradmin.html')
@login_required(login_url='/login')
def dashboard(request):
    return render(request, 'admin/dashboard/dashboard.html')
@login_required(login_url='/login')
def admin_usuarios(request):
    return render(request, 'admin/usuarios/usuarios.html')
@login_required(login_url='/login')
def admin_usuarios_incremento(request):
    return render(request, 'admin/usuarios/usuarios_incremento.html')    
@login_required(login_url='/login')
def admin_socios(request):
    return render(request, 'admin/socios/socios.html')
@login_required(login_url='/login')
def admin_socios_formularios(request):
    return render(request, 'admin/socios/socios_formularios.html')
@login_required(login_url='/login')
def seguro_vida(request):
    logging.warning("Seguro Vida requestttttt")
    return render(request, 'components/subservicios/seguroVida/seguro_vida.html')
@login_required(login_url='/login')
def seguro_vida_archivos_subidos(request):
    return render(request, 'components/subservicios/seguroVida/seguro_vida_archivos_subidos.html')
@login_required(login_url='/login')
def seguro_vida_archivos_recibidos(request):
    return render(request, 'components/subservicios/seguroVida/seguro_vida_archivos_recibidos.html')
@login_required(login_url='/login')
def seguro_vida_estado(request):
    return render(request, 'components/subservicios/seguroVida/seguro_vida_estado.html')
@login_required(login_url='/login')
def formularios(request):
    return render(request, 'components/forms/formularios_main.html')
@login_required(login_url='/login')
def formularios_form_a(request):
    return render(request, 'components/forms/formularios_form_a.html')
@login_required(login_url='/login')
def formularios_form_b(request):
    return render(request, 'components/forms/formularios_form_b.html')     


