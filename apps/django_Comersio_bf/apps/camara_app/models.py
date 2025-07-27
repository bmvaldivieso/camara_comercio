from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from datetime import date

# Create your models here.

# --- NUEVO MODELO: Solicitud de Seguro de Vida ---
class SolicitudSeguroVida(models.Model):

    TIPO_IDENTIFICACION_CHOICES = [('cedula', 'Cédula'), ('pasaporte', 'Pasaporte'), ('ruc', 'RUC'),]
    ESTADO_CIVIL_CHOICES = [('soltero', 'Soltero/a'), ('casado', 'Casado/a'), ('divorciado', 'Divorciado/a'), ('viudo', 'Viudo/a'),]
    ENVIO_CORRESPONDENCIA_CHOICES = [('domicilio', 'Domicilio'), ('trabajo', 'Trabajo'),]
    ES_USTED_CHOICES = [('titular', 'Titular'), ('beneficiario', 'Beneficiario'),]

    # Datos de identificación
    tipo_identificacion = models.CharField(max_length=10, choices=TIPO_IDENTIFICACION_CHOICES, default='cedula', verbose_name="Tipo de identificación")
    numero_identificacion = models.CharField(max_length=20, unique=True, verbose_name="Número de identificación")
    nombres = models.CharField(max_length=100, verbose_name="Nombres")
    apellidos = models.CharField(max_length=100, verbose_name="Apellidos")
    fecha_nacimiento = models.DateField(verbose_name="Fecha de nacimiento")
    estado_civil = models.CharField(max_length=20, choices=ESTADO_CIVIL_CHOICES, blank=True, null=True, verbose_name="Estado Civil")

    # Datos del domicilio
    direccion_domicilio = models.CharField(max_length=255, verbose_name="Dirección Domicilio")
    correo_domicilio = models.CharField(max_length=100, verbose_name="Correo Electrónico Domicilio")
    telefono_domicilio = models.CharField(max_length=20, blank=True, null=True, verbose_name="Teléfono Domicilio")
    celular_domicilio = models.CharField(max_length=20, verbose_name="Celular Domicilio")

    # Datos del trabajo
    nombre_empresa = models.CharField(max_length=255, blank=True, null=True, verbose_name="Nombre de la empresa")
    direccion_trabajo = models.CharField(max_length=255, blank=True, null=True, verbose_name="Dirección Trabajo")
    correo_trabajo = models.CharField(max_length=100, blank=True, null=True, verbose_name="Correo Electrónico Trabajo")
    telefono_trabajo = models.CharField(max_length=20, blank=True, null=True, verbose_name="Teléfono Trabajo")
    ocupacion = models.CharField(max_length=100, blank=True, null=True, verbose_name="Ocupación")
    envio_correspondencia = models.CharField(max_length=10, choices=ENVIO_CORRESPONDENCIA_CHOICES, blank=True, null=True, verbose_name="Envío de correspondencia")

    # Otros seguros
    otros_seguros_vida = models.BooleanField(default=False, verbose_name="¿Tiene o está tramitando otros seguros de vida?")
    especifique_companias_otros_seguros = models.CharField(max_length=255, blank=True, null=True, verbose_name="Especifique compañías de otros seguros")

    es_usted = models.CharField(max_length=20, choices=ES_USTED_CHOICES, blank=True, null=True, verbose_name="Es usted")

    # --- Sección V: Declaraciones Finales ---
    lugar_firma = models.CharField(max_length=100, verbose_name="Lugar de Firma")
    fecha_firma = models.DateField(auto_now_add=True, verbose_name="Fecha de Firma")
    firma_electronica_generada = models.BooleanField(default=False, verbose_name="¿Firma electrónica generada?")
    # Puedes añadir un campo para almacenar la firma si es una imagen o un hash
    # firma_electronica_archivo = models.ImageField(upload_to='firmas/', blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Solicitud de {self.nombres} {self.apellidos} - {self.numero_identificacion}"

    class Meta:
        verbose_name = "Solicitud de Seguro de Vida"
        verbose_name_plural = "Solicitudes de Seguro de Vida"
    
    
    def obtener_fecha_actual(self):
        meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
        hoy = timezone.now()
        return f"{hoy.day} de {meses[hoy.month - 1]} de {hoy.year}"



