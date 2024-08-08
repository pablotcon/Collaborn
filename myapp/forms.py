# forms.py
from django import forms
from django.forms import inlineformset_factory
from django.contrib.auth.models import User
from .models import Recurso, Perfil,Comentario, Mensaje, Proyecto, Tarea, ExperienciaLaboral, Educacion, SeguimientoTarea, Subtarea, ComentarioTarea, Categoria, Valoracion
from django.utils import timezone
from django.core.exceptions import ValidationError
from .models import Perfil
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class BusquedaEspecialistaForm(forms.Form):
    especialidad = forms.CharField(max_length=200, required=False)
    ubicacion = forms.CharField(max_length=200, required=False)
    disponibilidad = forms.BooleanField(required=False, label='Disponible')


class DisponibilidadForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['disponibilidad']
        labels = {
            'disponibilidad': '¿Disponible para proyectos?',
        }
        widgets = {
            'disponibilidad': forms.CheckboxInput(),
        }
        
class PerfilForm(forms.ModelForm):
    fecha_nacimiento = forms.DateField(
        input_formats=['%d-%m-%Y'],
        widget=forms.DateInput(format='%d-%m-%Y', attrs={'class': 'form-control datepicker', 'placeholder': 'DD-MM-YYYY'})
    )

    class Meta:
        model = Perfil
        fields = [
            'nombre', 'apellido', 'telefono', 'fecha_nacimiento', 'avatar',
            'website', 'twitter', 'facebook', 'linkedin', 'habilidad_1',
            'habilidad_2', 'habilidad_3', 'experiencia', 'especialidad', 'ubicacion', 'disponibilidad'
        ]
        widgets = {
            'habilidad_1': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Habilidad 1'}),
            'habilidad_2': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Habilidad 2'}),
            'habilidad_3': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Habilidad 3'}),
            'experiencia': forms.Textarea(attrs={'rows': 5}),
            'especialidad': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Especialidad'}),
            'ubicacion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ubicación'}),
            'disponibilidad': forms.CheckboxInput(),
            'website': forms.URLInput(attrs={'placeholder': 'No disponible'}),
            'twitter': forms.URLInput(attrs={'placeholder': 'No disponible'}),
            'facebook': forms.URLInput(attrs={'placeholder': 'No disponible'}),
            'linkedin': forms.URLInput(attrs={'placeholder': 'No disponible'}),
        }

class ExperienciaLaboralForm(forms.ModelForm):
    fecha_inicio = forms.DateField(
        input_formats=['%d-%m-%Y'],
        widget=forms.DateInput(format='%d-%m-%Y', attrs={'class': 'form-control datepicker', 'placeholder': 'DD-MM-YYYY'})
    )
    fecha_fin = forms.DateField(
        required=False,
        input_formats=['%d-%m-%Y'],
        widget=forms.DateInput(format='%d-%m-%Y', attrs={'class': 'form-control datepicker', 'placeholder': 'DD-MM-YYYY'})
    )

    
    class Meta:
        model = ExperienciaLaboral
        fields = ['titulo', 'fecha_inicio', 'fecha_fin', 'descripcion']

    def clean_fecha_inicio(self):
        fecha_inicio = self.cleaned_data['fecha_inicio']
        if fecha_inicio > timezone.now().date():
            raise ValidationError("La fecha de inicio no puede ser una fecha futura.")
        return fecha_inicio


class EducacionForm(forms.ModelForm):
    fecha_inicio = forms.DateField(
        input_formats=['%d-%m-%Y'],
        widget=forms.DateInput(format='%d-%m-%Y', attrs={'class': 'form-control datepicker', 'placeholder': 'DD-MM-YYYY'})
    )
    fecha_fin = forms.DateField(
        required=False,
        input_formats=['%d-%m-%Y'],
        widget=forms.DateInput(format='%d-%m-%Y', attrs={'class': 'form-control datepicker', 'placeholder': 'DD-MM-YYYY'})
    )

    class Meta:
        model = Educacion
        fields = ['titulo', 'institucion', 'fecha_inicio', 'fecha_fin']

    def clean_fecha_inicio(self):
        fecha_inicio = self.cleaned_data['fecha_inicio']
        if fecha_inicio > timezone.now().date():
            raise ValidationError("La fecha de inicio no puede ser una fecha futura.")
        return fecha_inicio

