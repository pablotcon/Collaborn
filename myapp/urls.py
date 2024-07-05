from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('proyectos/', views.proyecto_list, name='proyecto_list'),
    path('proyectos/create/', views.proyecto_create, name='proyecto_create'),
    path('proyectos/<int:proyecto_id>/', views.proyecto_detail, name='proyecto_detail'),
    path('proyectos/<int:proyecto_id>/postular/', views.postular_proyecto, name='postular_proyecto'),
    path('proyectos/<int:pk>/edit/', views.proyecto_detail, name='proyecto_edit'),
    path('proyectos/<int:pk>/delete/', views.proyecto_detail, name='proyecto_delete'),
    path('mis-postulaciones/', views.mis_postulaciones, name='mis_postulaciones'),
    path('perfil/', views.ver_perfil, name='ver_perfil'),
    path('perfil/editar/', views.editar_perfil, name='editar_perfil'),
    path('notificaciones/', views.listar_notificaciones, name='listar_notificaciones'),
    path('notificaciones/marcar-leida/<int:notificacion_id>/', views.marcar_notificacion_leida, name='marcar_notificacion_leida'),
    path('mensajes/enviar/', views.enviar_mensaje, name='enviar_mensaje'),
    path('mensajes/', views.listar_mensajes, name='listar_mensajes'),
    path('recursos/', views.listar_recursos, name='listar_recursos'),
    path('recursos/subir/', views.subir_recurso, name='subir_recurso'),
    path('recursos/<int:pk>/', views.recurso_detail, name='recurso_detail'),
    path('recursos/<int:pk>/edit/', views.recurso_detail, name='recurso_edit'),
    path('recursos/<int:pk>/delete/', views.recurso_detail, name='recurso_delete'),
    path('notificaciones/marcar-leida/<int:notificacion_id>/', views.marcar_notificacion_leida, name='marcar_notificacion_leida'),
    path('proyectos/<int:proyecto_id>/tareas/', views.listar_tareas, name='listar_tareas'),
    path('proyectos/<int:proyecto_id>/tareas/crear/', views.crear_tarea, name='crear_tarea'),
]