class DeclaracionSalud(models.Model):
    """
    Modelo para la Sección II: Declaración del Estado de Salud.
    Relacionado uno a uno con SolicitudSeguroVida.
    """
    solicitud = models.OneToOneField(SolicitudSeguroVida, on_delete=models.CASCADE, related_name='declaracion_salud', verbose_name="Solicitud de Seguro")

    # Datos físicos
    peso_kg = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, verbose_name="Peso (kg)")
    estatura_cm = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, verbose_name="Estatura (cm)")
    tension_arterial_sistolica = models.CharField(max_length=10, blank=True, null=True, verbose_name="Tensión Arterial Sistólica")
    tension_arterial_diastolica = models.CharField(max_length=10, blank=True, null=True, verbose_name="Tensión Arterial Diastólica")

    # Cambios de peso
    peso_ha_cambiado = models.BooleanField(default=False, verbose_name="¿Su peso ha aumentado o disminuido durante el último año?")
    cuanto_peso_cambio = models.CharField(max_length=50, blank=True, null=True, verbose_name="¿Cuánto peso cambió?")
    peso_cambio_intencional = models.BooleanField(default=False, verbose_name="¿Cambio de peso intencional?")
    causa_peso_cambio = models.CharField(max_length=255, blank=True, null=True, verbose_name="Causa del cambio de peso")

    # Preguntas de salud (1-10)
    pregunta1_salud = models.BooleanField(default=False, verbose_name="1. ¿Afecciones del corazón o aparato circulatorio...?")
    pregunta2_salud = models.BooleanField(default=False, verbose_name="2. ¿Afecciones de los órganos respiratorios...?")
    pregunta3_salud = models.BooleanField(default=False, verbose_name="3. ¿Enfermedad circulatoria o accidente vascular cerebral?")
    pregunta4_salud = models.BooleanField(default=False, verbose_name="4. ¿Enfermedades del sistema endocrino...?")
    pregunta5_salud = models.BooleanField(default=False, verbose_name="5. ¿Cirrosis hepática, hepatitis C o insuficiencia hepática?")
    pregunta6_salud = models.BooleanField(default=False, verbose_name="6. ¿Edema o supuración o aumento de volumen de los ganglios linfáticos?")
    pregunta7_salud = models.BooleanField(default=False, verbose_name="7. Afecciones del cerebro o del sistema nervioso...?")
    pregunta8_salud = models.BooleanField(default=False, verbose_name="8. Afecciones del aparato digestivo...?")
    pregunta9_salud = models.BooleanField(default=False, verbose_name="9. ¿Enfermedades de la piel?")
    pregunta10_salud = models.BooleanField(default=False, verbose_name="10. ¿Enfermedades infecciosas...?")
    # 11 a 28
    pregunta11_salud = models.BooleanField(default=False,verbose_name="11. ¿Afecciones urinarias o genitales? (riñones, próstata, etc.)")
    pregunta12_salud = models.BooleanField(default=False,verbose_name="12. ¿Enfermedades de la sangre, gota, hernia, etc.?")
    pregunta13_salud = models.BooleanField(default=False,verbose_name="13. ¿Enfermedades venéreas o de transmisión sexual?")
    pregunta14_salud = models.BooleanField(default=False,verbose_name="14. ¿Accidente grave o intoxicación?")
    pregunta15_salud = models.BooleanField(default=False,verbose_name="15. ¿Enfermedades de los oídos?")
    pregunta16_salud = models.BooleanField(default=False,verbose_name="16. ¿Enfermedades de los ojos?")
    pregunta17_salud = models.BooleanField(default=False,verbose_name="17. ¿Tratamiento por psiquiatra o psicólogo?")
    pregunta18_salud = models.BooleanField(default=False,verbose_name="18. ¿HIV o SIDA?")
    pregunta19_salud = models.BooleanField(default=False,verbose_name="19. ¿Le han prescrito medicamentos en los últimos 12 meses?")
    pregunta20_salud = models.BooleanField(default=False,verbose_name="20. ¿Le han indicado reposo o desintoxicación?")
    pregunta21_salud = models.BooleanField(default=False,verbose_name="21. ¿Ha recibido transfusiones?")
    pregunta22_salud = models.BooleanField(default=False,verbose_name="22. ¿Le han recomendado no donar sangre?")
    pregunta23_salud = models.BooleanField(default=False,verbose_name="23. ¿Tiene capacidad de trabajo reducida?")
    pregunta24_salud = models.BooleanField(default=False,verbose_name="24. ¿Ha dejado de trabajar por más de 3 semanas en los últimos 5 años?")
    pregunta25_salud = models.BooleanField(default=False,verbose_name="25. ¿Antecedentes hereditarios (diabetes, corazón, etc.)?")
    pregunta26_salud = models.BooleanField(default=False,verbose_name="26. ¿Intervención quirúrgica?")
    pregunta27_salud = models.BooleanField(default=False,verbose_name="27. ¿Hospitalización pendiente?")
    pregunta28_salud = models.BooleanField(default=False,verbose_name="28. ¿Cualquier otra enfermedad no declarada?")

    # Fuma
    fuma = models.BooleanField(default=False, blank=True)
    cantidad_fumada = models.CharField(max_length=255, null=True, blank=True)

    # Detalles adicionales de salud
    detalle_preguntas_salud = models.TextField(null=True, blank=True)
    nombre_medico = models.CharField(max_length=255, null=True, blank=True)
    medico_ultima_vez = models.CharField(max_length=255, null=True, blank=True)
    motivo_ultima_vez = models.CharField(max_length=255, null=True, blank=True)

    # Hábitos
    consume_alcohol = models.BooleanField(default=False, verbose_name="¿Consume usted bebidas alcohólicas?")
    cuales_alcohol = models.CharField(max_length=100, blank=True, null=True, verbose_name="¿Cuáles bebidas alcohólicas?")
    cuanto_diariamente_alcohol = models.CharField(max_length=100, blank=True, null=True, verbose_name="¿Cuánto alcohol diariamente?")
    uso_estupefacientes = models.BooleanField(default=False, verbose_name="¿Hace o ha hecho uso de estupefacientes?")
    cuales_estupefacientes = models.CharField(max_length=100, blank=True, null=True, verbose_name="¿Cuáles estupefacientes?")
    hasta_cuando_estupefacientes = models.CharField(max_length=100, blank=True, null=True, verbose_name="¿Hasta cuándo estupefacientes?")

    # Para mujeres
    toma_anticonceptivos = models.BooleanField(default=False, verbose_name="¿Toma Usted anticonceptivos?")
    esta_embarazada = models.BooleanField(default=False, verbose_name="¿Está usted embarazada?")
    cuantos_meses_embarazo = models.PositiveSmallIntegerField(blank=True, null=True, validators=[MinValueValidator(1), MaxValueValidator(12)], verbose_name="¿Cuántos meses de embarazo?")
    enfermedad_ginecologica = models.BooleanField(default=False, verbose_name="¿Ha sufrido alguna enfermedad ginecológica?")

    # Información médica adicional
    medico_cabecera = models.CharField(max_length=255, blank=True, null=True, verbose_name="¿Quién es su médico de cabecera?")
    medico_ultima_vez = models.CharField(max_length=255, blank=True, null=True, verbose_name="¿Quién es el médico que le ha tratado por última vez?")
    cuando_ultima_vez = models.DateField(blank=True, null=True, verbose_name="¿Cuándo fue la última vez que le trató un médico?")
    motivo_ultima_vez = models.CharField(max_length=255, blank=True, null=True, verbose_name="Motivo de la última consulta médica")
    otra_declaracion_salud = models.TextField(blank=True, null=True, verbose_name="¿Tiene Usted alguna otra cosa que declarar sobre su salud? Indique:")

    def __str__(self):
        return f"Declaración de Salud para Solicitud #{self.solicitud.id}"

    class Meta:
        verbose_name = "Declaración de Salud"
        verbose_name_plural = "Declaraciones de Salud"





