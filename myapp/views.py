<<<<<<< Updated upstream
from django.shortcuts import render

# Create your views here.
=======
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm,UserChangeForm

from .models import Proyecto, Postulacion, User
from django.contrib.auth.decorators import login_required
from django.forms import ModelForm

class ProyectoForm(ModelForm):
    class Meta:
        model = Proyecto
        fields = ['nombre', 'descripcion', 'fecha_inicio', 'fecha_fin']

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

@login_required
def postular_proyecto(request, proyecto_id):
    proyecto = Proyecto.objects.get(id=proyecto_id)
    if request.method == 'POST':
        Postulacion.objects.create(proyecto=proyecto, usuario=request.user)
        return redirect('proyecto_list')
    return render(request, 'myapp/postular_proyecto.html', {'proyecto': proyecto})

@login_required
def mis_postulaciones(request):
    postulaciones = Postulacion.objects.filter(usuario=request.user)
    return render(request, 'myapp/mis_postulaciones.html', {'postulaciones': postulaciones})    

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
def proyecto_list(request):
    proyectos = Proyecto.objects.all()
    return render(request, 'myapp/proyecto_list.html', {'proyectos': proyectos})

@login_required
def proyecto_detail(request, pk):
    proyecto = Proyecto.objects.get(pk=pk)
    return render(request, 'myapp/proyecto_detail.html', {'proyecto': proyecto})



def index(request):
    return render(request, 'myapp/index.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'myapp/register.html', {'form': form})

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

#VISTA LOGGOUT
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')
    
    
>>>>>>> Stashed changes
