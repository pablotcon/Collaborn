from django.test import TestCase
from django.contrib.auth.models import User
from myapp.models import Proyecto, Comentario, Notificacion, Mensaje

class NotificacionTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='password')
        self.user2 = User.objects.create_user(username='user2', password='password')
        self.proyecto = Proyecto.objects.create(
            nombre='Proyecto de prueba',
            descripcion='Descripción del proyecto',
            fecha_inicio='2024-01-01',
            fecha_fin='2024-12-31',
            creador=self.user1
        )
        self.mensaje = Mensaje.objects.create(
            emisor=self.user1,
            receptor=self.user2,
            contenido='Mensaje de prueba'
        )

    def test_comentario_notificacion(self):
        comentario = Comentario.objects.create(
            proyecto=self.proyecto,
            autor=self.user2,
            texto='Comentario de prueba'
        )
        notificaciones = Notificacion.objects.filter(receptor=self.user1)
        self.assertEqual(notificaciones.count(), 1)

    def test_mensaje_notificacion(self):
        notificaciones = Notificacion.objects.filter(receptor=self.user2)
        self.assertEqual(notificaciones.count(), 1)