class DetalleDeclaracionSalud(models.Model):
    """
    Modelo para los detalles de las preguntas afirmativas de la Sección II (tabla dinámica).
    Relacionado uno a muchos con DeclaracionSalud.
    """
    declaracion_salud = models.ForeignKey(DeclaracionSalud, on_delete=models.CASCADE, related_name='detalles_preguntas_salud', verbose_name="Declaración de Salud")
    numero_pregunta = models.PositiveSmallIntegerField(verbose_name="Nro de pregunta")
    detalle = models.TextField(verbose_name="Detalle de la afección")
    cuando = models.CharField(max_length=100, blank=True, null=True, verbose_name="¿Cuándo ocurrió?")
    duracion = models.CharField(max_length=100, blank=True, null=True, verbose_name="¿Duración?")
    secuelas = models.CharField(max_length=255, blank=True, null=True, verbose_name="¿Secuelas?")
    medico_tratante = models.CharField(max_length=255, blank=True, null=True, verbose_name="Nombre y dirección del médico tratante")

    def __str__(self):
        return f"Detalle Pregunta {self.numero_pregunta} - Solicitud #{self.declaracion_salud.solicitud.id}"

    class Meta:
        verbose_name = "Detalle de Declaración de Salud"
        verbose_name_plural = "Detalles de Declaración de Salud"


