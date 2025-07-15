# proyectoUno/views.py
from django.shortcuts import render
import logging

#def index(request):
#    return render(request, 'index.html')

#def categoria(request):
#    return render(request, 'categorias.html')

#def servicio(request):
#    return render(request, 'servicio.html')

#def subservicio(request):
#    return render(request, 'subservicio.html')

#def formulario(request):
#    return render(request, 'formulario.html')


# Create your views here.
def index(request):
    return render(request, 'index.html')


def login(request):
    logging.warning("Login requestttttt")
    return render(request, 'auth/login/login.html')



def register(request):
    return render(request, 'auth/register/register.html')
def master(request):
    return render(request, 'master/side_bar/master.html')    
def categorias(request):
    return render(request, 'components/categories/categorias.html')
def servicios(request):
    logging.warning("Servicios requestttttt")
    return render(request, 'components/services/servicios.html')
def subservicios(request):
    logging.warning("Subservicios requestttttt")
    return render(request, 'components/subservicios/subservicios.html')
def masteradmin(request):
    return render(request, 'admin/master/masteradmin.html')
def dashboard(request):
    return render(request, 'admin/dashboard/dashboard.html')
def admin_usuarios(request):
    return render(request, 'admin/usuarios/usuarios.html')
def admin_usuarios_incremento(request):
    return render(request, 'admin/usuarios/usuarios_incremento.html')    
def admin_socios(request):
    return render(request, 'admin/socios/socios.html')
def admin_socios_formularios(request):
    return render(request, 'admin/socios/socios_formularios.html')
def seguro_vida(request):
    logging.warning("Seguro Vida requestttttt")
    return render(request, 'components/subservicios/seguroVida/seguro_vida.html')
def seguro_vida_archivos_subidos(request):
    return render(request, 'components/subservicios/seguroVida/seguro_vida_archivos_subidos.html')
def seguro_vida_archivos_recibidos(request):
    return render(request, 'components/subservicios/seguroVida/seguro_vida_archivos_recibidos.html')
def seguro_vida_estado(request):
    return render(request, 'components/subservicios/seguroVida/seguro_vida_estado.html')
def formularios(request):
    return render(request, 'components/forms/formularios_main.html')
def formularios_form_a(request):
    return render(request, 'components/forms/formularios_form_a.html')
def formularios_form_b(request):
    return render(request, 'components/forms/formularios_form_b.html')     
def solicitud_seguro_form(request):
    return render(request, 'components/forms/solicitud_seguro_form.html')   

