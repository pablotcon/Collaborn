from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Tarea, Comentario, Notificacion, Actividad, Mensaje, Proyecto
from django.apps import AppConfig
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Postulacion, Proyecto

import logging
logger = logging.getLogger(__name__)

@receiver(post_save, sender=Mensaje)
def notificar_mensaje(sender, instance, created, **kwargs):
    if created:
        receptor = instance.receptor
        logger.debug(f'Creando notificación para mensaje de {instance.emisor.username} a {receptor.username}')
        # Verificar si la notificación ya existe
        if not Notificacion.objects.filter(
            receptor=receptor,
            mensaje=f'Tienes un nuevo mensaje de {instance.emisor.username}',
            url=f'/mensajes/{instance.id}/' if instance.id else None):
        
            logger.debug(f'Notificación creada para mensaje de {instance.emisor.username} a {receptor.username}')

@receiver(post_save, sender=Comentario)
def notificar_comentario_proyecto(sender, instance, created, **kwargs):
    if created:
        proyecto = instance.proyecto
        usuario = proyecto.creador
        Notificacion.objects.create(
            receptor=usuario,
            mensaje=f'Nuevo comentario en el proyecto "{proyecto.nombre}"',
            url=f'/proyectos/{proyecto.id}/'
        )
        logger.debug(f'Notificación creada para comentario en proyecto: {proyecto.nombre}')

@receiver(post_save, sender=Tarea)
def notificar_asignacion_tarea(sender, instance, created, **kwargs):
    if created and instance.asignada_a:
        Notificacion.objects.create(
            receptor=instance.asignada_a,
            mensaje=f"Se te ha asignado una nueva tarea: {instance.nombre}",
            url=f"/tareas/{instance.id}/"
        )

@receiver(post_save, sender=Tarea)
def registrar_actividad_tarea(sender, instance, created, **kwargs):
    if created:
        accion = f"Creó la tarea: {instance.nombre}"
    else:
        accion = f"Actualizó la tarea: {instance.nombre}"
    Actividad.objects.create(usuario=instance.asignada_a, accion=accion)

@receiver(post_save, sender=Postulacion)
def actualizar_historial_colaboradores(sender, instance, **kwargs):
    if instance.estado == 'aceptada':
        proyecto = instance.proyecto
        usuario = instance.usuario
        proyecto.colaboradores.add(usuario)
        proyecto.save()