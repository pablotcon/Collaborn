from django.contrib import admin
from .models import Proyecto, Postulacion, Notificacion, Mensaje, Recurso, Perfil

admin.site.register(Proyecto)
admin.site.register(Perfil)
admin.site.register(Postulacion)
admin.site.register(Notificacion)
admin.site.register(Mensaje)
admin.site.register(Recurso)
