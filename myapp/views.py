from django.forms import ModelForm, modelform_factory
from asgiref.sync import async_to_sync
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.db.models import Q
from django.contrib import messages
from .models import Proyecto, Postulacion, User, Notificacion, Mensaje, Recurso, Perfil, Comentario, Tarea, Actividad, SeguimientoTarea, Subtarea, Educacion, ExperienciaLaboral
from .forms import RecursoForm, PerfilForm, ComentarioForm, UserForm, MensajeForm, ProyectoForm, TareaForm, SeguimientoTareaForm, EducacionFormSet, ExperienciaLaboralFormSet, EducacionForm, SubtareaForm, ComentarioTareaForm, ExperienciaLaboralForm
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group
from channels.layers import get_channel_layer
from django.urls import reverse
import json
from django.utils import timezone
from django.http import JsonResponse
from django.template.loader import render_to_string
# Functions related to Task Management
@login_required
def admin_panel_tareas(request):
    if not request.user.is_staff:
        return redirect('index')
    
    proyectos = Proyecto.objects.all()
    tareas_por_proyecto = {proyecto: Tarea.objects.filter(proyecto=proyecto) for proyecto in proyectos}
    
    return render(request, 'myapp/admin_panel_tareas.html', {'tareas_por_proyecto': tareas_por_proyecto})

@login_required
def actualizar_estado_tarea(request, tarea_id):
    tarea = get_object_or_404(Tarea, id=tarea_id)
    if request.method == 'POST':
        tarea.completada = not tarea.completada
        tarea.save()
        messages.success(request, 'El estado de la tarea ha sido actualizado.')
    return redirect('detalle_tarea', tarea_id=tarea.id)

@login_required
def detalle_tarea(request, tarea_id):
    tarea = get_object_or_404(Tarea, id=tarea_id)
    subtareas = tarea.subtareas.all()
    seguimientos = SeguimientoTarea.objects.filter(tarea=tarea).order_by('-fecha')
    comentarios = tarea.comentarios.all().order_by('-fecha_creacion')

    if request.method == 'POST':
        if 'comentario' in request.POST:
            comentario_form = ComentarioTareaForm(request.POST)
            if comentario_form.is_valid():
                comentario = comentario_form.save(commit=False)
                comentario.tarea = tarea
                comentario.autor = request.user
                comentario.save()
                return redirect('detalle_tarea', tarea_id=tarea.id)
        elif 'seguimiento' in request.POST:
            seguimiento_form = SeguimientoTareaForm(request.POST)
            if seguimiento_form.is_valid():
                seguimiento = seguimiento_form.save(commit=False)
                seguimiento.tarea = tarea
                seguimiento.autor = request.user
                seguimiento.save()
                return redirect('detalle_tarea', tarea_id=tarea.id)
        elif 'subtarea' in request.POST:
            subtarea_form = SubtareaForm(request.POST)
            if subtarea_form.is_valid():
                subtarea = subtarea_form.save(commit=False)
                subtarea.tarea = tarea
                subtarea.save()
                return redirect('detalle_tarea', tarea_id=tarea.id)
    else:
        comentario_form = ComentarioTareaForm()
        seguimiento_form = SeguimientoTareaForm()
        subtarea_form = SubtareaForm()

    return render(request, 'myapp/detalle_tarea.html', {
        'tarea': tarea,
        'subtareas': subtareas,
        'seguimientos': seguimientos,
        'comentarios': comentarios,
        'comentario_form': comentario_form,
        'seguimiento_form': seguimiento_form,
        'subtarea_form': subtarea_form
    })

@login_required
def eliminar_tarea(request, tarea_id):
    tarea = get_object_or_404(Tarea, id=tarea_id)
    next_url = request.GET.get('next', 'proyecto_lista')  # Por defecto redirige a 'proyecto_lista' si 'next' no está presente

    if request.method == 'POST':
        if 'confirm' in request.POST:
            tarea.delete()
            messages.success(request, 'Tarea eliminada exitosamente.')
            return redirect(next_url)
        elif 'cancel' in request.POST:
            messages.info(request, 'Eliminación cancelada.')
            return redirect(next_url)

    return render(request, 'myapp/eliminar_tarea.html', {'tarea': tarea, 'next': next_url})

