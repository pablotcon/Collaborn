from django import forms
from django.contrib.auth.models import User
from .models import Recurso, Perfil, Comentario, Mensaje, Proyecto, Tarea

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username']

class PerfilForm(forms.ModelForm):
    birth_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        input_formats=['%Y-%m-%d']  # Asegúrate de que el formato de entrada es correcto
    )

    class Meta:
        model = Perfil
        fields = ['bio', 'location', 'birth_date']


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