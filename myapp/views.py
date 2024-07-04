from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from .models import Proyecto, Postulacion, User, Notificacion, Mensaje, Recurso
from django.contrib.auth.decorators import login_required
from django.forms import ModelForm
from django.db.models import Q
from .forms import RecursoForm

from django.contrib.auth import logout as auth_logout

# Modulo Recursos
@login_required
def subir_recurso(request):
    if request.method == 'POST':
        form = RecursoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('listar_recursos')
    else:
        form = RecursoForm()
    return render(request, 'myapp/subir_recurso.html', {'form': form})

@login_required
def listar_recursos(request):
    recursos = Recurso.objects.all()
    return render(request, 'myapp/listar_recursos.html', {'recursos': recursos})


@login_required
def recurso_detail(request, pk):
    recurso = get_object_or_404(Recurso, pk=pk)
    
    if request.method == 'POST':
        if 'edit' in request.POST:
            form = RecursoForm(request.POST, request.FILES, instance=recurso)
            if form.is_valid():
                form.save()
                return redirect('recurso_detail', pk=pk)
        elif 'delete' in request.POST:
            recurso.delete()
            return redirect('listar_recursos')
    else:
        form = RecursoForm(instance=recurso)
    
    return render(request, 'myapp/recurso_detail.html', {'recurso': recurso, 'form': form})

# Modulo Mensajes

class MensajeForm(ModelForm):
    class Meta:
        model = Mensaje
        fields = ['receptor', 'contenido']

@login_required
def enviar_mensaje(request):
    if request.method == 'POST':
        form = MensajeForm(request.POST)
        if form.is_valid():
            mensaje = form.save(commit=False)
            mensaje.emisor = request.user
            mensaje.save()
            return redirect('listar_mensajes')
    else:
        form = MensajeForm()
    return render(request, 'myapp/enviar_mensaje.html', {'form': form})

@login_required
def listar_mensajes(request):
    mensajes_recibidos = Mensaje.objects.filter(receptor=request.user)
    return render(request, 'myapp/listar_mensajes.html', {'mensajes': mensajes_recibidos})

# Notificaciones
@login_required
def listar_notificaciones(request):
    notificaciones = Notificacion.objects.filter(usuario=request.user)
    return render(request, 'myapp/listar_notificaciones.html', {'notificaciones': notificaciones})

# Modulo Proyectos

@login_required
def proyecto_list(request):
    query = request.GET.get('q')
    if query:
        proyectos = Proyecto.objects.filter(
            Q(nombre__icontains=query) | Q(descripcion__icontains=query)
        )
    else:
        proyectos = Proyecto.objects.all()
    return render(request, 'myapp/proyecto_list.html', {'proyectos': proyectos})

class ProyectoForm(ModelForm):
    class Meta:
        model = Proyecto
        fields = ['nombre', 'descripcion', 'fecha_inicio', 'fecha_fin']

@login_required
def proyecto_create(request):
    if request.method == 'POST':
        form = ProyectoForm(request.POST)
        if form.is_valid():
            proyecto = form.save(commit=False)
            proyecto.creador = request.user
            proyecto.save()
            return redirect('proyecto_list')
    else:
        form = ProyectoForm()
    return render(request, 'myapp/proyecto_form.html', {'form': form})

@login_required
def proyecto_detail(request, pk):
    proyecto = get_object_or_404(Proyecto, pk=pk)
    
    if request.method == 'POST':
        if 'edit' in request.POST:
            form = ProyectoForm(request.POST, instance=proyecto)
            if form.is_valid():
                form.save()
                return redirect('proyecto_detail', pk=pk)
        elif 'delete' in request.POST:
            proyecto.delete()
            return redirect('proyecto_list')
    else:
        form = ProyectoForm(instance=proyecto)
    
    return render(request, 'myapp/proyecto_detail.html', {'proyecto': proyecto, 'form': form})

#Edits proyect
@login_required
def proyecto_edit(request, pk):
    proyecto = Proyecto.objects.get(pk=pk)
    if request.method == 'POST':
        form = ProyectoForm(request.POST, instance=proyecto)
        if form.is_valid():
            form.save()
            return redirect('proyecto_list')
    else:
        form = ProyectoForm(instance=proyecto)
    return render(request, 'myapp/proyecto_form.html', {'form': form})

@login_required
def proyecto_delete(request, pk):
    proyecto = Proyecto.objects.get(pk=pk)
    if request.method == 'POST':
        proyecto.delete()
        return redirect('proyecto_list')
    return render(request, 'myapp/proyecto_confirm_delete.html', {'proyecto': proyecto})

@login_required
def postular_proyecto(request, proyecto_id):
    proyecto = Proyecto.objects.get(id=proyecto_id)
    if request.method == 'POST':
        Postulacion.objects.create(proyecto=proyecto, usuario=request.user)
        Notificacion.objects.create(
            usuario=proyecto.creador,
            mensaje=f'El usuario {request.user.username} se ha postulado a tu proyecto "{proyecto.nombre}".'
        )
        return redirect('proyecto_list')
    return render(request, 'myapp/postular_proyecto.html', {'proyecto': proyecto})

@login_required
def mis_postulaciones(request):
    postulaciones = Postulacion.objects.filter(usuario=request.user)
    return render(request, 'myapp/mis_postulaciones.html', {'postulaciones': postulaciones})

# Modulo Perfil
@login_required
def ver_perfil(request):
    return render(request, 'myapp/ver_perfil.html', {'user': request.user})

@login_required
def editar_perfil(request):
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('ver_perfil')
    else:
        form = UserChangeForm(instance=request.user)
    return render(request, 'myapp/editar_perfil.html', {'form': form})

# Modulo de Login/Registro
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'myapp/login.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'myapp/register.html', {'form': form})

@login_required
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')
    return render(request, 'myapp/logout.html')

def index(request):
    return render(request, 'myapp/index.html')
