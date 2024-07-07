from django.db import models
from django.contrib.auth.models import User


def get_default_user():
    return User.objects.first().id if User.objects.exists() else None

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Proyecto(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    ciudad = models.CharField(max_length=100, blank=True, null=True)
    imagen = models.ImageField(upload_to='proyectos/', blank=True, null=True)
    categoria = models.CharField(max_length=100, blank=True, null=True)
    creador = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre
class Tarea(models.Model):
    proyecto = models.ForeignKey(Proyecto, related_name='tareas', on_delete=models.CASCADE)
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, null=True)
    completada = models.BooleanField(default=False)
    fecha_limite = models.DateField(blank=True, null=True)
    asignada_a = models.ForeignKey(User, related_name='tareas_asignadas', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.nombre
    
class Subtarea(models.Model):
    tarea = models.ForeignKey(Tarea, on_delete=models.CASCADE, related_name='subtareas')
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    fecha_limite = models.DateTimeField()
    completada = models.BooleanField(default=False)
    
    def __str__(self):
        return self.nombre
    
# Definición del modelo SeguimientoTarea
class SeguimientoTarea(models.Model):
    tarea = models.ForeignKey(Tarea, on_delete=models.CASCADE, related_name='seguimientos')
    comentario = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

class ComentarioTarea(models.Model):
    tarea = models.ForeignKey(Tarea, on_delete=models.CASCADE, related_name='comentarios')
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    texto = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.texto[:20]

class Actividad(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    accion = models.CharField(max_length=255)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.username} - {self.accion}"

class Comentario(models.Model):
    proyecto = models.ForeignKey(Proyecto, related_name='comentarios', on_delete=models.CASCADE)
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    texto = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.texto

class Postulacion(models.Model):
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_postulacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.usuario.username} en {self.proyecto.nombre}'

class Notificacion(models.Model):
    receptor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notificaciones')
    mensaje = models.CharField(max_length=255)
    url = models.CharField(max_length=200, default='/')
    leido = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Notificación para {self.receptor.username} - {self.mensaje}'

class Mensaje(models.Model):
    emisor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mensajes_enviados')
    receptor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mensajes_recibidos')
    contenido = models.TextField()
    leido = models.BooleanField(default=False)
    fecha_envio = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Mensaje de {self.emisor.username} a {self.receptor.username}'

class Recurso(models.Model):
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField()
    archivo = models.FileField(upload_to='recursos/')
    fecha_subida = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo

class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    birth_date = models.DateField(null=True, blank=True)
    descripcion = models.TextField(blank=True, null=True, default='')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    website = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    facebook = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    nombre = models.CharField(max_length=30, blank=True, null=True, default='')
    apellido = models.CharField(max_length=30, blank=True, null=True, default='')

    def __str__(self):
        return self.user.username

class ExperienciaLaboral(models.Model):
    perfil = models.ForeignKey(Perfil, related_name='experiencias', on_delete=models.CASCADE)
    titulo = models.CharField(max_length=200)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)

class Educacion(models.Model):
    perfil = models.ForeignKey(Perfil, related_name='educaciones', on_delete=models.CASCADE)
    institucion = models.CharField(max_length=200)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.institucion
    
