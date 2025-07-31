from django.contrib import admin
from .models import * 
admin.site.register(Mas_informacion)
admin.site.register(Subservicios)
admin.site.register(Beneficio)
admin.site.register(Servicios)
admin.site.register(PerfilUsuario)
admin.site.register(Seleccion)
admin.site.register(Formularios)
admin.site.register(Categorias)
admin.site.register(Entidades)
admin.site.register(Convenios)
admin.site.register(Factura)
admin.site.register(BeneficiarioSeguro)
admin.site.register(InformacionSeguroSocio)
admin.site.register(Socio)

# --- Fin de los modelos afiliados---

# --- NUEVO MODELO: Solicitud de Seguro de Vida ---
admin.site.register(SolicitudSeguroVida)
admin.site.register(DeclaracionSalud)
admin.site.register(DetalleDeclaracionSalud)
admin.site.register(Beneficiario)
admin.site.register(DeporteActividad)
admin.site.register(Producto)
admin.site.register(FormularioProductoVida)


# --- Fin de los modelos de Solicitud de Seguro de Vida ---
admin.site.register(Mensaje)
admin.site.register(Publicacion)
admin.site.register(ImagenPublicacion)
admin.site.register(Firma)
