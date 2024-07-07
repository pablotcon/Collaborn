from django import forms
from django.forms import inlineformset_factory
from django.contrib.auth.models import User
from .models import Recurso, Perfil, Comentario, Mensaje, Proyecto, Tarea, ExperienciaLaboral, Educacion,SeguimientoTarea

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['nombre', 'apellido','telefono', 'birth_date','avatar', 'website', 'twitter', 'facebook', 'linkedin']

class ExperienciaLaboralForm(forms.ModelForm):
    class Meta:
        model = ExperienciaLaboral
        fields = ['titulo', 'fecha_inicio', 'fecha_fin', 'descripcion']

class EducacionForm(forms.ModelForm):
    class Meta:
        model = Educacion
        fields = ['institucion', 'fecha_inicio', 'fecha_fin', 'descripcion']

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
    fecha_inicio = forms.DateField(
        widget=forms.TextInput(attrs={'id': 'id_fecha_inicio', 'class': 'form-control'}),
        label='Fecha de inicio de postulaciones'
    )
    fecha_fin = forms.DateField(
        widget=forms.TextInput(attrs={'id': 'id_fecha_fin', 'class': 'form-control'}),
        label='Fecha de cierre de postulaciones'
    )

    class Meta:
        model = Proyecto
        fields = ['nombre', 'descripcion', 'fecha_inicio', 'fecha_fin']
        
class TareaForm(forms.ModelForm):
    class Meta:
        model = Tarea
        fields = ['nombre', 'descripcion', 'fecha_limite', 'asignada_a']
        widgets = {
            'fecha_limite': forms.DateInput(attrs={'type': 'date'}),
        }

class SeguimientoTareaForm(forms.ModelForm):
    class Meta:
        model = SeguimientoTarea
        fields = ['comentario']