from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('proyectos/', views.proyecto_list, name='proyecto_list'),
    path('crear_proyecto/', views.crear_proyecto, name='crear_proyecto'),
    path('proyectos/<int:proyecto_id>/', views.proyecto_detail, name='proyecto_detail'),
    path('proyectos/<int:proyecto_id>/post ular/', views.postular_proyecto, name='postular_proyecto'),    path('proyectos/<int:pk>/edit/', views.proyecto_edit, name='proyecto_edit'),
    path('proyectos/<int:pk>/delete/', views.proyecto_delete, name='proyecto_delete'),

    path('mis-postulaciones/', views.mis_postulaciones, name='mis_postulaciones'),

    path('perfil/', views.ver_perfil, name='ver_perfil'),
    path('perfil/editar/', views.editar_perfil, name='editar_perfil'),
    path('perfil/cambiar_password/', views.cambiar_password, name='cambiar_password'),
    path('perfil/historial_actividades/', views.historial_actividades, name='historial_actividades'),

    path('notificaciones/', views.listar_notificaciones, name='listar_notificaciones'),
    path('notificaciones/<int:notificacion_id>/marcar_leida/', views.marcar_notificacion_leida, name='marcar_notificacion_leida'),

    path('mensajes/', views.listar_mensajes, name='listar_mensajes'),
    path('mensajes/enviar/', views.enviar_mensaje, name='enviar_mensaje'),
    path('mensajes/enviar/<int:receptor_id>/', views.enviar_mensaje_receptor, name='enviar_mensaje_receptor'),
    path('mensajes/eliminar/<int:mensaje_id>/', views.eliminar_mensaje, name='eliminar_mensaje'),

    path('recursos/', views.listar_recursos, name='listar_recursos'),
    path('recursos/subir/', views.subir_recurso, name='subir_recurso'),
    path('recursos/<int:pk>/', views.recurso_detail, name='recurso_detail'),
    path('recursos/<int:pk>/edit/', views.recurso_edit, name='recurso_edit'),
    path('recursos/<int:pk>/delete/', views.recurso_delete, name='recurso_delete'),

    path('panel/tareas/', views.admin_panel_tareas, name='admin_panel_tareas'),
    path('tareas/<int:tarea_id>/detalle/', views.detalle_tarea, name='detalle_tarea'),
    path('proyectos/<int:proyecto_id>/tareas/', views.listar_tareas, name='listar_tareas'),
    path('proyectos/<int:proyecto_id>/tareas/agregar/', views.agregar_tarea, name='agregar_tarea'),
    path('tareas/<int:tarea_id>/editar/', views.editar_tarea, name='editar_tarea'),
    path('tareas/<int:tarea_id>/eliminar/', views.eliminar_tarea, name='eliminar_tarea'),
    path('tareas/<int:tarea_id>/confirmar_eliminar/', views.confirmar_eliminar_tarea, name='confirmar_eliminar_tarea'),
    path('historial_actividades/', views.historial_actividades, name='historial_actividades'),
]