ExperienciaLaboralFormSet = inlineformset_factory(Perfil, ExperienciaLaboral, form=ExperienciaLaboralForm, extra=0, can_delete=True)
EducacionFormSet = inlineformset_factory(Perfil, Educacion, form=EducacionForm, extra=0, can_delete=True)

class ValoracionForm(forms.ModelForm):
    class Meta:
        model = Valoracion
        fields = ['puntuacion', 'comentario']
        widgets = {
            'puntuacion': forms.Select(attrs={'class': 'form-control'}),
            'comentario': forms.Textarea(attrs={'class': 'form-control'}),
        }


class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['texto']
        widgets = {
            'texto': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Escribe tu comentario aquí...'}),
        }

class MensajeForm(forms.ModelForm):
    receptor_username = forms.CharField(
        max_length=150, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de usuario del destinatario'})
    )
    imagen = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'}))

    class Meta:
        model = Mensaje
        fields = ['receptor_username', 'contenido', 'imagen']

    def clean(self):
        cleaned_data = super().clean()
        contenido = cleaned_data.get("contenido")
        imagen = cleaned_data.get("imagen")

        if not contenido and not imagen:
            raise forms.ValidationError("Debe proporcionar al menos un mensaje o una imagen.")
        
class RecursoForm(forms.ModelForm):
    class Meta:
        model = Recurso
        fields = ['titulo', 'descripcion', 'archivo']

class ProyectoForm(forms.ModelForm):
    CIUDADES_CHOICES = [
        ('santiago', 'Santiago'),
        ('valparaiso', 'Valparaíso'),
        ('concepcion', 'Concepción'),
        ('la_serena', 'La Serena'),
        ('antofagasta', 'Antofagasta'),
        ('temuco', 'Temuco'),
        ('rancagua', 'Rancagua'),
        ('iquique', 'Iquique'),
        ('puerto_montt', 'Puerto Montt'),
    ]

    CATEGORIAS_CHOICES = [
        ('tecnologia', 'Tecnología'),
        ('educacion', 'Educación'),
        ('salud', 'Salud'),
        ('finanzas', 'Finanzas'),
        ('energia', 'Energía'),
        ('animales', 'Animales'),
    ]
    
    fecha_inicio = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control datepicker', 'placeholder': 'DD-MM-YYYY'}),
        label='Fecha de inicio de postulaciones'
    )
    fecha_fin = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control datepicker', 'placeholder': 'DD-MM-YYYY'}),
        label='Fecha de cierre de postulaciones'
    )
    ciudad = forms.ChoiceField(
        choices=CIUDADES_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Ciudad'
    )
    imagen = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        label='Imagen del proyecto'
    )
    categoria = forms.ChoiceField(
        choices=CATEGORIAS_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Categoría'
    )

    class Meta:
        model = Proyecto
        fields = ['nombre', 'descripcion', 'fecha_inicio', 'fecha_fin', 'ciudad', 'imagen', 'categoria']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
            'ciudad': forms.TextInput(attrs={'class': 'form-control'}),
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
        }

class TareaForm(forms.ModelForm):
    fecha_limite = forms.DateField(
        input_formats=['%d-%m-%Y'],
        widget=forms.DateInput(format='%d-%m-%Y', attrs={'class': 'form-control datepicker', 'placeholder': 'DD-MM-YYYY'})
    )

    class Meta:
        model = Tarea
        fields = ['nombre', 'descripcion', 'fecha_limite', 'asignada_a']

class SubtareaForm(forms.ModelForm):
    fecha_limite = forms.DateField(
        input_formats=['%d-%m-%Y'],
        widget=forms.DateInput(format='%d-%m-%Y', attrs={'class': 'form-control datepicker', 'placeholder': 'DD-MM-YYYY'})
    )

    class Meta:
        model = Subtarea
        fields = ['nombre', 'descripcion', 'fecha_limite', 'completada']

class SeguimientoTareaForm(forms.ModelForm):
    class Meta:
        model = SeguimientoTarea
        fields = ['comentario']

class ComentarioTareaForm(forms.ModelForm):
    class Meta:
        model = ComentarioTarea
        fields = ['texto']
