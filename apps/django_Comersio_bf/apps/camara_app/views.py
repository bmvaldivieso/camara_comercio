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
from .forms import SocioPersonalForm, SocioBusinessForm, SocioActivityContactForm, InformacionSeguroSocioForm,CategoriaForm,ServicioForm,SubservicioForm,FormProductoForm
from .forms import SolicitudSeguroVidaForm, DeclaracionSaludForm, DeporteActividadForm, BeneficiarioForm, FormProductoVidaForm

from django.contrib.auth import logout as auth_logout
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponse


from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen import canvas
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
from io import BytesIO
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string


from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import get_object_or_404
from .models import PerfilUsuario
from .forms import MensajeForm
from .forms import PublicacionForm
from .forms import ImagenPublicacionForm
from .models import ImagenPublicacion
from django.forms.models import modelformset_factory
from django.views.decorators.http import require_POST

from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseForbidden
import pusher







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
            auth_login(request, user)

            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            is_superuser = user.is_superuser
            print(f"Superuser: {user.is_superuser}")

            context = {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "is_superuser": is_superuser
            }
            print(context)

            if is_superuser:
                return redirect('/dashboard')
            else:
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
                activo=False,
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

    categorias = Categorias.objects.all()
    context = {'categorias': categorias}
    return render(request, 'components/categories/categorias.html', context)



@login_required(login_url='/login')
def servicios(request, categoria_id):
    logging.warning("Servicios requestttttt")
    servicios = Servicios.objects.filter(categorias__id=categoria_id).all()
    context = {'servicios': servicios,'categoria_id':categoria_id}
    return render(request, 'components/services/servicios.html', context)



@login_required(login_url='/login')
def subservicios(request,servicio_id,categoria_id):
    logging.warning("Subservicios requestttttt")
    subservicios = Subservicios.objects.filter(servicios__id=servicio_id).all()
    context ={'subservicios':subservicios,'servicio_id':servicio_id,'categoria_id':categoria_id}
    return render(request, 'components/subservicios/subservicios.html', context)


from django.http import FileResponse
from datetime import datetime

@login_required(login_url='/login')
def seguro_vida(request, servicio_id, producto_id,categoria_id):
    producto = Producto.objects.get(id=producto_id)
    perfil = request.user.perfil

    if request.method == 'POST':
        data = request.POST

        formulario = FormularioProductoVida.objects.create(
            perfil=perfil,
            producto=producto,
            tiene_enfermedad_grave=bool(data.get('tiene_enfermedad_grave')),
            ha_sido_hospitalizado=bool(data.get('ha_sido_hospitalizado')),
            practica_deportes_extremos=bool(data.get('practica_deportes_extremos')),
            nombre_beneficiario=data.get('nombre_beneficiario'),
            relacion_beneficiario=data.get('relacion_beneficiario'),
            porcentaje_beneficiario=data.get('porcentaje_beneficiario'),
            acepta_terminos=bool(data.get('acepta_terminos')),
            estado=bool(False),
            fecha_registro=datetime.now(),
        )
        formulario.save()   
        logging.warning("Formulario guardado exitosamente")
        pdf_buffer = generar_poliza_pdf(perfil, formulario)
        return FileResponse(pdf_buffer, as_attachment=True, filename='poliza_seguro_vida.pdf')
    context = {'servicio_id': servicio_id,'producto': producto,'categoria_id':categoria_id}
    return render(request, 'components/subservicios/seguroVida/seguro_vida.html', context)


def generar_poliza_pdf(perfil, formulario):
    html_string = render_to_string("components/subservicios/seguroVida/pdf/poliza_vida.html", {'perfil': perfil,'formulario': formulario})
    pdf_file = BytesIO()
    HTML(string=html_string).write_pdf(pdf_file)
    pdf_file.seek(0)
    return pdf_file






@login_required(login_url='/login')
def firma(request,servicio_id,producto_id,categoria_id):
    logging.warning("Firma requestttttt")
    producto = Producto.objects.get(id=producto_id)
    context ={'servicio_id':servicio_id,'producto':producto,'categoria_id':categoria_id}
    return render(request, 'components/subservicios/firmaElectronica/firma.html',context)


