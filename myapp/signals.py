from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Tarea, Comentario, Notificacion, Actividad, Mensaje
from django.apps import AppConfig
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

class MyappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'myapp'

    def ready(self):
        import myapp.signals


@receiver(post_save, sender=Mensaje)
def enviar_notificacion_mensaje(sender, instance, created, **kwargs):
    if created:
        receptor = instance.receptor
        Notificacion.objects.create(
            receptor=receptor,
            mensaje=f"Tienes un nuevo mensaje de {instance.emisor.username}",
            url=f"/mensajes/{instance.id}/"
        )
        # Enviar notificación en tiempo real
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"user_{receptor.id}",
            {
                'type': 'send_notification',
                'notification': f"Tienes un nuevo mensaje de {instance.emisor.username}"
            }
        )

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
       
@receiver(post_save, sender=Comentario)
def notificar_comentario_proyecto(sender, instance, **kwargs):
    proyecto = instance.proyecto
    for usuario in User.objects.filter(proyectos_creados=proyecto):
        Notificacion.objects.create(
            usuario=usuario,
            mensaje=f'Nuevo comentario en el proyecto "{proyecto.nombre}": {instance.texto}'
        )