@login_required
@permission_required('myapp.add_tarea', raise_exception=True)
def agregar_tarea(request, proyecto_id):
    proyecto = get_object_or_404(Proyecto, id=proyecto_id)
    if request.method == 'POST':
        form = TareaForm(request.POST)
        if form.is_valid():
            tarea = form.save(commit=False)
            tarea.proyecto = proyecto
            tarea.save()

            # Crear una notificación para el usuario asignado a la tarea
            if tarea.asignada_a:
                Notificacion.objects.create(
                    receptor=tarea.asignada_a,
                    mensaje=f"Se te ha asignado una nueva tarea: {tarea.nombre}",
                    url=f"/tareas/{tarea.id}/"
                )

            messages.success(request, 'Tarea agregada exitosamente.')
            return redirect('listar_tareas', proyecto_id=proyecto.id)
        else:
            messages.error(request, 'Error al agregar la tarea.')
    else:
        form = TareaForm()
    return render(request, 'myapp/agregar_tarea.html', {'form': form, 'proyecto': proyecto})

@login_required

def agregar_subtarea(request, tarea_id):
    tarea = get_object_or_404(Tarea, id=tarea_id)
    if request.method == 'POST':
        form = SubtareaForm(request.POST)
        if form.is_valid():
            subtarea = form.save(commit=False)
            subtarea.tarea = tarea
            subtarea.save()
            messages.success(request, 'Subtarea agregada exitosamente.')
            return redirect('detalle_tarea', tarea_id=tarea.id)
        else:
            messages.error(request, 'Error al agregar la subtarea.')
    else:
        form = SubtareaForm()
    return render(request, 'myapp/agregar_subtarea.html', {'form': form, 'tarea': tarea})


@login_required
def listar_tareas(request, proyecto_id):
    proyecto = get_object_or_404(Proyecto, id=proyecto_id)
    tareas = Tarea.objects.filter(proyecto=proyecto)
    
    query = request.GET.get('q')
    if query:
        tareas = tareas.filter(nombre__icontains=query)
    
    return render(request, 'myapp/listar_tareas.html', {'proyecto': proyecto, 'tareas': tareas})

@login_required
def editar_tarea(request, tarea_id):
    tarea = get_object_or_404(Tarea, id=tarea_id)
    proyecto_id = tarea.proyecto.id
    if request.method == 'POST':
        form = TareaForm(request.POST, instance=tarea)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tarea editada exitosamente.')
            return redirect('listar_tareas', proyecto_id=proyecto_id)
        else:
            messages.error(request, 'Error al editar la tarea.')
    else:
        form = TareaForm(instance=tarea)
    return render(request, 'myapp/editar_tarea.html', {'form': form, 'proyecto_id': proyecto_id})

@login_required
def confirmar_eliminar_tarea(request, tarea_id):
    tarea = get_object_or_404(Tarea, id=tarea_id)
    if request.method == 'POST':
        tarea.delete()
        messages.success(request, 'Tarea eliminada exitosamente.')
        return redirect('admin_panel_tareas')
    return render(request, 'myapp/confirmar_eliminar_tarea.html', {'tarea': tarea})

@login_required
def seguir_tarea(request, tarea_id):
    tarea = get_object_or_404(Tarea, id=tarea_id)
    seguimiento, created = SeguimientoTarea.objects.get_or_create(usuario=request.user, tarea=tarea)
    if created:
        messages.success(request, 'Ahora sigues esta tarea.')
    else:
        messages.info(request, 'Ya sigues esta tarea.')
    return redirect('detalle_tarea', tarea_id=tarea_id)

@login_required
def dejar_seguir_tarea(request, tarea_id):
    tarea = get_object_or_404(Tarea, id=tarea_id)
    seguimiento = get_object_or_404(SeguimientoTarea, usuario=request.user, tarea=tarea)
    seguimiento.delete()
    messages.success(request, 'Has dejado de seguir esta tarea.')
    return redirect('detalle_tarea', tarea_id=tarea_id)