class DeporteActividad(models.Model):
    """
    Modelo para la Sección III: Deportes y Actividades Recreacionales.
    Relacionado uno a muchos con SolicitudSeguroVida.
    """
    solicitud = models.ForeignKey(SolicitudSeguroVida, on_delete=models.CASCADE, related_name='deportes_actividades', verbose_name="Solicitud de Seguro")
    nombre_actividad = models.CharField(max_length=255, verbose_name="¿Qué deportes y/o actividades recreacionales practica?")
    con_competicion = models.BooleanField(default=False, verbose_name="¿Con competición?")
    es_piloto = models.BooleanField(default=False, verbose_name="¿Es piloto o está en proceso de serlo?")
    paracaidismo = models.BooleanField(default=False, verbose_name="¿Paracaidismo?")

    class Meta:
        verbose_name = "Deporte o Actividad Recreacional"
        verbose_name_plural = "Deportes y Actividades Recreacionales"


class Beneficiario(models.Model):
    """
    Modelo para la Sección IV: Designación de Beneficiarios.
    Relacionado uno a muchos con SolicitudSeguroVida.
    """
    solicitud = models.ForeignKey(SolicitudSeguroVida, on_delete=models.CASCADE, related_name='beneficiarios', verbose_name="Solicitud de Seguro")
    nombres_completos = models.CharField(max_length=255, verbose_name="Nombres completos")
    direccion = models.CharField(max_length=255, verbose_name="Dirección")
    fecha_nacimiento = models.DateField(verbose_name="Fecha de nacimiento")
    parentesco = models.CharField(max_length=100, verbose_name="Parentesco")
    cedula_identidad = models.CharField(max_length=20, verbose_name="C.I.")
    porcentaje = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(100)], verbose_name="Porcentaje (%)")

    def __str__(self):
        return f"Beneficiario: {self.nombres_completos} de Solicitud #{self.solicitud.id}"

    class Meta:
        verbose_name = "Beneficiario"
        verbose_name_plural = "Beneficiarios"



# --- Fin de los modelos afiliados---




class BeneficiarioSeguro(models.Model):
    nombre_completo = models.CharField(max_length=255)
    porcentaje = models.DecimalField(max_digits=5, decimal_places=2, help_text="Porcentaje del seguro (ej. 50.00)")

    class Meta:
        verbose_name = "Beneficiario de Seguro"
        verbose_name_plural = "Beneficiarios de Seguro"

    def __str__(self):
        return f"{self.nombre_completo} ({self.porcentaje}%)"



class InformacionSeguroSocio(models.Model):
    nombre_titular = models.CharField(max_length=255)
    telefono_titular = models.CharField(max_length=20, blank=True, null=True)
    fecha_nacimiento_titular = models.DateField(blank=True, null=True)
    cedula_titular = models.CharField(max_length=10)
    firma_titular = models.CharField(max_length=255, blank=True, null=True, help_text="Nombre completo para firma de aceptación")
    id_beneficiario = models.ForeignKey(BeneficiarioSeguro, on_delete=models.SET_NULL, null=True, blank=True, related_name='informacion_seguro')
    class Meta:
        verbose_name = "Información de Seguro del Socio"
        verbose_name_plural = "Información de Seguros de Socios"

    def __str__(self):
        return f"Seguro de {self.nombre_titular}"


