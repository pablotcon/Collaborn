from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout,update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required, permission_required
from django.forms import ModelForm
from django.db.models import Q
from django.contrib import messages
from .models import Proyecto, Postulacion, User, Notificacion, Mensaje, Recurso, Perfil, Comentario, Tarea
from .forms import RecursoForm, PerfilForm, ComentarioForm, UserForm, MensajeForm, ProyectoForm, TareaForm
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Recurso

@login_required
def recurso_detail(request, pk):
    recurso = get_object_or_404(Recurso, pk=pk)
    return render(request, 'myapp/recurso_detail.html', {'recurso': recurso})

@permission_required('myapp.can_edit_recurso', raise_exception=True)
@login_required
def recurso_edit(request, pk):
    recurso = get_object_or_404(Recurso, pk=pk)
    if request.method == 'POST':
        form = RecursoForm(request.POST, instance=recurso)
        if form.is_valid():
            form.save()
            messages.success(request, 'Recurso editado exitosamente.')
            return redirect('recurso_detail', pk=recurso.pk)
        else:
            messages.error(request, 'Error al editar el recurso.')
    else:
        form = RecursoForm(instance=recurso)
    return render(request, 'myapp/recurso_form.html', {'form': form})

@permission_required('myapp.can_delete_recurso', raise_exception=True)
@login_required
def recurso_delete(request, pk):
    recurso = get_object_or_404(Recurso, pk=pk)
    if request.method == 'POST':
        recurso.delete()
        messages.success(request, 'Recurso eliminado exitosamente.')
        return redirect('listar_recursos')
    return render(request, 'myapp/recurso_confirm_delete.html', {'recurso': recurso})
def historial_actividades(request):
    comentarios = Comentario.objects.filter(autor=request.user).order_by('-fecha_creacion')
    tareas_asignadas = Tarea.objects.filter(asignado_a=request.user).order_by('-fecha_creacion')
    return render(request, 'myapp/historial_actividades.html', {'comentarios': comentarios, 'tareas_asignadas': tareas_asignadas})


# Modulo de Tareas
@login_required
def agregar_tarea(request, proyecto_id):
    proyecto = get_object_or_404(Proyecto, id=proyecto_id)
    if request.method == 'POST':
        form = TareaForm(request.POST)
        if form.is_valid():
            tarea = form.save(commit=False)
            tarea.proyecto = proyecto
            tarea.save()
            messages.success(request, 'Tarea agregada exitosamente.')
            return redirect('listar_tareas', proyecto_id=proyecto.id)
    else:
        form = TareaForm()
    return render(request, 'myapp/agregar_tarea.html', {'form': form})

@login_required
def listar_tareas(request, proyecto_id):
    proyecto = get_object_or_404(Proyecto, id=proyecto_id)
    tareas = proyecto.tareas.all()
    return render(request, 'myapp/listar_tareas.html', {'proyecto': proyecto, 'tareas': tareas})

@login_required
def editar_tarea(request, tarea_id):
    tarea = get_object_or_404(Tarea, id=tarea_id)
    if request.method == 'POST':
        form = TareaForm(request.POST, instance=tarea)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tarea actualizada exitosamente.')
            return redirect('listar_tareas', proyecto_id=tarea.proyecto.id)
    else:
        form = TareaForm(instance=tarea)
    return render(request, 'myapp/editar_tarea.html', {'form': form, 'tarea': tarea})

@login_required
def eliminar_tarea(request, tarea_id):
    tarea = get_object_or_404(Tarea, id=tarea_id)
    proyecto_id = tarea.proyecto.id
    tarea.delete()
    messages.success(request, 'Tarea eliminada exitosamente.')
    return redirect('listar_tareas', proyecto_id=proyecto_id)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Perfil.objects.get_or_create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'perfil'):
        instance.perfil.save()

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
    query = request.GET.get('q')
    recursos = Recurso.objects.all()
    
    if query:
        recursos = recursos.filter(
            Q(titulo__icontains=query) | Q(descripcion__icontains=query)
        )

    return render(request, 'myapp/listar_recursos.html', {'recursos': recursos})


# Modulo Mensajes
@login_required
def enviar_mensaje(request):
    if request.method == 'POST':
        form = MensajeForm(request.POST)
        if form.is_valid():
            mensaje = form.save(commit=False)
            mensaje.emisor = request.user
            mensaje.save()
            Notificacion.objects.create(
                usuario=mensaje.receptor,
                mensaje=f'Has recibido un nuevo mensaje de {request.user.username}.'
            )
            messages.success(request, 'Mensaje enviado exitosamente.')
            return redirect('listar_mensajes')
        else:
            messages.error(request, 'Error al enviar el mensaje.')
    else:
        form = MensajeForm()
    return render(request, 'myapp/enviar_mensaje.html', {'form': form})

@login_required
def listar_mensajes(request):
    mensajes_recibidos = Mensaje.objects.filter(receptor=request.user)
    return render(request, 'myapp/listar_mensajes.html', {'mensajes': mensajes_recibidos})

# Notificaciones
def send_notification(user, message):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"user_{user.id}", 
        {
            "type": "user_notification",
            "message": message,
        }
    )

def user_notification(event):
    message = event['message']
    self.send(text_data=json.dumps({
        'message': message
    }))