@login_required
def listar_seguimientos(request):
    seguimientos = request.user.seguimientos.all()
    return render(request, 'myapp/listar_seguimientos.html', {'seguimientos': seguimientos})

@login_required
def agregar_seguimiento(request, tarea_id):
    tarea = get_object_or_404(Tarea, id=tarea_id)
    if request.method == 'POST':
        form = SeguimientoTareaForm(request.POST)
        if form.is_valid():
            seguimiento = form.save(commit=False)
            seguimiento.tarea = tarea
            seguimiento.usuario = request.user
            seguimiento.save()
            return redirect('detalle_tarea', tarea_id=tarea.id)
    else:
        form = SeguimientoTareaForm()
    return render(request, 'myapp/detalle_tarea.html', {'tarea': tarea, 'form': form})

@login_required
def actualizar_estado_tarea(request, tarea_id):
    tarea = get_object_or_404(Tarea, id=tarea_id)
    if request.method == 'POST':
        tarea.completada = not tarea.completada
        tarea.save()
        messages.success(request, 'El estado de la tarea ha sido actualizado.')
    return redirect('detalle_tarea', tarea_id=tarea.id)

# Function to send notifications
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
    # Note: 'self' is not defined in this function; this part needs to be adjusted
    self.send(text_data=json.dumps({
        'message': message
    }))




# Functions related to User Profile
@login_required
def editar_perfil(request):
    perfil = request.user.perfil

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        perfil_form = PerfilForm(request.POST, request.FILES, instance=perfil)
        experiencia_formset = ExperienciaLaboralFormSet(request.POST, request.FILES, instance=perfil)
        educacion_formset = EducacionFormSet(request.POST, request.FILES, instance=perfil)
        
        if user_form.is_valid() and perfil_form.is_valid() and experiencia_formset.is_valid() and educacion_formset.is_valid():
            user_form.save()
            perfil_form.save()
            experiencia_formset.save()
            educacion_formset.save()
            messages.success(request, 'Perfil actualizado exitosamente')
            return redirect('ver_perfil')
        else:
            print(user_form.errors)
            print(perfil_form.errors)
            print(experiencia_formset.errors)
            print(educacion_formset.errors)
    else:
        user_form = UserForm(instance=request.user)
        perfil_form = PerfilForm(instance=perfil)
        experiencia_formset = ExperienciaLaboralFormSet(instance=perfil)
        educacion_formset = EducacionFormSet(instance=perfil)

    return render(request, 'myapp/editar_perfil.html', {
        'user_form': user_form,
        'perfil_form': perfil_form,
        'experiencia_formset': experiencia_formset,
        'educacion_formset': educacion_formset,
        'experiencias': perfil.experiencias.all(),
        'educaciones': perfil.educaciones.all(),
    })

@login_required
def editar_experiencia(request, pk):
    experiencia = get_object_or_404(ExperienciaLaboral, pk=pk)
    if request.method == 'POST':
        form = ExperienciaLaboralForm(request.POST, instance=experiencia)
        if form.is_valid():
            form.save()
            messages.success(request, 'Experiencia actualizada exitosamente.')
            return redirect('editar_perfil')
    else:
        form = ExperienciaLaboralForm(instance=experiencia)
    return render(request, 'myapp/editar_experiencia.html', {'form': form})

@login_required
def eliminar_experiencia(request, pk):
    experiencia = get_object_or_404(ExperienciaLaboral, pk=pk)
    if request.method == 'POST':
        experiencia.delete()
        messages.success(request, 'Experiencia eliminada exitosamente.')
        return redirect('editar_perfil')
    return render(request, 'myapp/eliminar_experiencia.html', {'experiencia': experiencia})

@login_required
def editar_educacion(request, pk):
    educacion = get_object_or_404(Educacion, pk=pk)
    if request.method == 'POST':
        form = EducacionForm(request.POST, instance=educacion)
        if form.is_valid():
            form.save()
            messages.success(request, 'Educación actualizada exitosamente.')
            return redirect('editar_perfil')
    else:
        form = EducacionForm(instance=educacion)
    return render(request, 'myapp/editar_educacion.html', {'form': form})