@login_required(login_url='/login')
def productos_carrito(request):
    perfil = request.user.perfil
    productos = perfil.productos.all() 
    data = []

    for producto in productos:
        data.append({'titulo': producto.titulo,'precio': str(producto.precio)})

    return JsonResponse({'productos': data})


@login_required(login_url='/login')
def productos_carrito_add(request,producto_id,servicio_id,categoria_id):
    logging.warning("Productos carrito add requestttttt")
    perfil = request.user.perfil
    producto = Producto.objects.get(id=producto_id)
    perfil.productos.add(producto)
    perfil.save()
    return redirect('subservicios',servicio_id=servicio_id,categoria_id=categoria_id)




@login_required(login_url='/login')
def productos_carrito_count(request):
    logging.warning("Productos carrito count requestttttt")
    perfil = request.user.perfil
    productos = perfil.productos.all() 
    total = 0
    if len(productos) != 0:
        for producto in productos:
            total += producto.precio
        enviar_factura(request,total,productos,perfil)    
        perfil.productos.remove(*productos)
        perfil.save()
    else:
        messages.error(request, "No hay productos en el carrito.")
    return JsonResponse({'total': total})




def enviar_factura(request,total,productos,perfil):
        subject = 'Factura de Compra'
        from_email = settings.EMAIL_HOST_USER
        to_email = [request.user.email]

        html_message = render_to_string('factura_compra.html', {'usuario': request.user,'perfil': perfil,'productos': productos,'total': total})

        try:
            send_mail(subject, '', from_email, to_email, html_message=html_message)
            logging.warning(f"Factura enviada a {request.user.email}")
        except Exception as e:
            logging.warning(f"Error al enviar la factura: {e}")


@login_required(login_url='/login')
def home(request):
    publicaciones = Publicacion.objects.all()
    return render(request, 'components/home/home.html', {'publicaciones': publicaciones})







  
@login_required(login_url='/login')
def admin_socios_c(request):
    return render(request, 'admin/socios/socios.html')
@login_required(login_url='/login')
def admin_socios_formularios_c(request):
    return render(request, 'admin/socios/socios_formularios.html')
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





















# USUARIOS ADMIN

@login_required(login_url='/login')
def masteradmin(request):
    return render(request, 'admin/master/masteradmin.html')




@login_required(login_url='/login')
@user_passes_test(lambda u: u.is_superuser)
def admin_usuarios(request):
    usuarios = User.objects.all().order_by('-date_joined')  
    return render(request, 'admin/usuarios/usuarios.html', {'usuarios': usuarios})



@login_required(login_url='/login')
@user_passes_test(lambda u: u.is_superuser)
def admin_usuarios_info(request, user_id):
    usuario = get_object_or_404(User, id=user_id)
    return render(request, 'admin/usuarios/usuario_info.html', {'usuario': usuario})




@login_required(login_url='/login')
@user_passes_test(lambda u: u.is_superuser)
def admin_usuarios_incremento(request):
    usuarios = User.objects.all()
    return render(request, 'admin/usuarios/usuarios_incremento.html', {'usuarios': usuarios})





@login_required(login_url='/login')
@user_passes_test(lambda u: u.is_superuser)
def enviar_mensaje_usuario(request, user_id):
    usuario = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = MensajeForm(request.POST)
        if form.is_valid():
            mensaje = form.save(commit=False)
            mensaje.usuario = usuario
            mensaje.save()
            #messages.success(request, "Mensaje enviado correctamente.")
            return redirect('admin_usuarios_incremento')
    else:
        form = MensajeForm()
    return render(request, 'admin/usuarios/enviar_mensaje.html', {'form': form, 'usuario': usuario})    




@login_required(login_url='/login')
@user_passes_test(lambda u: u.is_superuser)
def dashboard(request):
    total_usuarios = User.objects.count()
    total_socios = Socio.objects.count()
    usuarios = User.objects.all()

    context = {
        'total_usuarios': total_usuarios,
        'total_socios': total_socios,
        'usuarios': usuarios,
    }
    return render(request, 'admin/dashboard/dashboard.html', context) 



