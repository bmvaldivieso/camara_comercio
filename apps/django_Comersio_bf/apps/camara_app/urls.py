# proyectoUno/urls.py
from django.urls import path
from . import views  # Asegúrate de que las vistas estén importadas correctamente

urlpatterns = [

    path('', views.index, name='index'),
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('logout', views.logout_view, name='logout'),
    path('categorias', views.categorias, name='categorias'),
    path('servicios/<int:categoria_id>', views.servicios, name='servicios'),
    path('subservicios/<int:servicio_id>/<int:categoria_id>', views.subservicios, name='subservicios'),
    path('masteradmin', views.masteradmin, name='masteradmin'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('admin_usuarios', views.admin_usuarios, name='admin_usuarios'),
    path('admin_usuarios_incremento', views.admin_usuarios_incremento, name='admin_usuarios_incremento'),
    path('admin_socios', views.admin_socios_c, name='admin_socios'),
    path('admin_socios_formularios', views.admin_socios_formularios_c, name='admin_socios_formularios'),


    path('seguro_vida/<int:servicio_id>/<int:producto_id>/<int:categoria_id>', views.seguro_vida, name='seguro_vida'),
    path('firma/<int:servicio_id>/<int:producto_id>/<int:categoria_id>', views.firma, name='firma'),
    path('carrito/', views.productos_carrito, name='productos_carrito'),
    path('carrito_add/<int:producto_id>/<int:servicio_id>/<int:categoria_id>', views.productos_carrito_add, name='productos_carrito_add'),
    path('carrito_count', views.productos_carrito_count, name='productos_carrito_count'),



    path('seguro_vida_archivos_subidos', views.seguro_vida_archivos_subidos, name='seguro_vida_archivos_subidos'),
    path('seguro_vida_archivos_recibidos', views.seguro_vida_archivos_recibidos, name='seguro_vida_archivos_recibidos'),
    path('seguro_vida_estado', views.seguro_vida_estado, name='seguro_vida_estado'),    
    path('formularios', views.formularios, name='formularios'),
    path('formularios_form_a', views.formularios_form_a, name='formularios_form_a'),
    path('formularios_form_b', views.formularios_form_b, name='formularios_form_b'),
    path('solicitud_seguro_form', views.solicitud_seguro_form, name='solicitud_seguro_form'),
    path('ser_socio', views.ser_socio, name='ser_socio'),
    path('present_Socio', views.present_Socio, name='present_Socio'),





    #nuevas
    path('admin_usuarios_info/<int:user_id>', views.admin_usuarios_info, name='admin_usuarios_info'),
    path('admin_usuarios_mensaje/<int:user_id>/', views.enviar_mensaje_usuario, name='enviar_mensaje_usuario'),
    path('publicaciones/', views.listar_publicaciones, name='listar_publicaciones'),
    path('publicaciones/crear/', views.crear_publicacion, name='crear_publicacion'),
    path('publicaciones/ver_info/<int:publicacion_id>/', views.ver_info_publicacion, name='ver_info_publicacion'),
    path('admin_socios', views.admin_socios, name='admin_socios'),
    path('publicaciones/socios/toggle-estado/', views.toggle_estado_socio, name='toggle_estado_socio'),
    path('publicaciones/socios/ver_info/<int:socio_id>/', views.ver_info_socio, name='ver_info_socio'),
    path('admin_socios_formularios/ver_info/<int:solicitud_id>/', views.ver_info_solicitud, name='ver_info_solicitud'),
    path('listar_categorias_admin', views.listar_categorias_admin, name='listar_categorias_admin'),
    path('crear_categoria', views.crear_categoria, name='crear_categoria'),
    path('editar_categoria/<int:id>/', views.editar_categoria, name='editar_categoria'),
    path('eliminar_categoria/<int:id>/', views.eliminar_categoria, name='eliminar_categoria'),
    path('listar_servicios_admin', views.listar_servicios_admin, name='listar_servicios_admin'),
    path('crear_servicio', views.crear_servicio, name='crear_servicio'),
    path('editar_servicio/<int:id>/', views.editar_servicio, name='editar_servicio'),
    path('eliminar_servicio/<int:id>/', views.eliminar_servicio, name='eliminar_servicio'),
    path('listar_subservicios_admin', views.listar_subservicios_admin, name='listar_subservicios_admin'),
]
