# proyectoUno/urls.py
from django.urls import path
from . import views  # Asegúrate de que las vistas estén importadas correctamente

urlpatterns = [
    #path('', views.index, name='index'),  # Ruta de la vista 'index'
    #path('categorias', views.categoria, name='categorias'),
    #path('servicios', views.servicio, name='servicios'),
    #path('subservicios', views.subservicio, name='subservicios'),
    #path('formularios', views.formulario, name='formularios'),

    path('', views.index, name='index'),
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('master', views.master, name='master'),
    path('categorias', views.categorias, name='categorias'),
    path('servicios', views.servicios, name='servicios'),
    path('subservicios', views.subservicios, name='subservicios'),
    path('masteradmin', views.masteradmin, name='masteradmin'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('admin_usuarios', views.admin_usuarios, name='admin_usuarios'),
    path('admin_usuarios_incremento', views.admin_usuarios_incremento, name='admin_usuarios_incremento'),
    path('admin_socios', views.admin_socios, name='admin_socios'),
    path('admin_socios_formularios', views.admin_socios_formularios, name='admin_socios_formularios'),
    path('seguro_vida', views.seguro_vida, name='seguro_vida'),
    path('seguro_vida_archivos_subidos', views.seguro_vida_archivos_subidos, name='seguro_vida_archivos_subidos'),
    path('seguro_vida_archivos_recibidos', views.seguro_vida_archivos_recibidos, name='seguro_vida_archivos_recibidos'),
    path('seguro_vida_estado', views.seguro_vida_estado, name='seguro_vida_estado'),    
    path('formularios', views.formularios, name='formularios'),
    path('formularios_form_a', views.formularios_form_a, name='formularios_form_a'),
    path('formularios_form_b', views.formularios_form_b, name='formularios_form_b'),
    path('solicitud_seguro_form', views.solicitud_seguro_form, name='solicitud_seguro_form'),
]