@login_required(login_url='/login')
@user_passes_test(lambda u: u.is_superuser)
def listar_publicaciones(request):
    publicaciones = Publicacion.objects.all().order_by('-fecha_creacion')
    return render(request, 'admin/publicaciones/lista_publicaciones.html', {
        'publicaciones': publicaciones
    })


@login_required(login_url='/login')
@user_passes_test(lambda u: u.is_superuser)
def crear_publicacion(request):
    ImagenFormSet = modelformset_factory(ImagenPublicacion, form=ImagenPublicacionForm, extra=3, max_num=5)

    if request.method == 'POST':
        pub_form = PublicacionForm(request.POST)
        formset = ImagenFormSet(request.POST, request.FILES, queryset=ImagenPublicacion.objects.none())

        if pub_form.is_valid() and formset.is_valid():
            publicacion = pub_form.save(commit=False)
            publicacion.autor = request.user
            publicacion.save()

            for form in formset:
                if form.cleaned_data.get('imagen'):
                    imagen = form.save(commit=False)
                    imagen.publicacion = publicacion
                    imagen.save()

            return redirect('listar_publicaciones')
    else:
        pub_form = PublicacionForm()
        formset = ImagenFormSet(queryset=ImagenPublicacion.objects.none())

    return render(request, 'admin/publicaciones/crear_publicacion.html', {
        'form': pub_form,
        'formset': formset,
    }) 



@login_required(login_url='/login')
@user_passes_test(lambda u: u.is_superuser)
def ver_info_publicacion(request, publicacion_id):
    publicacion = get_object_or_404(Publicacion, id=publicacion_id)
    imagenesPublicacion = ImagenPublicacion.objects.filter(publicacion=publicacion)
    return render(request, 'admin/publicaciones/ver_info_publicacion.html', {
        'publicacion': publicacion,
        'imagenesPublicacion': imagenesPublicacion
    })    


@login_required(login_url='/login')
@user_passes_test(lambda u: u.is_superuser)
def admin_socios(request):
    socios = Socio.objects.prefetch_related('perfiles').order_by('-id')  
    context = {
        'socios': socios,
    }
    return render(request, 'admin/socios/socios.html', context)




@login_required(login_url='/login')
@user_passes_test(lambda u: u.is_superuser)
@require_POST
def toggle_estado_socio(request):
    socio_id = request.POST.get('id')
    activo = request.POST.get('activo') == 'true'  

    socio = get_object_or_404(Socio, id=socio_id)
    socio.activo = activo
    socio.save()

    return JsonResponse({'success': True, 'activo': socio.activo})

@login_required(login_url='/login')
@user_passes_test(lambda u: u.is_superuser)
def ver_info_socio(request, socio_id):
    socio = get_object_or_404(Socio, id=socio_id)
    return render(request, 'admin/socios/ver_info_socio.html', {'socio': socio})



@login_required(login_url='/login')
@user_passes_test(lambda u: u.is_superuser)
def admin_socios_formularios(request):
    solicitudes = SolicitudSeguroVida.objects.all().order_by('-fecha_creacion')
    return render(request, 'admin/socios/socios_formularios.html', {'solicitudes': solicitudes}) 


@login_required(login_url='/login')
@user_passes_test(lambda u: u.is_superuser)
def ver_info_solicitud(request, solicitud_id):
    solicitud = get_object_or_404(SolicitudSeguroVida, id=solicitud_id)
    return render(request, 'admin/socios/ver_info_solicitud.html', {'solicitud': solicitud})    




@login_required(login_url='/login')
@user_passes_test(lambda u: u.is_superuser)
def listar_categorias_admin(request):
    categorias = Categorias.objects.all().order_by('-fecha_creacion')
    context = {'categorias': categorias}
    return render(request, 'admin/categorias/listar_categorias_admin.html', context)






