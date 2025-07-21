from django import forms
from .models import *
from django.forms import inlineformset_factory
from django.core.exceptions import ValidationError
import re 

class SocioPersonalForm(forms.ModelForm):
    # Campos del Slide 1: Datos Personales
    razon_social = forms.CharField(label="Razón Social:", max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    nombre_comercial = forms.CharField(label="Nombre Comercial / Nombres y Apellidos:", max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
    ruc_cedula = forms.CharField(label="RUC / Cédula:", max_length=13, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email_principal = forms.EmailField(label="Correo Electrónico:", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    REDES_SOCIALES_CHOICES = [('WhatsApp', 'WhatsApp'), ('Facebook', 'Facebook'), ('Instagram', 'Instagram'), ('YouTube', 'YouTube'), ('TikTok', 'TikTok'), ]
    redes_sociales_checkboxes = forms.MultipleChoiceField(label="Red social que utiliza:", choices=REDES_SOCIALES_CHOICES, widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}), required=False)

    class Meta:
        model = Socio
        fields = ['razon_social', 'nombre_comercial', 'ruc_cedula', 'email_principal', 'redes_sociales_checkboxes']
        widgets = {'razon_social': forms.TextInput(attrs={'id': 'razon_social'}), 'nombre_comercial': forms.TextInput(attrs={'id': 'nombre_comercial'}), 'ruc_cedula': forms.TextInput(attrs={'id': 'ruc_cedula'}), 'email_principal': forms.EmailInput(attrs={'id': 'email'}),}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.redes_sociales:
            self.initial['redes_sociales_checkboxes'] = self.instance.redes_sociales.split(',')
        for field_name, field in self.fields.items():
            if field_name != 'redes_sociales_checkboxes':
                 if 'class' in field.widget.attrs:
                     field.widget.attrs['class'] += ' form-control'
                 else:
                     field.widget.attrs['class'] = 'form-control'
            if field_name == 'email_principal':
                field.widget.attrs['id'] = 'email'

    def clean(self):
        cleaned_data = super().clean()
        redes_seleccionadas = cleaned_data.get('redes_sociales_checkboxes')
        if redes_seleccionadas:
            cleaned_data['redes_sociales'] = ','.join(redes_seleccionadas)
        else:
            cleaned_data['redes_sociales'] = '' 
        return cleaned_data


class SocioBusinessForm(forms.ModelForm):
    # Campos del Slide 2: Representante Legal y Datos de Empresa
    class Meta:
        model = Socio
        fields = ['cedula_representante', 'apellidos_nombres_representante', 'direccion_principal', 'calle', 'numero', 'interseccion', 'referencia', 'parroquia', 'ciudad', 'pais', 'pagina_web', 'email_empresa', 'telefono1', 'telefono2', 'celular',]
        widgets = {
            'cedula_representante': forms.TextInput(attrs={'id': 'cedula_representante'}),
            'apellidos_nombres_representante': forms.TextInput(attrs={'id': 'apellidos_representante'}),
            'direccion_principal': forms.TextInput(attrs={'id': 'direccion'}),
            'calle': forms.TextInput(attrs={'id': 'calle'}),
            'numero': forms.TextInput(attrs={'id': 'numero'}),
            'interseccion': forms.TextInput(attrs={'id': 'interseccion'}),
            'referencia': forms.TextInput(attrs={'id': 'referencia'}),
            'parroquia': forms.TextInput(attrs={'id': 'parroquia'}),
            'ciudad': forms.TextInput(attrs={'id': 'ciudad'}),
            'pais': forms.TextInput(attrs={'id': 'pais'}),
            'pagina_web': forms.URLInput(attrs={'id': 'web'}),
            'email_empresa': forms.EmailInput(attrs={'id': 'email_empresa'}),
            'telefono1': forms.TextInput(attrs={'id': 'telefono1'}),
            'telefono2': forms.TextInput(attrs={'id': 'telefono2'}),
            'celular': forms.TextInput(attrs={'id': 'celular'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if 'class' in field.widget.attrs:
                field.widget.attrs['class'] += ' form-control'
            else:
                field.widget.attrs['class'] = 'form-control'


class SocioActivityContactForm(forms.ModelForm):
    # Campos del Slide 3: Actividad Económica y Contactos
    TIPO_NEGOCIO_CHOICES_FORM = [('Comercio', 'Comercio'), ('Servicios', 'Servicios'), ('Importación/Exportación', 'Importación/Exportación'), ('Industria', 'Industria'), ('Otros', 'Otros'),]
    tipo_negocio_checkboxes = forms.MultipleChoiceField(label="Tipo de Negocio:", choices=TIPO_NEGOCIO_CHOICES_FORM, widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}), required=False)

    class Meta:
        model = Socio
        fields = ['actividad_especifica', 'representante_contacto', 'propietario_contacto', 'tipo_negocio_checkboxes']
        widgets = {'actividad_especifica': forms.TextInput(attrs={'id': 'actividad_especifica'}), 'representante_contacto': forms.TextInput(attrs={'id': 'representante_contacto'}), 'propietario_contacto': forms.TextInput(attrs={'id': 'propietario_contacto'}),}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.tipo_negocio:
            self.initial['tipo_negocio_checkboxes'] = [self.instance.tipo_negocio]

        for field_name, field in self.fields.items():
            if field_name != 'tipo_negocio_checkboxes':
                if 'class' in field.widget.attrs:
                    field.widget.attrs['class'] += ' form-control'
                else:
                    field.widget.attrs['class'] = 'form-control'

    def clean(self):
        cleaned_data = super().clean()
        tipos_seleccionados = cleaned_data.get('tipo_negocio_checkboxes')
        if tipos_seleccionados:
            cleaned_data['tipo_negocio'] = tipos_seleccionados[0]
        else:
            cleaned_data['tipo_negocio'] = None

        return cleaned_data



class InformacionSeguroSocioForm(forms.ModelForm):
    # Campos del Slide 4: Confirmación (Información del Titular del Seguro + Único Beneficiario)
    nombre_titular = forms.CharField(label="Nombre del Titular:", max_length=255, widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'nombre_titular'}))
    telefono_titular = forms.CharField(label="Teléfono:", max_length=20, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'telefono_titular'}))
    fecha_nacimiento_titular = forms.DateField(label="Fecha de Nacimiento:", required=False, widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'id': 'fecha_nacimiento'}))
    cedula_titular = forms.CharField(label="C.C.:", max_length=10, widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'cedula_titular'}))
    nombre_beneficiario = forms.CharField(label="Nombre del Beneficiario:", max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'beneficiario_1'}))
    porcentaje_beneficiario = forms.DecimalField(label="Porcentaje Beneficiario:", max_digits=5, decimal_places=2, required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'id': 'porcentaje_1'}))
    firma_titular = forms.CharField(label="Firma:", max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'firma', 'placeholder': 'Nombre completo para firma'}))

    class Meta:
        model = InformacionSeguroSocio
        fields = ['nombre_titular', 'telefono_titular', 'fecha_nacimiento_titular', 'cedula_titular', 'nombre_beneficiario', 'porcentaje_beneficiario', 'firma_titular',]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if 'class' in field.widget.attrs:
                field.widget.attrs['class'] += ' form-control'
            else:
                field.widget.attrs['class'] = 'form-control'













