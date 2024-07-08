from django.core.management.base import BaseCommand
from myapp.models import Proyecto, Tarea
from django.contrib.auth.models import User
from django.utils import timezone
import random

class Command(BaseCommand):
    help = 'Populate tasks for the project ACTIVA RECUPERACIÓN – EMERGENCIA INUNDACIONES 2024'

    def handle(self, *args, **kwargs):
        try:
            proyecto = Proyecto.objects.get(nombre="ACTIVA RECUPERACIÓN – EMERGENCIA INUNDACIONES 2024")
        except Proyecto.DoesNotExist:
            proyecto = Proyecto.objects.create(
                nombre="ACTIVA RECUPERACIÓN – EMERGENCIA INUNDACIONES 2024",
                descripcion="Asistir a contribuyentes que sean micro, pequeñas y medianas empresas en la recuperación de su actividad económica mediante el apoyo a través del cofinanciamiento de proyectos individuales.",
                fecha_inicio=timezone.now(),
                fecha_fin=timezone.now() + timezone.timedelta(days=365),
                ciudad="Santiago",
                categoria="Recuperación"
            )
        
        # Crear tareas ficticias
        nombres_tareas = [
            "Evaluación inicial de daños",
            "Contacto con proveedores",
            "Adquisición de materiales",
            "Reparación de equipos",
            "Reclutamiento de personal",
            "Construcción de nueva infraestructura",
            "Auditoría de seguridad",
            "Implementación de nuevas tecnologías",
            "Monitoreo de avances",
            "Informe final de recuperación"
        ]

        descripcion_tareas = [
            "Evaluar los daños iniciales causados por las inundaciones.",
            "Establecer contacto con proveedores para suministros necesarios.",
            "Adquirir materiales para la recuperación y reparación.",
            "Reparar equipos dañados durante las inundaciones.",
            "Reclutar personal adicional para las labores de recuperación.",
            "Construir nuevas infraestructuras donde sea necesario.",
            "Realizar una auditoría de seguridad post-recuperación.",
            "Implementar nuevas tecnologías para mejorar la productividad.",
            "Monitorear los avances de las tareas de recuperación.",
            "Preparar y presentar el informe final del proyecto de recuperación."
        ]

        users = User.objects.all()
        if not users:
            self.stdout.write(self.style.ERROR('No hay usuarios en la base de datos.'))
            return

        for i in range(len(nombres_tareas)):
            tarea = Tarea.objects.create(
                proyecto=proyecto,
                nombre=nombres_tareas[i],
                descripcion=descripcion_tareas[i],
                completada=False,
                fecha_limite=timezone.now() + timezone.timedelta(days=random.randint(30, 90)),
                asignada_a=random.choice(users)
            )
            self.stdout.write(self.style.SUCCESS(f'Tarea creada: {tarea.nombre}'))

        self.stdout.write(self.style.SUCCESS('Todas las tareas ficticias han sido creadas con éxito.'))