@login_required
def eliminar_educacion(request, pk):
    educacion = get_object_or_404(Educacion, pk=pk)
    if request.method == 'POST':
        educacion.delete()
        messages.success(request, 'Educación eliminada exitosamente.')
        return redirect('editar_perfil')
    return render(request, 'myapp/eliminar_educacion.html', {'educacion': educacion})

@login_required


@login_required
def ver_perfil(request):
    perfil = request.user.perfil
    experiencias = perfil.experiencias.all().order_by('-fecha_inicio')
    educaciones = perfil.educaciones.all().order_by('-fecha_inicio')

    return render(request, 'myapp/ver_perfil.html', {
        'perfil': perfil,
        'experiencias': experiencias,
        'educaciones': educaciones,
    })

@login_required
def cambiar_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Su contraseña ha sido cambiada exitosamente.')
            return redirect('ver_perfil')
        else:
            messages.error(request, 'Por favor corrija los errores a continuación.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'myapp/cambiar_password.html', {'form': form})

# Funciones de Notificaciones
@login_required
def notificaciones_ajax(request):
    notificaciones = request.user.notificacion_set.all().order_by('-fecha_creacion')[:5]  # Obtener las últimas 5 notificaciones
    notificaciones_no_leidas = request.user.notificacion_set.filter(leido=False).count()
    
    html = render_to_string('myapp/notificaciones_dropdown.html', {'notificaciones': notificaciones})
    
    return JsonResponse({
        'html': html,
        'count': notificaciones_no_leidas,
    })



@login_required
def listar_notificaciones(request):
    notificaciones_no_leidas = request.user.notificacion_set.filter(leido=False).count()
    notificaciones = request.user.notificacion_set.all().order_by('-fecha_creacion')
    return render(request, 'myapp/listar_notificaciones.html', {
        'notificaciones': notificaciones,
        'notificaciones_no_leidas': notificaciones_no_leidas,
    })

@login_required
def marcar_notificacion_leida(request, notificacion_id):
    notificacion = get_object_or_404(Notificacion, id=notificacion_id, receptor=request.user)
    notificacion.leido = True
    notificacion.save()
    messages.success(request, 'Notificación marcada como leída.')
    return redirect('listar_notificaciones')

@login_required
def proyecto_lista(request):
    query = request.GET.get('q', '')
    if query:
        proyectos = Proyecto.objects.filter(
            Q(nombre__icontains=query) | Q(descripcion__icontains=query)
        )
    else:
        proyectos = Proyecto.objects.all()
    return render(request, 'myapp/proyecto_lista.html', {'proyectos': proyectos})

@login_required
def crear_proyecto(request):
    if request.method == 'POST':
        form = ProyectoForm(request.POST, request.FILES)
        if form.is_valid():
            proyecto = form.save(commit=False)
            proyecto.creador = request.user
            proyecto.save()
            messages.success(request, 'Proyecto creado exitosamente.')
            return redirect('proyecto_detalle', proyecto_id=proyecto.id)
        else:
            messages.error(request, 'Error al crear el proyecto.')
    else:
        form = ProyectoForm()
    return render(request, 'myapp/crear_proyecto.html', {'form': form})

@login_required
def proyecto_edit(request, pk):
    proyecto = get_object_or_404(Proyecto, pk=pk)
    if request.method == 'POST':
        form = ProyectoForm(request.POST, request.FILES, instance=proyecto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Proyecto editado exitosamente.')
            return redirect('proyecto_detalle', proyecto_id=proyecto.id)
        else:
            messages.error(request, 'Error al editar el proyecto.')
    else:
        form = ProyectoForm(instance=proyecto)
    return render(request, 'myapp/editar_proyecto.html', {'form': form})

@login_required
def proyecto_detalle(request, proyecto_id):
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
            return redirect('proyecto_detalle', proyecto_id=proyecto.id)
        else:
            messages.error(request, 'Error al agregar el comentario.')
    else:
        form = ComentarioForm()
    postulaciones = proyecto.postulacion_set.all()
    return render(request, 'myapp/proyecto_detalle.html', {
        'proyecto': proyecto, 
        'comentarios': comentarios, 
        'form': form,
        'postulaciones': postulaciones,
    })


@permission_required('myapp.delete_proyecto', raise_exception=True)
@login_required
def proyecto_delete(request, pk):
    proyecto = get_object_or_404(Proyecto, pk=pk)
    if request.method == 'POST':
        proyecto.delete()
        messages.success(request, 'Proyecto eliminado exitosamente.')
        return redirect('proyecto_lista')
    return render(request, 'myapp/confirmar_eliminar_proyecto.html', {'proyecto': proyecto})

@login_required
@permission_required('myapp.delete_proyecto', raise_exception=True)
def confirmar_eliminar_proyecto(request, pk):
    proyecto = get_object_or_404(Proyecto, pk=pk)
    if request.method == 'POST':
        proyecto.delete()
        messages.success(request, 'Proyecto eliminado exitosamente.')
        return redirect('proyecto_lista')
    return render(request, 'myapp/confirmar_eliminar_proyecto.html', {'proyecto': proyecto})

@login_required
def postular_proyecto(request, proyecto_id):
    proyecto = get_object_or_404(Proyecto, id=proyecto_id)
    if request.method == 'POST':
        postulacion, created = Postulacion.objects.get_or_create(proyecto=proyecto, usuario=request.user)
        if not created:
            messages.error(request, 'Ya te has postulado a este proyecto.')
        else:
            Notificacion.objects.create(
                receptor=proyecto.creador,
                mensaje=f'El usuario {request.user.username} se ha postulado a tu proyecto "{proyecto.nombre}".'
            )
            messages.success(request, 'Te has postulado al proyecto exitosamente.')
        return redirect('proyecto_detalle', proyecto_id=proyecto_id)
    return render(request, 'myapp/proyecto_detalle.html', {'proyecto': proyecto})

@login_required
@permission_required('myapp.change_postulacion', raise_exception=True)
def aceptar_postulacion(request, postulacion_id):
    postulacion = get_object_or_404(Postulacion, id=postulacion_id)
    if request.method == 'POST':
        postulacion.estado = 'aceptada'
        postulacion.save()
        messages.success(request, 'La postulación ha sido aceptada.')
        Notificacion.objects.create(
            receptor=postulacion.usuario,
            mensaje=f'Tu postulación al proyecto "{postulacion.proyecto.nombre}" ha sido aceptada.'
        )
    return redirect('proyecto_detalle', proyecto_id=postulacion.proyecto.id)

@login_required
@permission_required('myapp.change_postulacion', raise_exception=True)
def rechazar_postulacion(request, postulacion_id):
    postulacion = get_object_or_404(Postulacion, id=postulacion_id)
    if request.method == 'POST':
        postulacion.estado = 'rechazada'
        postulacion.save()
        messages.success(request, 'La postulación ha sido rechazada.')
        Notificacion.objects.create(
            receptor=postulacion.usuario,
            mensaje=f'Tu postulación al proyecto "{postulacion.proyecto.nombre}" ha sido rechazada.'
        )
    return redirect('proyecto_detalle', proyecto_id=postulacion.proyecto.id)

@login_required
def mis_postulaciones(request):
    postulaciones = Postulacion.objects.filter(usuario=request.user)
    return render(request, 'myapp/mis_postulaciones.html', {'postulaciones': postulaciones})

# Functions related to Resources
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

# Functions related to Messages
@login_required
def listar_mensajes(request):
    query = request.GET.get('q')
    if query:
        mensajes_recibidos = Mensaje.objects.filter(receptor=request.user, contenido__icontains=query).order_by('-fecha_envio')
        mensajes_enviados = Mensaje.objects.filter(emisor=request.user, contenido__icontains=query).order_by('-fecha_envio')
    else:
        mensajes_recibidos = Mensaje.objects.filter(receptor=request.user).order_by('-fecha_envio')
        mensajes_enviados = Mensaje.objects.filter(emisor=request.user).order_by('-fecha_envio')
    
    mensajes_recibidos.update(leido=True)

    return render(request, 'myapp/listar_mensajes.html', {
        'mensajes_recibidos': mensajes_recibidos,
        'mensajes_enviados': mensajes_enviados,
        'users': User.objects.exclude(id=request.user.id),
        'query': query
    })

@login_required
def enviar_mensaje(request):
    if request.method == 'POST':
        form = MensajeForm(request.POST)
        if form.is_valid():
            mensaje = form.save(commit=False)
            mensaje.emisor = request.user  # Asigna el emisor aquí
            mensaje.save()

            # Crear notificación para el receptor
            Notificacion.objects.create(
                receptor=mensaje.receptor,
                mensaje=f"Tienes un nuevo mensaje de {request.user.username}",
                url=f"/mensajes/{mensaje.id}/"
            )

            messages.success(request, 'Mensaje enviado exitosamente.')
            return redirect('listar_mensajes')
        else:
            messages.error(request, 'Error al enviar el mensaje.')
    else:
        form = MensajeForm()
    
    return render(request, 'myapp/enviar_mensaje.html', {'form': form})

@login_required
def eliminar_mensaje(request, mensaje_id):
    mensaje = get_object_or_404(Mensaje, id=mensaje_id)
    if request.method == 'POST':
        mensaje.delete()
        messages.success(request, 'Mensaje eliminado exitosamente.')
        return redirect('listar_mensajes')
    return render(request, 'myapp/confirm_delete_mensaje.html', {'mensaje': mensaje})

@login_required
def detalle_mensaje(request, mensaje_id):
    mensaje = get_object_or_404(Mensaje, id=mensaje_id)

    # Marcar la notificación como leída
    notificacion = Notificacion.objects.filter(receptor=request.user, url=f"/mensajes/{mensaje_id}/").first()
    if notificacion:
        notificacion.leido = True
        notificacion.save()

    return render(request, 'myapp/detalle_mensaje.html', {'mensaje': mensaje})

# Functions related to Activities
@login_required
def historial_actividades(request):
    actividades = Actividad.objects.filter(usuario=request.user).order_by('-fecha')
    return render(request, 'myapp/historial_actividades.html', {'actividades': actividades})

# User Authentication Functions
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
            Perfil.objects.get_or_create(user=user)
            login(request, user)
            return redirect('editar_perfil')
    else:
        form = UserCreationForm()
    return render(request, 'myapp/register.html', {'form': form})

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')
    return render(request, 'myapp/logout.html')

@login_required
def index(request):
    nuevos_mensajes = Mensaje.objects.filter(receptor=request.user, leido=False).count()
    return render(request, 'myapp/index.html', {'nuevos_mensajes': nuevos_mensajes})

# Signal to save user profile upon user creation
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'perfil'):
        instance.perfil.save()


#ADMIN DASHBOARD

@login_required
@user_passes_test(lambda u: u.is_staff)
def admin_dashboard(request):
    query = request.GET.get('q', '')
    filtro = request.GET.get('filtro', 'todos')
    
    proyectos = Proyecto.objects.all()
    tareas = Tarea.objects.all()

    if query:
        proyectos = proyectos.filter(
            Q(nombre__icontains=query) | Q(descripcion__icontains=query)
        )
        tareas = tareas.filter(
            Q(nombre__icontains=query) | Q(descripcion__icontains=query)
        )

    if filtro == 'activos':
        proyectos = proyectos.filter(fecha_fin__gt=timezone.now())
    elif filtro == 'completados':
        proyectos = proyectos.filter(fecha_fin__lte=timezone.now())

    context = {
        'proyectos': proyectos,
        'tareas': tareas,
        'proyectos_activos': proyectos.filter(fecha_fin__gt=timezone.now()).count(),
        'proyectos_completados': proyectos.filter(fecha_fin__lte=timezone.now()).count(),
        'tareas_pendientes': tareas.filter(completada=False).count(),
        'tareas_completadas': tareas.filter(completada=True).count(),
        'query': query,
        'filtro': filtro,
    }
    return render(request, 'myapp/admin_dashboard.html', context)