#segundos modleos de formualrios#
# --- Formulario para la Sección I (Datos del Solicitante) y Sección V (Declaraciones Finales) ---
class SolicitudSeguroVidaForm(forms.ModelForm):

    correo_trabajo = forms.CharField(required=False,widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'ejemplo@dominio.com'}),label="Correo Electrónico Trabajo")
    def clean_numero_identificacion(self):
        numero = self.cleaned_data['numero_identificacion']
        if not re.fullmatch(r'^\d{10}$', numero) and not re.fullmatch(r'^\d{13}$', numero):
            raise forms.ValidationError("El número de identificación debe ser de 10 o 13 dígitos numéricos.")
        return numero

    def clean(self):
        cleaned_data = super().clean()
        otros_seguros_vida = cleaned_data.get('otros_seguros_vida')
        especifique_companias_otros_seguros = cleaned_data.get('especifique_companias_otros_seguros')
        if otros_seguros_vida and not especifique_companias_otros_seguros:
            self.add_error('especifique_companias_otros_seguros', "Este campo es requerido si tiene otros seguros de vida.")
        return cleaned_data

    class Meta:
        model = SolicitudSeguroVida
        fields = [
            'tipo_identificacion', 'numero_identificacion', 'nombres', 'apellidos',
            'fecha_nacimiento', 'estado_civil', 'direccion_domicilio', 'correo_domicilio',
            'telefono_domicilio', 'celular_domicilio', 'nombre_empresa', 'direccion_trabajo',
            'correo_trabajo', 'telefono_trabajo', 'ocupacion', 'envio_correspondencia',
            'otros_seguros_vida', 'especifique_companias_otros_seguros', 'es_usted',
            'lugar_firma', 'firma_electronica_generada'
        ]
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}),
            'correo_domicilio': forms.EmailInput(attrs={'placeholder': 'ejemplo@dominio.com'}),
            'celular_domicilio': forms.TextInput(attrs={'placeholder': 'Ej. 0991234567'}),
            'nombres': forms.TextInput(attrs={'class': 'form-control'}),
            'apellidos': forms.TextInput(attrs={'class': 'form-control'}),
            'numero_identificacion': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion_domicilio': forms.TextInput(attrs={'class': 'form-control'}),
            'lugar_firma': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'tipo_identificacion': "Tipo de identificación",
            'numero_identificacion': "Número de identificación",
            'nombres': "Nombres",
            'apellidos': "Apellidos",
            'fecha_nacimiento': "Fecha de nacimiento",
            'estado_civil': "Estado Civil",
            'direccion_domicilio': "Dirección Domicilio",
            'correo_domicilio': "Correo Electrónico Domicilio",
            'telefono_domicilio': "Teléfono Domicilio",
            'celular_domicilio': "Celular Domicilio",
            'nombre_empresa': "Nombre de la empresa",
            'direccion_trabajo': "Dirección Trabajo",
            'correo_trabajo': "Correo Electrónico Trabajo",
            'telefono_trabajo': "Teléfono Trabajo",
            'ocupacion': "Ocupación (a que se dedica)",
            'envio_correspondencia': "Envío de correspondencia",
            'otros_seguros_vida': "¿Tiene o está tramitando otros seguros de vida?",
            'especifique_companias_otros_seguros': "Especifique compañías:",
            'es_usted': "Es usted",
            'lugar_firma': "Lugar de Firma",
            'firma_electronica_generada': "¿Firma electrónica generada?",
        }



