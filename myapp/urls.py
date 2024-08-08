from django.urls import path
from . import views
from django.conf import settings 
from django.conf.urls.static import static

urlpatterns = [
    # Autenticación
    path('', views.index, name='index'),  # Página principal
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),

    # Perfil
    path('perfil/', views.ver_mi_perfil, name='ver_mi_perfil'),
    path('perfil/editar/', views.editar_perfil, name='editar_perfil'),
    path('perfil/cambiar_password/', views.cambiar_password, name='cambiar_password'),
    path('perfil/<int:user_id>/', views.ver_perfil, name='ver_perfil'),

    # Proyectos
    path('proyectos/', views.proyecto_lista, name='proyecto_lista'),
    path('proyectos/<int:proyecto_id>/', views.proyecto_detalle, name='proyecto_detalle'),
    path('proyectos/crear/', views.crear_proyecto, name='crear_proyecto'),
    path('proyectos/<int:pk>/editar/', views.proyecto_edit, name='proyecto_edit'),
    path('proyectos/<int:pk>/confirmar_eliminar/', views.confirmar_eliminar_proyecto, name='confirmar_eliminar_proyecto'),
    path('proyectos/<int:pk>/eliminar/', views.proyecto_delete, name='proyecto_delete'),

    # Postulaciones
    path('proyecto/<int:proyecto_id>/gestionar_postulaciones/', views.gestionar_postulaciones, name='gestionar_postulaciones'),
    path('proyectos/<int:proyecto_id>/postular/', views.postular_proyecto, name='postular_proyecto'),
    path('postulaciones/aceptar/<int:postulacion_id>/', views.aceptar_postulacion, name='aceptar_postulacion'),
    path('postulacion/aceptar/<int:postulacion_id>/', views.aceptar_postulacion, name='aceptar_postulacion'),
    path('postulacion/rechazar/<int:postulacion_id>/', views.rechazar_postulacion, name='rechazar_postulacion'),
    path('mis_postulaciones/', views.mis_postulaciones, name='mis_postulaciones'),

    # Experiencia y educación
    path('experiencia/<int:pk>/editar/', views.editar_experiencia, name='editar_experiencia'),
    path('experiencia/<int:pk>/eliminar/', views.eliminar_experiencia, name='eliminar_experiencia'),
    path('educacion/<int:pk>/editar/', views.editar_educacion, name='editar_educacion'),
    path('educacion/<int:pk>/eliminar/', views.eliminar_educacion, name='eliminar_educacion'),

    # Especialistas
    path('buscar_especialistas/', views.buscar_especialistas, name='buscar_especialistas'),
    path('especialistas/', views.listar_especialistas, name='listar_especialistas'),
    path('especialistas/<int:especialista_id>/valorar/', views.valorar_especialista, name='valorar_especialista'),
    path('proyectos/<int:proyecto_id>/recomendar/', views.recomendar_especialistas, name='recomendar_especialistas'),

    # Tareas
    path('tareas/<int:tarea_id>/actualizar_estado/', views.actualizar_estado_tarea, name='actualizar_estado_tarea'),
    path('tareas/agregar/<int:proyecto_id>/', views.agregar_tarea, name='agregar_tarea'),
    path('tareas/<int:tarea_id>/agregar_subtarea/', views.agregar_subtarea, name='agregar_subtarea'),
    path('tareas/<int:tarea_id>/', views.detalle_tarea, name='detalle_tarea'),
    path('tareas/editar/<int:tarea_id>/', views.editar_tarea, name='editar_tarea'),
    path('tareas/eliminar/<int:tarea_id>/', views.eliminar_tarea, name='eliminar_tarea'),
    path('tareas/confirmar_eliminar/<int:tarea_id>/', views.confirmar_eliminar_tarea, name='confirmar_eliminar_tarea'),
    path('tareas/listar/<int:proyecto_id>/', views.listar_tareas, name='listar_tareas'),
    path('tareas/seguir/<int:tarea_id>/', views.seguir_tarea, name='seguir_tarea'),
    path('tareas/dejar_seguir/<int:tarea_id>/', views.dejar_seguir_tarea, name='dejar_seguir_tarea'),
    path('tareas/seguimientos/', views.listar_seguimientos, name='listar_seguimientos'),
    path('tareas/seguimiento/agregar/<int:tarea_id>/', views.agregar_seguimiento, name='agregar_seguimiento'),

    # Notificaciones
    path('notificaciones/', views.listar_notificaciones, name='listar_notificaciones'),
     path('notificaciones/marcar_leida/<int:notificacion_id>/', views.marcar_notificacion_leida, name='marcar_notificacion_leida'),
    path('notificaciones/ajax/', views.notificaciones_ajax, name='notificaciones_ajax'),

    # Recursos
    path('recursos/', views.listar_recursos, name='listar_recursos'),
    path('recursos/subir/', views.subir_recurso, name='subir_recurso'),
    path('recursos/<int:pk>/', views.recurso_detail, name='recurso_detail'),
    path('recursos/<int:pk>/editar/', views.recurso_edit, name='recurso_edit'),
    path('recursos/<int:pk>/eliminar/', views.recurso_delete, name='recurso_delete'),

    # Mensajes
    path('mensajes/', views.listar_mensajes, name='listar_mensajes'),
    path('mensajes/enviar/', views.enviar_mensaje, name='enviar_mensaje'),
    path('mensajes/eliminar/<int:mensaje_id>/', views.eliminar_mensaje, name='eliminar_mensaje'),
    path('mensajes/iniciar_nuevo_chat/', views.iniciar_nuevo_chat, name='iniciar_nuevo_chat'),
    path('mensajes/ocultar_conversacion/', views.ocultar_conversacion, name='ocultar_conversacion'),
    path('mensajes/cargar_mensajes/', views.cargar_mensajes, name='cargar_mensajes'),
    path('mensajes/<int:user_id>/', views.ver_chat, name='ver_chat'),

    # Actividades
    path('actividades/historial/<int:user_id>/', views.historial_actividades, name='historial_actividades'),
    path('test/proyectos_colaborados/<int:user_id>/', views.test_proyectos_colaborados, name='test_proyectos_colaborados'),
    path('verificar_relaciones/', views.verificar_relaciones, name='verificar_relaciones'),
    
    # Admin Dashboard
    path('admin_panel/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin_panel_tareas/', views.admin_panel_tareas, name='admin_panel_tareas'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