@login_required
def listar_notificaciones(request):
    notificaciones = request.user.notificacion_set.filter(leida=False)
    return render(request, 'myapp/listar_notificaciones.html', {'notificaciones': notificaciones})

@login_required
def marcar_notificacion_leida(request, notificacion_id):
    notificacion = get_object_or_404(Notificacion, id=notificacion_id, usuario=request.user)
    notificacion.leida = True
    notificacion.save()
    return redirect('listar_notificaciones')

# Modulo Proyectos
@login_required
def proyecto_list(request):
    query = request.GET.get('q')
    filter_by = request.GET.get('filter_by')
    proyectos = Proyecto.objects.all()
    
    if query:
        proyectos = proyectos.filter(
            Q(nombre__icontains=query) | Q(descripcion__icontains(query))
        )

    if filter_by:
        if filter_by == 'mis_proyectos':
            proyectos = proyectos.filter(creador=request.user)

    return render(request, 'myapp/proyecto_list.html', {'proyectos': proyectos})

@login_required
def crear_proyecto(request):
    if request.method == 'POST':
        form = ProyectoForm(request.POST)
        if form.is_valid():
            proyecto = form.save(commit=False)
            proyecto.creador = request.user
            proyecto.save()
            messages.success(request, 'Proyecto creado exitosamente.')
            return redirect('proyecto_detail', proyecto_id=proyecto.id)
        else:
            messages.error(request, 'Error al crear el proyecto.')
    else:
        form = ProyectoForm()
    return render(request, 'myapp/crear_proyecto.html', {'form': form})

@login_required
def proyecto_detail(request, proyecto_id):
    proyecto = get_object_or_404(Proyecto, id=proyecto_id)
    comentarios = proyecto.comentarios.all()

    if request.method == 'POST':
        form = ComentarioForm(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.proyecto = proyecto
            comentario.autor = request.user
            comentario.save()
            messages.success(request, 'Comentario agregado exitosamente.')
            return redirect('proyecto_detail', proyecto_id=proyecto.id)
        else:
            messages.error(request, 'Error al agregar el comentario.')
    else:
        form = ComentarioForm()

    return render(request, 'myapp/proyecto_detail.html', {'proyecto': proyecto, 'comentarios': comentarios, 'form': form})

@permission_required('myapp.can_edit_proyecto', raise_exception=True)
@login_required
def proyecto_edit(request, pk):
    proyecto = get_object_or_404(Proyecto, pk=pk)
    if request.method == 'POST':
        form = ProyectoForm(request.POST, instance=proyecto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Proyecto editado exitosamente.')
            return redirect('proyecto_list')
        else:
            messages.error(request, 'Error al editar el proyecto.')
    else:
        form = ProyectoForm(instance=proyecto)
    return render(request, 'myapp/proyecto_form.html', {'form': form})


@permission_required('myapp.can_delete_proyecto', raise_exception=True)
@login_required
def proyecto_delete(request, pk):
    proyecto = get_object_or_404(Proyecto, pk=pk)
    if request.method == 'POST':
        proyecto.delete()
        messages.success(request, 'Proyecto eliminado exitosamente.')
        return redirect('proyecto_list')
    return render(request, 'myapp/proyecto_confirm_delete.html', {'proyecto': proyecto})
@login_required
def postular_proyecto(request, proyecto_id):
    proyecto = get_object_or_404(Proyecto, id=proyecto_id)
    if request.method == 'POST':
        # Verificar si el usuario ya se ha postulado
        if Postulacion.objects.filter(proyecto=proyecto, usuario=request.user).exists():
            messages.error(request, 'Ya te has postulado a este proyecto.')
        else:
            Postulacion.objects.create(proyecto=proyecto, usuario=request.user)
            Notificacion.objects.create(
                usuario=proyecto.creador,
                mensaje=f'El usuario {request.user.username} se ha postulado a tu proyecto "{proyecto.nombre}".'
            )
            messages.success(request, 'Te has postulado al proyecto exitosamente.')
        return redirect('proyecto_detail', pk=proyecto_id)
    return render(request, 'myapp/proyecto_detail.html', {'proyecto': proyecto})

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
    user = request.user
    perfil = get_object_or_404(Perfil, user=user)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        perfil_form = PerfilForm(request.POST, request.FILES, instance=perfil)
        if user_form.is_valid() and perfil_form.is_valid():
            user_form.save()
            perfil_form.save()
            messages.success(request, 'Perfil actualizado exitosamente.')
            return redirect('ver_perfil')
        else:
            messages.error(request, 'Por favor corrija los errores a continuación.')
    else:
        user_form = UserForm(instance=user)
        perfil_form = PerfilForm(instance=perfil)
    return render(request, 'myapp/editar_perfil.html', {'user_form': user_form, 'perfil_form': perfil_form})

@login_required
def cambiar_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Mantener la sesión después de cambiar la contraseña
            messages.success(request, 'Su contraseña ha sido cambiada exitosamente.')
            return redirect('ver_perfil')
        else:
            messages.error(request, 'Por favor corrija los errores a continuación.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'myapp/cambiar_password.html', {'form': form})

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
            user = form.save()
            # Asegurarse de que el perfil se crea si no existe
            Perfil.objects.get_or_create(user=user)
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'myapp/register.html', {'form': form})

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')
    return render(request, 'myapp/logout.html')

def index(request):
    return render(request, 'myapp/index.html')