# --- Formulario para la Sección II: Declaración del Estado de Salud ---
class DeclaracionSaludForm(forms.ModelForm):
    def clean_peso_kg(self):
        peso = self.cleaned_data.get('peso_kg')
        if peso is not None and (peso < 1 or peso > 300): 
            raise forms.ValidationError("El peso debe estar entre 1 y 300 kg.")
        return peso

    def clean_estatura_cm(self):
        estatura = self.cleaned_data.get('estatura_cm')
        if estatura is not None and (estatura < 50 or estatura > 250): 
            raise forms.ValidationError("La estatura debe estar entre 50 y 250 cm.")
        return estatura

    def clean(self):
        cleaned_data = super().clean()
        peso_ha_cambiado = cleaned_data.get('peso_ha_cambiado')
        cuanto_peso_cambio = cleaned_data.get('cuanto_peso_cambio')
        peso_cambio_intencional = cleaned_data.get('peso_cambio_intencional')
        causa_peso_cambio = cleaned_data.get('causa_peso_cambio')
        if peso_ha_cambiado and not cuanto_peso_cambio:
            self.add_error('cuanto_peso_cambio', "Este campo es requerido si su peso ha cambiado.")
        if peso_cambio_intencional and not causa_peso_cambio:
            self.add_error('causa_peso_cambio', "Este campo es requerido si el cambio de peso fue intencional.")

        consume_alcohol = cleaned_data.get('consume_alcohol')
        cuales_alcohol = cleaned_data.get('cuales_alcohol')
        cuanto_diariamente_alcohol = cleaned_data.get('cuanto_diariamente_alcohol')

        if consume_alcohol and not cuales_alcohol:
            self.add_error('cuales_alcohol', "Este campo es requerido si consume alcohol.")
        if consume_alcohol and not cuanto_diariamente_alcohol:
            self.add_error('cuanto_diariamente_alcohol', "Este campo es requerido si consume alcohol.")

        uso_estupefacientes = cleaned_data.get('uso_estupefacientes')
        cuales_estupefacientes = cleaned_data.get('cuales_estupefacientes')
        hasta_cuando_estupefacientes = cleaned_data.get('hasta_cuando_estupefacientes')

        if uso_estupefacientes and not cuales_estupefacientes:
            self.add_error('cuales_estupefacientes', "Este campo es requerido si ha usado estupefacientes.")
        if uso_estupefacientes and not hasta_cuando_estupefacientes:
            self.add_error('hasta_cuando_estupefacientes', "Este campo es requerido si ha usado estupefacientes.")

        esta_embarazada = cleaned_data.get('esta_embarazada')
        cuantos_meses_embarazo = cleaned_data.get('cuantos_meses_embarazo')

        if esta_embarazada and not cuantos_meses_embarazo:
            self.add_error('cuantos_meses_embarazo', "Este campo es requerido si está embarazada.")

        return cleaned_data

    class Meta:
        model = DeclaracionSalud
        exclude = ['solicitud']
        widgets = {
            'peso_kg': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 300}),
            'estatura_cm': forms.NumberInput(attrs={'class': 'form-control', 'min': 50, 'max': 250}),
            'tension_arterial_sistolica': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. 120'}),
            'tension_arterial_diastolica': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. 80'}),
            'cuanto_peso_cambio': forms.TextInput(attrs={'class': 'form-control'}),
            'causa_peso_cambio': forms.TextInput(attrs={'class': 'form-control'}),
            'cuales_alcohol': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Cerveza, vino, etc.'}),
            'cuanto_diariamente_alcohol': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. 10 cervezas al día'}),
            'cuales_estupefacientes': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. cocaina, marihuana, etc.'}),
            'hasta_cuando_estupefacientes': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej.5 0 4 veces al mes'}),
            'cuantos_meses_embarazo': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 12,'placeholder': 'Ej. 5 meses'}),
            'cuando_ultima_vez': forms.DateInput(attrs={'type': 'date'}),
            'otra_declaracion_salud': forms.Textarea(attrs={'rows': 3}),
            # Nuevos widgets
            'detalle_preguntas_salud': forms.Textarea(attrs={'rows': 3}),
            'nombre_medico': forms.TextInput(attrs={'class': 'form-control'}),
            'medico_ultima_vez': forms.TextInput(attrs={'class': 'form-control'}),
            'motivo_ultima_vez': forms.TextInput(attrs={'class': 'form-control'}),
            'cantidad_fumada': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. 10 cigarrillos al día'}),
        }
        labels = {
            'peso_kg': "Peso (kg)",
            'estatura_cm': "Estatura (cm)",
            'tension_arterial_sistolica': "Tensión Arterial Sistólica",
            'tension_arterial_diastolica': "Tensión Arterial Diastólica",
            'peso_ha_cambiado': "¿Su peso ha aumentado o disminuido durante el último año?",
            'cuanto_peso_cambio': "¿Cuánto?",
            'peso_cambio_intencional': "¿Intencionalmente?",
            'causa_peso_cambio': "Causa:",
            'pregunta1_salud': "1. ¿Afecciones del corazón o aparato circulatorio por ejemplo infartos, palpitaciones, opresión, síncope, angina de pecho, defecto cardíaco congénito, tensión arterial elevada, flebitis, varices?",
            'pregunta2_salud': "2. ¿Afecciones de los órganos respiratorios (asma, bronquitis crónica, tuberculosis, enfisema, etc.)?",
            'pregunta3_salud': "3. ¿Ha padecido o padece de enfermedad circulatoria o ha tenido accidente vascular cerebral?",
            'pregunta4_salud': "4. ¿Enfermedades del sistema endocrino (diabetes, tiroides, etc.), del sistema urinario (cálculos, etc.) o del sistema hematopoyético?",
            'pregunta5_salud': "5. ¿Cirrosis hepática, hepatitis C o insuficiencia hepática?",
            'pregunta6_salud': "6. ¿Edema o supuración o aumento de volumen de los ganglios linfáticos?",
            'pregunta7_salud': "7. ¿Afecciones del cerebro o del sistema nervioso (convulsiones, parálisis, epilepsia, dolor de cabeza crónico, etc.)?",
            'pregunta8_salud': "8. ¿Afecciones del aparato digestivo (estómago, intestino, hígado, páncreas, vesícula)?",
            'pregunta9_salud': "9. ¿Enfermedades de la piel (lupus, psoriasis, etc.)?",
            'pregunta10_salud': "10. ¿Enfermedades infecciosas (VIH, SIDA, etc.)?",
            # Nuevas preguntas 11–28
            'pregunta11_salud': "11. ¿Afecciones urinarias o genitales? (riñones, próstata, etc.)",
            'pregunta12_salud': "12. ¿Enfermedades de la sangre, gota, hernia, etc.?",
            'pregunta13_salud': "13. ¿Enfermedades venéreas o de transmisión sexual?",
            'pregunta14_salud': "14. ¿Accidente grave o intoxicación?",
            'pregunta15_salud': "15. ¿Enfermedades de los oídos?",
            'pregunta16_salud': "16. ¿Enfermedades de los ojos?",
            'pregunta17_salud': "17. ¿Tratamiento por psiquiatra o psicólogo?",
            'pregunta18_salud': "18. ¿HIV o SIDA?",
            'pregunta19_salud': "19. ¿Le han prescrito medicamentos en los últimos 12 meses?",
            'pregunta20_salud': "20. ¿Le han indicado reposo o desintoxicación?",
            'pregunta21_salud': "21. ¿Ha recibido transfusiones?",
            'pregunta22_salud': "22. ¿Le han recomendado no donar sangre?",
            'pregunta23_salud': "23. ¿Tiene capacidad de trabajo reducida?",
            'pregunta24_salud': "24. ¿Ha dejado de trabajar por más de 3 semanas en los últimos 5 años?",
            'pregunta25_salud': "25. ¿Antecedentes hereditarios (diabetes, corazón, etc.)?",
            'pregunta26_salud': "26. ¿Intervención quirúrgica?",
            'pregunta27_salud': "27. ¿Hospitalización pendiente?",
            'pregunta28_salud': "28. ¿Cualquier otra enfermedad no declarada?",

            # Fumar
            'fuma': "¿Fuma usted?",
            'cantidad_fumada': "¿Cuánto diariamente? (cigarrillos, puros, etc.)",

            # Detalles
            'detalle_preguntas_salud': "Especifique detalles si respondió SÍ a alguna pregunta",
            'nombre_medico': "Nombre de su médico de cabecera",
            'medico_ultima_vez': "Médico que le trató por última vez",
            'motivo_ultima_vez': "Motivo de la última consulta",

            # Alcoholes
            'consume_alcohol': "¿Consume usted bebidas alcohólicas?",
            'cuales_alcohol': "¿Cuáles?",
            'cuanto_diariamente_alcohol': "¿Cuánto diariamente?",

            # Estupefacientes
            'uso_estupefacientes': "¿Hace o ha hecho uso de estupefacientes?",
            'cuales_estupefacientes': "¿Cuáles?",
            'hasta_cuando_estupefacientes': "¿Hasta cuándo?",
            'toma_anticonceptivos': "a) ¿Toma Usted anticonceptivos?",
            'esta_embarazada': "b) ¿Está usted embarazada?",
            'cuantos_meses_embarazo': "¿Cuántos meses?",
            'enfermedad_ginecologica': "c) ¿Ha sufrido alguna enfermedad ginecológica (ovarios, senos, etc.)?",
            'medico_cabecera': "¿Quién es su médico de cabecera?",
            'medico_ultima_vez': "¿Quién es el médico que le ha tratado por última vez?",
            'cuando_ultima_vez': "Cuando:",
            'motivo_ultima_vez': "Motivo:",
            'otra_declaracion_salud': "¿Tiene Usted alguna otra cosa que declarar sobre su salud? Indique:",
        }






