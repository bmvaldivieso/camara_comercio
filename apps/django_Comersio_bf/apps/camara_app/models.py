from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Mas_informacion(models.Model):
    """
    Modelo para almacenar contenido de información adicional.
    Corresponde a la tabla 'Mas_informacion' en el esquema de la base de datos.
    """
    Contenido = models.TextField() 

    class Meta:
        verbose_name = "Más Información"
        verbose_name_plural = "Más Información"

    def __str__(self):
        return f"Más info #{self.id}"

class Subservicios(models.Model):
    """
    Modelo para almacenar los sub-servicios ofrecidos.
    Corresponde a la tabla 'Subservicios' en el esquema de la base de datos.
    """
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    img = models.ImageField(upload_to='subservicios/', null=True, blank=True)

    class Meta:
        verbose_name = "Subservicio"
        verbose_name_plural = "Subservicios"

    def __str__(self):
        return self.nombre

class Beneficio(models.Model):
    """
    Modelo para almacenar los beneficios ofrecidos con los servicios.
    Corresponde a la tabla 'Beneficio' en el esquema de la base de datos.
    """
    beneficio = models.CharField(max_length=100) 
    nombres = models.CharField(max_length=100)
    cantidad = models.IntegerField()
    porcentaje_descuento = models.FloatField()

    class Meta:
        verbose_name = "Beneficio"
        verbose_name_plural = "Beneficios"

    def __str__(self):
        return self.nombre

class Servicios(models.Model):
    """
    Modelo para almacenar los servicios principales.
    Corresponde a la tabla 'Servicios' en el esquema de la base de datos.
    """
    nombre = models.CharField(max_length=100)
    contacto = models.CharField(max_length=100)
    descripcion = models.TextField()
    requisitos = models.TextField()
    img = models.ImageField(upload_to='servicios/', null=True, blank=True)
    ubicacion = models.CharField(max_length=255)
    precio = models.DecimalField(max_digits=10, decimal_places=2) 

    id_mas_informacion = models.ForeignKey(Mas_informacion, on_delete=models.SET_NULL, null=True, blank=True, related_name='servicios')
    id_subservicios = models.ForeignKey(Subservicios, on_delete=models.SET_NULL, null=True, blank=True, related_name='servicios')
    id_beneficio = models.ForeignKey(Beneficio, on_delete=models.SET_NULL, null=True, blank=True, related_name='servicios_asociados')

    class Meta:
        verbose_name = "Servicio"
        verbose_name_plural = "Servicios"

    def __str__(self):
        return self.nombre



class PerfilUsuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    cedula = models.CharField(max_length=20)
    socio = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"



class Seleccion(models.Model):
    """
    Modelo para registrar selecciones, vinculando servicios a usuarios por fecha.
    Corresponde a la tabla 'Seleccion' en el esquema de la base de datos.
    """
    id_servicios = models.ForeignKey(Servicios, on_delete=models.CASCADE, related_name='selecciones')
    id_usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='selecciones', null=True, blank=True)
    fecha = models.DateField()

    class Meta:
        verbose_name = "Selección"
        verbose_name_plural = "Selecciones"

    def __str__(self):
        return f"Selección {self.id} - {self.id_servicios.nombre} por {self.id_usuario.first_name}"

class Formularios(models.Model):
    """
    Modelo para rastrear los formularios de usuario.
    Corresponde a la tabla 'Formularios' en el esquema de la base de datos.
    """
    f_seguro_vida = models.BooleanField(default=False)
    f_inscripcion = models.BooleanField(default=False)
    id_usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='formulario', null=True, blank=True)

    class Meta:
        verbose_name = "Formulario"
        verbose_name_plural = "Formularios"

    def __str__(self):
        return f"Formulario de {self.id_usuario.first_name}"

class Categorias(models.Model):
    """
    Modelo para categorizar servicios.
    Corresponde a la tabla 'Categorias' en el esquema de la base de datos.
    """
    tipo = models.CharField(max_length=100)
    nombre = models.CharField(max_length=100)
    fecha_creacion = models.DateField()
    img = models.ImageField(upload_to='categorias/', null=True, blank=True)
    monto_total = models.DecimalField(max_digits=10, decimal_places=2)
    id_servicio = models.ForeignKey(Servicios, on_delete=models.CASCADE, related_name='categorias')

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"

    def __str__(self):
        return self.nombre

class Entidades(models.Model):
    """
    Modelo para almacenar información sobre entidades (ej. empresas, socios).
    Corresponde a la tabla 'Entidades' en el esquema de la base de datos.
    """
    nombre = models.CharField(max_length=100)
    correo = models.EmailField()
    num_telefono = models.CharField(max_length=20, null=True, blank=True)
    direccion = models.CharField(max_length=255, null=True, blank=True)
    img = models.ImageField(upload_to='entidades/', null=True, blank=True)

    class Meta:
        verbose_name = "Entidad"
        verbose_name_plural = "Entidades"

    def __str__(self):
        return self.nombre

class Convenios(models.Model):
    """
    Modelo para almacenar detalles de acuerdos o convenios.
    Corresponde a la tabla 'Convenios' en el esquema de la base de datos.
    """
    nombre = models.CharField(max_length=100)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(null=True, blank=True)
    condiciones = models.TextField(null=True, blank=True)
    activo = models.BooleanField(default=True)
    descuento = models.FloatField(default=0.0)
    precio_convenido = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    id_servicio = models.ForeignKey(Servicios, on_delete=models.CASCADE, related_name='convenios')
    id_entidad = models.ForeignKey(Entidades, on_delete=models.CASCADE, related_name='convenios')

    class Meta:
        verbose_name = "Convenio"
        verbose_name_plural = "Convenios"

    def __str__(self):
        return f"Convenio {self.nombre} con {self.id_entidad.nombre}"

class Factura(models.Model):
    """
    Modelo para almacenar detalles de facturas.
    Corresponde a la tabla 'Factura' en el esquema de la base de datos.
    """
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    cedula = models.CharField(max_length=20)
    correo = models.EmailField()
    nombre_servicio_a = models.CharField(max_length=255) 
    fecha = models.DateField()
    importes = models.DecimalField(max_digits=10, decimal_places=2) 
    descuento_socio = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "Factura"
        verbose_name_plural = "Facturas"

    def __str__(self):
        return f"Factura #{self.id} - {self.first_name} {self.last_name}"