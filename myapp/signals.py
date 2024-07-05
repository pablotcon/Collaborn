from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Tarea, Comentario, Notificacion

@receiver(post_save, sender=Tarea)
def notificar_asignacion_tarea(sender, instance, created, **kwargs):
    if created and instance.asignado_a:
        mensaje = f'Se te ha asignado una nueva tarea: {instance.nombre}'
        Notificacion.objects.create(usuario=instance.asignado_a, mensaje=mensaje)

@receiver(post_save, sender=Comentario)
def notificar_comentario_proyecto(sender, instance, created, **kwargs):
    if created:
        mensaje = f'Nuevo comentario en el proyecto {instance.proyecto.nombre}: {instance.texto}'
        for usuario in User.objects.filter(proyectos=instance.proyecto):
            Notificacion.objects.create(usuario=usuario, mensaje=mensaje)