"""
# --- Formulario para los detalles de la Declaración de Salud (tabla dinámica) ---
from django import forms
from django.forms import modelformset_factory
from .models import DetalleDeclaracionSalud

# Cambiar el formulario individual por un formset
DetalleDeclaracionSaludFormSet = modelformset_factory(
    DetalleDeclaracionSalud,
    fields=('numero_pregunta', 'detalle', 'cuando', 'duracion', 'secuelas', 'medico_tratante'),
    extra=1,  # Número de formularios vacíos por defecto
    can_delete=True,
    widgets={
        'numero_pregunta': forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'min': 1, 'max': 28}),
        'detalle': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
        'cuando': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
        'duracion': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
        'secuelas': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
        'medico_tratante': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
    }
)

"""



# --- Formulario para la Sección III: Deportes y Actividades Recreacionales ---

class DeporteActividadForm(forms.ModelForm):
    class Meta:
        model = DeporteActividad
        exclude = ['solicitud']
        widgets = {
            'nombre_actividad': forms.TextInput(attrs={'class': 'form-control'}),
            'con_competicion': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'es_piloto': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'paracaidismo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'nombre_actividad': "¿Qué deportes y/o actividades recreacionales practica?",
            'con_competicion': "¿Con competición?",
            'es_piloto': "¿Es piloto o está en proceso de serlo?",
            'paracaidismo': "¿Paracaidismo?",
        }




