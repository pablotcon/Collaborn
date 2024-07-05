from django.contrib import admin
from .models import Proyecto, Comentario, Mensaje, Notificacion, Recurso, Perfil, Tarea

@admin.register(Proyecto)
class ProyectoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'creador', 'fecha_inicio', 'fecha_fin')
    search_fields = ('nombre', 'descripcion')
    list_filter = ('fecha_inicio', 'fecha_fin', 'creador')

@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ('proyecto', 'usuario', 'fecha_creacion')
    search_fields = ('contenido',)
    list_filter = ('fecha_creacion', 'usuario')

@admin.register(Mensaje)
class MensajeAdmin(admin.ModelAdmin):
    list_display = ('emisor', 'receptor', 'fecha_envio')
    search_fields = ('contenido',)
    list_filter = ('fecha_envio', 'emisor', 'receptor')

@admin.register(Notificacion)
class NotificacionAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'mensaje', 'fecha_creacion', 'leida')
    search_fields = ('mensaje',)
    list_filter = ('fecha_creacion', 'leida', 'usuario')

@admin.register(Recurso)
class RecursoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'fecha_subida')
    search_fields = ('titulo',)
    list_filter = ('fecha_subida',)

@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ('user', 'location', 'birth_date')
    search_fields = ('user__username', 'user__email', 'location')

@admin.register(Tarea)
class TareaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'proyecto', 'asignado_a', 'fecha_vencimiento')
    search_fields = ('nombre', 'descripcion')
    list_filter = ('fecha_vencimiento', 'proyecto', 'asignado_a')