# --- NUEVO MODELO: Socio ---
class Socio(models.Model):
    TIPO_NEGOCIO_CHOICES = [('Comercio', 'Comercio'), ('Servicios', 'Servicios'), ('Importación/Exportación', 'Importación/Exportación'), ('Industria', 'Industria'), ('Otros', 'Otros'),]

    razon_social = models.CharField(max_length=255, blank=True, null=True, help_text="Razón Social (para personas jurídicas)")
    nombre_comercial = models.CharField(max_length=255, help_text="Nombre Comercial (empresa) o Nombres y Apellidos (persona natural)")
    ruc_cedula = models.CharField(max_length=13, unique=True, help_text="RUC (13 dígitos) o Cédula (10 dígitos)")
    email_principal = models.EmailField(unique=True, help_text="Correo electrónico principal del socio/empresa")
    redes_sociales = models.CharField(max_length=255, blank=True, null=True, help_text="Redes sociales que utiliza (separadas por comas)")

    #slide 2
    cedula_representante = models.CharField(max_length=10, blank=True, null=True, help_text="Cédula o Pasaporte del Representante Legal")
    apellidos_nombres_representante = models.CharField(max_length=255, blank=True, null=True, help_text="Apellidos y Nombres del Representante Legal")
    direccion_principal = models.CharField(max_length=255, help_text="Dirección principal del negocio")
    calle = models.CharField(max_length=100, blank=True, null=True)
    numero = models.CharField(max_length=20, blank=True, null=True)
    interseccion = models.CharField(max_length=100, blank=True, null=True, help_text="Calle de intersección")
    referencia = models.CharField(max_length=255, blank=True, null=True, help_text="Referencia de la dirección")
    parroquia = models.CharField(max_length=100, blank=True, null=True)
    ciudad = models.CharField(max_length=100, default="Loja")
    pais = models.CharField(max_length=100, default="Ecuador")
    pagina_web = models.URLField(max_length=200, blank=True, null=True)
    email_empresa = models.EmailField(blank=True, null=True, help_text="Correo electrónico de la empresa (si es diferente al principal)")
    telefono1 = models.CharField(max_length=20, blank=True, null=True)
    telefono2 = models.CharField(max_length=20, blank=True, null=True)
    celular = models.CharField(max_length=20, blank=True, null=True)

    #slide 3
    tipo_negocio = models.CharField(max_length=100, choices=TIPO_NEGOCIO_CHOICES, blank=True, null=True, help_text="Tipo principal de negocio (ej. Comercio, Servicios). Puede ser expandido a ManyToMany si aplica varios.")
    actividad_especifica = models.TextField(blank=True, null=True, help_text="Descripción específica de la actividad económica")
    representante_contacto = models.CharField(max_length=255, blank=True, null=True, help_text="Nombre del Representante Legal (para contacto)")
    propietario_contacto = models.CharField(max_length=255, blank=True, null=True, help_text="Nombre del Propietario/Dueño (para contacto - personas naturales)")

    # Auditoría
    fecha_registro = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True, help_text="Indica si el socio está activo")
    #Relaciones
    id_seguro = models.ForeignKey(InformacionSeguroSocio, on_delete=models.SET_NULL, null=True, blank=True, related_name='socios')

    class Meta:
        verbose_name = "Socio"
        verbose_name_plural = "Socios"

    def __str__(self):
        return self.nombre_comercial
























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



class FormularioProductoVida(models.Model):
    perfil = models.ForeignKey('PerfilUsuario', on_delete=models.SET_NULL, null=True, blank=True, related_name='formularios_vida')
    producto = models.ForeignKey('Producto', on_delete=models.SET_NULL, null=True, blank=True, related_name='formularios_vida')
    
    # Declaración de salud
    tiene_enfermedad_grave = models.BooleanField(default=False)
    ha_sido_hospitalizado = models.BooleanField(default=False)
    practica_deportes_extremos = models.BooleanField(default=False)

    # Beneficiario
    nombre_beneficiario = models.CharField(max_length=100)
    relacion_beneficiario = models.CharField(max_length=50)
    porcentaje_beneficiario = models.PositiveIntegerField()

    # Confirmación de términos
    acepta_terminos = models.BooleanField(default=False)
    estado = models.BooleanField(default=False)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Formulario de {self.perfil.user.get_full_name()}"








