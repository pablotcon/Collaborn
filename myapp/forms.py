from django import forms
from django.forms import inlineformset_factory
from django.contrib.auth.models import User
from .models import Recurso, Perfil, Comentario, Mensaje, Proyecto, Tarea, ExperienciaLaboral, Educacion, SeguimientoTarea, Subtarea, ComentarioTarea, Categoria

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['nombre', 'apellido', 'telefono', 'fecha_nacimiento', 'avatar', 'website', 'twitter', 'facebook', 'linkedin']

class ExperienciaLaboralForm(forms.ModelForm):
    class Meta:
        model = ExperienciaLaboral
        fields = ['titulo', 'fecha_inicio', 'fecha_fin', 'descripcion']

    def clean_fecha_inicio(self):
        fecha_inicio = self.cleaned_data.get('fecha_inicio')
        if not fecha_inicio:
            raise forms.ValidationError('Este campo es obligatorio.')
        return fecha_inicio

    def clean_fecha_fin(self):
        fecha_fin = self.cleaned_data.get('fecha_fin')
        if not fecha_fin:
            raise forms.ValidationError('Este campo es obligatorio.')
        return fecha_fin

class EducacionForm(forms.ModelForm):
    class Meta:
        model = Educacion
        fields = ['titulo', 'institucion', 'fecha_inicio', 'fecha_fin']

    def clean_fecha_inicio(self):
        fecha_inicio = self.cleaned_data.get('fecha_inicio')
        if not fecha_inicio:
            raise forms.ValidationError('Este campo es obligatorio.')
        return fecha_inicio

    def clean_fecha_fin(self):
        fecha_fin = self.cleaned_data.get('fecha_fin')
        if not fecha_fin:
            raise forms.ValidationError('Este campo es obligatorio.')
        return fecha_fin

ExperienciaLaboralFormSet = inlineformset_factory(Perfil, ExperienciaLaboral, form=ExperienciaLaboralForm, extra=1, can_delete=True)
EducacionFormSet = inlineformset_factory(Perfil, Educacion, form=EducacionForm, extra=1, can_delete=True)

class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['texto']

class MensajeForm(forms.ModelForm):
    class Meta:
        model = Mensaje
        fields = ['receptor', 'contenido']

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
        # Añadir más ciudades según sea necesario
    ]

    fecha_inicio = forms.DateField(
        widget=forms.DateInput(attrs={'id': 'id_fecha_inicio', 'class': 'form-control', 'type': 'date'}),
        label='Fecha de inicio de postulaciones'
    )
    fecha_fin = forms.DateField(
        widget=forms.DateInput(attrs={'id': 'id_fecha_fin', 'class': 'form-control', 'type': 'date'}),
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
    categoria = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Categoría'
    )

    class Meta:
        model = Proyecto
        fields = ['nombre', 'descripcion', 'fecha_inicio', 'fecha_fin', 'ciudad', 'imagen', 'categoria']
class TareaForm(forms.ModelForm):
    class Meta:
        model = Tarea
        fields = ['nombre', 'descripcion', 'fecha_limite', 'asignada_a']
        widgets = {
            'fecha_limite': forms.DateInput(attrs={'type': 'date'}),
        }

class SubtareaForm(forms.ModelForm):
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