# --- Formulario para la Sección IV: Designación de Beneficiarios ---
class BeneficiarioForm(forms.ModelForm):
    def clean_porcentaje(self):
        porcentaje = self.cleaned_data.get('porcentaje')
        if porcentaje is not None and (porcentaje < 0 or porcentaje > 100):
            raise forms.ValidationError("El porcentaje debe estar entre 0 y 100.")
        return porcentaje

    class Meta:
        model = Beneficiario
        exclude = ['solicitud']
        widgets = {'nombres_completos': forms.TextInput(attrs={'class': 'form-control'}), 'direccion': forms.TextInput(attrs={'class': 'form-control'}), 'fecha_nacimiento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}), 'parentesco': forms.TextInput(attrs={'class': 'form-control'}), 'cedula_identidad': forms.TextInput(attrs={'class': 'form-control'}), 'porcentaje': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 100}),}
        labels = {'nombres_completos': "Nombres completos", 'direccion': "Dirección", 'fecha_nacimiento': "Fecha de nacimiento", 'parentesco': "Parentesco", 'cedula_identidad': "C.I.", 'porcentaje': "Porcentaje (%)",}
        required = {'nombres_completos': True, 'direccion': True, 'fecha_nacimiento': True, 'parentesco': True, 'porcentaje': True,}