class Producto(models.Model):

    subservicio = models.OneToOneField('Subservicios', on_delete=models.SET_NULL, null=True, blank=True, related_name='producto')
    precio = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True) 
    descripcion = models.CharField(max_length=255, blank=True, null=True)
    titulo = models.CharField(max_length=255, blank=True, null=True)
    url_html = models.CharField(max_length=255, blank=True, null=True) 
    fecha_creacion = models.DateField(default=date.today)
    usuarios = models.ManyToManyField('PerfilUsuario', related_name='productos', blank=True)


    def __str__(self):
        return f'Producto de {self.subservicio.nombre if self.subservicio else "Sin asignar"}'



class Subservicios(models.Model):
    """
    Modelo para almacenar los sub-servicios ofrecidos.
    Corresponde a la tabla 'Subservicios' en el esquema de la base de datos.
    """
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    fecha_creacion = models.DateField(default=date.today)
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
        return self.beneficio

class Servicios(models.Model):
    """
    Modelo para almacenar los servicios principales.
    Corresponde a la tabla 'Servicios' en el esquema de la base de datos.
    """
    nombre = models.CharField(max_length=100)
    contacto = models.CharField(max_length=100)
    descripcion = models.TextField()
    fecha_creacion = models.DateField()
    requisitos = models.TextField()
    img = models.ImageField(upload_to='servicios/', null=True, blank=True)
    ubicacion = models.CharField(max_length=255)

    id_mas_informacion = models.ForeignKey(Mas_informacion, on_delete=models.SET_NULL, null=True, blank=True, related_name='servicios')
    id_subservicios = models.ManyToManyField(Subservicios, blank=True, related_name='servicios',null=True)
    id_beneficio = models.ForeignKey(Beneficio, on_delete=models.SET_NULL, null=True, blank=True, related_name='servicios_asociados')
    id_socio = models.ForeignKey(Socio, on_delete=models.SET_NULL, null=True, blank=True, related_name='servicios')

    class Meta:
        verbose_name = "Servicio"
        verbose_name_plural = "Servicios"

    def __str__(self):
        return self.nombre




class PerfilUsuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    cedula = models.CharField(max_length=20)
    socio = models.ForeignKey(Socio, on_delete=models.SET_NULL, null=True, blank=True, related_name='perfiles')
    id_solicitud = models.ForeignKey(SolicitudSeguroVida, on_delete=models.SET_NULL, null=True, blank=True, related_name='perfiles')
    imagen = models.ImageField(upload_to='perfiles/', null=True, blank=True)  

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
    f_socio = models.BooleanField(default=False)
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
    servicios = models.ManyToManyField('Servicios', related_name='categorias')
    

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
    id_perfil_usuario = models.ForeignKey(PerfilUsuario, on_delete=models.CASCADE, related_name='facturas',null=True, blank=True)

    class Meta:
        verbose_name = "Factura"
        verbose_name_plural = "Facturas"

    def __str__(self):
        return f"Factura #{self.id} - {self.first_name} {self.last_name}"







#modelos byron
class Mensaje(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mensajes')
    titulo = models.CharField(max_length=255)
    asunto = models.CharField(max_length=255)
    contenido = models.TextField()
    fecha_envio = models.DateTimeField(auto_now_add=True)
    estado = models.BooleanField(default=True)

    def __str__(self):
        return f"Mensaje a {self.usuario.username} - {self.titulo}"


class Publicacion(models.Model):
    autor = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'is_superuser': True})
    titulo = models.CharField(max_length=200)
    contenido = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    servicio = models.ForeignKey(Servicios, on_delete=models.CASCADE)

    def __str__(self):
        return self.titulo

class ImagenPublicacion(models.Model):
    publicacion = models.ForeignKey(Publicacion, related_name='imagenes', on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='publicaciones/')

    def __str__(self):
        return f"Imagen de {self.publicacion.titulo}"            