@login_required(login_url='/login')
@user_passes_test(lambda u: u.is_superuser)
def crear_categoria(request):

    if request.method == "POST":
        form = CategoriaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Categoría creada exitosamente.")
            return redirect('listar_categorias_admin')
        else:
            messages.error(request, "Error al crear la categoría.")
            return redirect('crear_categoria')

    else:
        pub_form = CategoriaForm()

    return render(request, 'admin/categorias/crear_categoria.html', {'form': pub_form})

@login_required(login_url='/login')
@user_passes_test(lambda u: u.is_superuser)
def editar_categoria(request, id):
    categoria = get_object_or_404(Categorias, id=id)
    if request.method == "POST":
        form = CategoriaForm(request.POST, request.FILES, instance=categoria)
        if form.is_valid():
            form.save()
            messages.success(request, "Categoría editada exitosamente.")
            return redirect('listar_categorias_admin')
        else:
            messages.error(request, "Error al editar la categoría.")
            return redirect('editar_categoria', id=id)
    else:
        form = CategoriaForm(instance=categoria)
    return render(request, 'admin/categorias/editar_categoria.html', {'form': form, 'categoria': categoria})


@login_required(login_url='/login')
@user_passes_test(lambda u: u.is_superuser)
def eliminar_categoria(request, id):
    categoria = get_object_or_404(Categorias, id=id)
    categoria.delete()
    messages.success(request, "Categoría eliminada exitosamente.")
    return redirect('listar_categorias_admin')


@login_required(login_url='/login')
@user_passes_test(lambda u: u.is_superuser)
def listar_servicios_admin(request):
    servicios = Servicios.objects.all().order_by('-fecha_creacion')
    context = {'servicios': servicios}
    return render(request, 'admin/servicios/listar_servicios_admin.html', context)


@login_required(login_url='/login')
@user_passes_test(lambda u: u.is_superuser)
def crear_servicio(request):

    if request.method == "POST":
        form = ServicioForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Servicio creado exitosamente.")
            return redirect('listar_servicios_admin')
        else:
            messages.error(request, "Error al crear el servicio.")
            return redirect('crear_servicio')

    else:
        pub_form = ServicioForm()

    return render(request, 'admin/servicios/crear_servicio.html', {'form': pub_form})




@login_required(login_url='/login')
@user_passes_test(lambda u: u.is_superuser)
def editar_servicio(request, id):
    servicio = get_object_or_404(Servicios, id=id)
    if request.method == "POST":
        form = ServicioForm(request.POST, request.FILES, instance=servicio)
        if form.is_valid():
            form.save()
            messages.success(request, "Servicio editado exitosamente.")
            return redirect('listar_servicios_admin')
        else:
            messages.error(request, "Error al editar el servicio.")
            return redirect('editar_servicio', id=id)
    else:
        form = ServicioForm(instance=servicio)
    return render(request, 'admin/servicios/editar_servicio.html', {'form': form, 'servicio': servicio})



@login_required(login_url='/login')
@user_passes_test(lambda u: u.is_superuser)
def eliminar_servicio(request, id):
    servicio = get_object_or_404(Servicios, id=id)
    servicio.delete()
    messages.success(request, "Servicio eliminado exitosamente.")
    return redirect('listar_servicios_admin')


@login_required(login_url='/login')
@user_passes_test(lambda u: u.is_superuser)
def listar_subservicios_admin(request):
    subservicios = Subservicios.objects.all().order_by('-fecha_creacion')
    context = {'subservicios': subservicios}
    return render(request, 'admin/subservicios/listar_subservicios.html', context)
    

@login_required(login_url='/login')
@user_passes_test(lambda u: u.is_superuser)
def crear_subservicio(request):

    if request.method == "POST":
        form = SubservicioForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Subservicio creado exitosamente.")
            return redirect('listar_subservicios_admin')
        else:
            messages.error(request, "Error al crear el subservicio.")
            return redirect('crear_subservicio')

    else:
        pub_form = SubservicioForm()

    return render(request, 'admin/subservicios/crear_subservicio.html', {'form': pub_form})


