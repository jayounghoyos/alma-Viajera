from django.test import TestCase
from decimal import Decimal
from apps.catalog.models import Item, Categoria, Calificacion
from apps.user.models import Usuario


class ItemModelTest(TestCase):
    """
    Pruebas unitarias para el modelo Item.
    Verifica el correcto funcionamiento del sistema de calificaciones.
    """

    def setUp(self):
        """Configuracion inicial para las pruebas"""
        # Crear categoria de prueba
        self.categoria = Categoria.objects.create(
            nombre='tour',
            descripcion='Categoria de tours turisticos'
        )

        # Crear usuario vendedor de prueba
        self.vendedor = Usuario.objects.create_user(
            username='vendedor_test',
            email='vendedor@test.com',
            password='testpass123',
            es_proveedor=True
        )

        # Crear item de prueba
        self.item = Item.objects.create(
            nombre='Tour Ciudad Historica',
            descripcion='Un tour por el centro historico',
            precio=Decimal('50000.00'),
            categoria=self.categoria,
            vendedor=self.vendedor,
            disponibilidad=True
        )

        # Crear usuarios para calificar
        self.usuario1 = Usuario.objects.create_user(
            username='usuario1',
            email='usuario1@test.com',
            password='pass123'
        )
        self.usuario2 = Usuario.objects.create_user(
            username='usuario2',
            email='usuario2@test.com',
            password='pass123'
        )
        self.usuario3 = Usuario.objects.create_user(
            username='usuario3',
            email='usuario3@test.com',
            password='pass123'
        )

    def test_promedio_calificacion_sin_calificaciones(self):
        """Test: Item sin calificaciones debe retornar 0"""
        promedio = self.item.promedio_calificacion()
        self.assertEqual(promedio, 0)

    def test_promedio_calificacion_con_una_calificacion(self):
        """Test: Item con una calificacion debe retornar ese valor"""
        Calificacion.objects.create(
            item=self.item,
            usuario=self.usuario1,
            puntuacion=5,
            comentario='Excelente tour'
        )
        promedio = self.item.promedio_calificacion()
        self.assertEqual(promedio, 5.0)

    def test_promedio_calificacion_con_multiples_calificaciones(self):
        """Test: Item con varias calificaciones debe calcular el promedio correcto"""
        Calificacion.objects.create(
            item=self.item,
            usuario=self.usuario1,
            puntuacion=5
        )
        Calificacion.objects.create(
            item=self.item,
            usuario=self.usuario2,
            puntuacion=4
        )
        Calificacion.objects.create(
            item=self.item,
            usuario=self.usuario3,
            puntuacion=3
        )
        # Promedio: (5 + 4 + 3) / 3 = 4.0
        promedio = self.item.promedio_calificacion()
        self.assertEqual(promedio, 4.0)

    def test_estrellas_sin_calificaciones(self):
        """Test: Item sin calificaciones debe mostrar 0 estrellas llenas"""
        estrellas = self.item.estrellas()
        self.assertEqual(estrellas['llenas'], 0)
        self.assertEqual(estrellas['media'], 0)
        self.assertEqual(estrellas['vacias'], 5)

    def test_estrellas_con_calificacion_completa(self):
        """Test: Calificacion de 5 debe mostrar 5 estrellas llenas"""
        Calificacion.objects.create(
            item=self.item,
            usuario=self.usuario1,
            puntuacion=5
        )
        estrellas = self.item.estrellas()
        self.assertEqual(estrellas['llenas'], 5)
        self.assertEqual(estrellas['media'], 0)
        self.assertEqual(estrellas['vacias'], 0)

    def test_estrellas_con_media_estrella(self):
        """Test: Promedio de 3.5 debe mostrar 3 llenas, 1 media, 1 vacia"""
        Calificacion.objects.create(
            item=self.item,
            usuario=self.usuario1,
            puntuacion=4
        )
        Calificacion.objects.create(
            item=self.item,
            usuario=self.usuario2,
            puntuacion=3
        )
        # Promedio: 3.5
        estrellas = self.item.estrellas()
        self.assertEqual(estrellas['llenas'], 3)
        self.assertEqual(estrellas['media'], 1)
        self.assertEqual(estrellas['vacias'], 1)
