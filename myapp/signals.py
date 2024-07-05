from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Tarea, Comentario, Notificacion
from django.apps import AppConfig


class MyappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'myapp'

    def ready(self):
        import myapp.signals

@receiver(post_save, sender=Tarea)
def notificar_asignacion_tarea(sender, instance, created, **kwargs):
    if created and instance.asignada_a:
        mensaje = f'Has sido asignado a la tarea: {instance.nombre}'
        Notificacion.objects.create(
            usuario=instance.asignada_a,
            mensaje=mensaje
        )
        
@receiver(post_save, sender=Comentario)
def notificar_comentario_proyecto(sender, instance, **kwargs):
    proyecto = instance.proyecto
    for usuario in User.objects.filter(proyectos_creados=proyecto):
        Notificacion.objects.create(
            usuario=usuario,
            mensaje=f'Nuevo comentario en el proyecto "{proyecto.nombre}": {instance.texto}'
        )