@login_required(login_url='/login')
@user_passes_test(lambda u: u.is_superuser)
def editar_subservicio(request, id):
    subservicio = get_object_or_404(Subservicios, id=id)
    if request.method == "POST":
        form = SubservicioForm(request.POST, request.FILES, instance=subservicio)
        if form.is_valid():
            form.save()
            messages.success(request, "Subservicio editado exitosamente.")
            return redirect('listar_subservicios_admin')
        else:
            messages.error(request, "Error al editar el subservicio.")
            return redirect('editar_subservicio', id=id)
    else:
        form = SubservicioForm(instance=subservicio)
    return render(request, 'admin/subservicios/editar_subservicio.html', {'form': form, 'subservicio': subservicio})


@login_required(login_url='/login')
@user_passes_test(lambda u: u.is_superuser)
def eliminar_subservicio(request, id):
    subservicio = get_object_or_404(Subservicios, id=id)
    subservicio.delete()
    messages.success(request, "Subservicio eliminado exitosamente.")
    return redirect('listar_subservicios_admin')

@login_required(login_url='/login')
@user_passes_test(lambda u: u.is_superuser)
def listar_productos(request):
    productos = Producto.objects.all().order_by('-fecha_creacion')
    context = {'productos': productos}
    return render(request, 'admin/producto/listar_productos.html', context)


@login_required(login_url='/login')
@user_passes_test(lambda u: u.is_superuser)
def crear_producto(request):
    if request.method == "POST":
        form = FormProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto creado exitosamente.")
            return redirect('listar_productos')
        else:
            messages.error(request, "Error al crear el producto.")
            return redirect('crear_producto')
    else:
        form = FormProductoForm()
    return render(request, 'admin/producto/crear_producto.html', {'form': form})



@login_required(login_url='/login')
@user_passes_test(lambda u: u.is_superuser)
def editar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    if request.method == "POST":
        form = FormProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto editado exitosamente.")
            return redirect('listar_productos')
        else:
            messages.error(request, "Error al editar el producto.")
            return redirect('editar_producto', id=id)
    else:
        form = FormProductoForm(instance=producto)
    return render(request, 'admin/producto/editar_producto.html', {'form': form, 'producto': producto})



@login_required(login_url='/login')
@user_passes_test(lambda u: u.is_superuser)
def eliminar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    producto.delete()
    messages.success(request, "Producto eliminado exitosamente.")
    return redirect('listar_productos')






pusher_client = pusher.Pusher(app_id=settings.PUSHER_APP_ID,key=settings.PUSHER_KEY,secret=settings.PUSHER_SECRET,cluster=settings.PUSHER_CLUSTER,ssl=True)


@login_required(login_url='/login')
@csrf_exempt
def pusher_auth(request):
    print("Llegó a pusher_auth!")

    if not request.user.is_authenticated:
        return HttpResponseForbidden()

    channel_name = request.POST.get('channel_name')
    socket_id = request.POST.get('socket_id')
    expected_channel = f"private-user-{request.user.id}"


    if channel_name != expected_channel:
        return HttpResponseForbidden("Canal no autorizado")

    auth = pusher_client.authenticate(channel=channel_name,socket_id=socket_id)
    return JsonResponse(auth)



@login_required(login_url='/login')
@user_passes_test(lambda u: u.is_superuser)
def trigger_event(request, user_id):
    channel_name = f"private-user-{user_id}"
    pusher_client.trigger(channel_name, 'my-event', {'message': f'Hola, usuario {user_id}! Tienes una nueva notificación.'})
    return JsonResponse({'status': 'Evento enviado correctamente'})


@login_required(login_url='/login')
def obtener_mensajes_usuario(request, user_id):
    mensajes = Mensaje.objects.filter(usuario=user_id).values('titulo', 'asunto', 'contenido', 'estado')
    return JsonResponse(list(mensajes), safe=False)


@login_required(login_url='/login')
def marcar_mensajes_leidos(request, user_id):
    Mensaje.objects.filter(usuario=user_id, estado=True).update(estado=False)
    return JsonResponse({'status': 'ok'})





















