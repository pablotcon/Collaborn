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
        input_formats=['%Y-%m-%d']
    )
    email = forms.EmailField()

    class Meta:
        model = Perfil
        fields = ['nombre', 'apellido', 'telefono', 'birth_date', 'descripcion', 'avatar', 'website', 'twitter', 'facebook', 'linkedin', 'email']

    def __init__(self, *args, **kwargs):
        super(PerfilForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['nombre'].initial = self.instance.nombre
            self.fields['apellido'].initial = self.instance.apellido
            self.fields['telefono'].initial = self.instance.telefono
            self.fields['descripcion'].initial = self.instance.descripcion
            self.fields['email'].initial = self.instance.user.email

    def save(self, *args, **kwargs):
        user = self.instance.user
        user.email = self.cleaned_data['email']
        user.save()
        return super(PerfilForm, self).save(*args, **kwargs)



class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']  # Incluye otros campos si es necesario

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