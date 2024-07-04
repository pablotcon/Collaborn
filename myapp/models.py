from django.db import models
from django.contrib.auth.models import User

class Proyecto(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    creador = models.ForeignKey(User, on_delete=models.CASCADE)

class Postulacion(models.Model):
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_postulacion = models.DateTimeField(auto_now_add=True)
