from django.test import TestCase
from decimal import Decimal
from apps.cart.models import Carrito, CarritoItem
from apps.catalog.models import Item, Categoria
from apps.user.models import Usuario


class CarritoModelTest(TestCase):
    """
    Pruebas unitarias para el modelo Carrito.
    Verifica el correcto calculo del total del carrito.
    """

    def setUp(self):
        """Configuracion inicial para las pruebas"""
        # Crear categoria
        self.categoria = Categoria.objects.create(
            nombre='souvenir',
            descripcion='Souvenirs turisticos'
        )

        # Crear usuario vendedor
        self.vendedor = Usuario.objects.create_user(
            username='vendedor_cart',
            email='vendedor@cart.com',
            password='pass123',
            es_proveedor=True
        )

        # Crear usuario comprador
        self.usuario = Usuario.objects.create_user(
            username='comprador',
            email='comprador@test.com',
            password='pass123'
        )

        # Crear items de prueba con diferentes precios
        self.item1 = Item.objects.create(
            nombre='Llavero artesanal',
            descripcion='Llavero hecho a mano',
            precio=Decimal('5000.00'),
            categoria=self.categoria,
            vendedor=self.vendedor,
            stock=100
        )

        self.item2 = Item.objects.create(
            nombre='Camiseta tipica',
            descripcion='Camiseta con disenos tipicos',
            precio=Decimal('35000.00'),
            categoria=self.categoria,
            vendedor=self.vendedor,
            stock=50
        )

        self.item3 = Item.objects.create(
            nombre='Taza ceramica',
            descripcion='Taza de ceramica pintada',
            precio=Decimal('15000.00'),
            categoria=self.categoria,
            vendedor=self.vendedor,
            stock=30
        )

        # Crear carrito
        self.carrito = Carrito.objects.create(
            usuario=self.usuario
        )

    def test_carrito_vacio_total_cero(self):
        """Test: Carrito vacio debe tener total 0"""
        total = self.carrito.calcular_total()
        self.assertEqual(total, Decimal('0.00'))

    def test_carrito_un_item_cantidad_uno(self):
        """Test: Un item con cantidad 1 debe calcular el total correctamente"""
        CarritoItem.objects.create(
            carrito=self.carrito,
            item=self.item1,
            cantidad=1
        )
        total = self.carrito.calcular_total()
        self.assertEqual(total, Decimal('5000.00'))

    def test_carrito_un_item_cantidad_multiple(self):
        """Test: Un item con cantidad mayor a 1 debe multiplicar correctamente"""
        CarritoItem.objects.create(
            carrito=self.carrito,
            item=self.item2,
            cantidad=3
        )
        # 35000 * 3 = 105000
        total = self.carrito.calcular_total()
        self.assertEqual(total, Decimal('105000.00'))

    def test_carrito_multiples_items(self):
        """Test: Multiple items deben sumar correctamente"""
        CarritoItem.objects.create(
            carrito=self.carrito,
            item=self.item1,
            cantidad=2
        )
        CarritoItem.objects.create(
            carrito=self.carrito,
            item=self.item2,
            cantidad=1
        )
        CarritoItem.objects.create(
            carrito=self.carrito,
            item=self.item3,
            cantidad=3
        )
        # (5000 * 2) + (35000 * 1) + (15000 * 3) = 10000 + 35000 + 45000 = 90000
        total = self.carrito.calcular_total()
        self.assertEqual(total, Decimal('90000.00'))

    def test_subtotal_carritoitem(self):
        """Test: La propiedad subtotal de CarritoItem debe calcular correctamente"""
        carrito_item = CarritoItem.objects.create(
            carrito=self.carrito,
            item=self.item2,
            cantidad=4
        )
        # 35000 * 4 = 140000
        self.assertEqual(carrito_item.subtotal, Decimal('140000.00'))

    def test_carrito_actualiza_total_en_bd(self):
        """Test: calcular_total() debe actualizar el campo total en la BD"""
        CarritoItem.objects.create(
            carrito=self.carrito,
            item=self.item1,
            cantidad=5
        )
        total_calculado = self.carrito.calcular_total()

        # Recargar el carrito desde la BD
        self.carrito.refresh_from_db()

        # El total en BD debe coincidir con el calculado
        self.assertEqual(self.carrito.total, total_calculado)
        self.assertEqual(self.carrito.total, Decimal('25000.00'))
