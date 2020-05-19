from django.test import TestCase
from django.contrib.auth.models import User
from apps_fork.basket.models import Basket
from apps_fork.basket.models import Line
from apps_fork.catalogue.models import Product
from apps_fork.catalogue.models import ProductClass
from apps_fork.partner.models import Partner
from apps_fork.partner.models import StockRecord
from apps_fork.partner.strategy import Selector
from apps_fork.checkout.calculators import OrderTotalCalculator
from oscar.core import prices
from django.conf import settings
from decimal import Decimal as D
from decimal import *


class BasketTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Setup users
        cls.test_user = User.objects.create_user(username='Monsieur_test', password = 't3st')

        # Setup partners
        cls.partner1 = Partner.objects.create(id=1, name='partner1')
        cls.partner2 = Partner.objects.create(id=2, name='partner2')

        # Setup product class
        cls.product_class = ProductClass.objects.create(name='class 1')

        # Setup Products
        cls.product1 = Product.objects.create(upc='abcde', title='Produit 1', product_class=cls.product_class, partner=cls.partner1)
        cls.product2 = Product.objects.create(upc='fghij', title='Produit 2', product_class=cls.product_class, partner=cls.partner2)

        # Setup Stockrecords
        tax_rate = settings.OSCAR_DEFAULT_TAX_RATE
        cls.ttc_1 = 10
        cls.ttc_2 = 20
        cls.ht_1 = cls.ttc_1 / (1 + tax_rate)
        cls.ht_2 = cls.ttc_2 / (1 + tax_rate)
        cls.stockrecord_product1 = StockRecord.objects.create(product=cls.product1, partner=cls.partner1, price_excl_tax=cls.ht_1, price_retail=cls.ttc_1, num_in_stock=5)
        cls.stockrecord_product2 = StockRecord.objects.create(product=cls.product2, partner=cls.partner2, price_excl_tax=cls.ht_2, price_retail=cls.ttc_2, num_in_stock=10)

        # Setup Baskets multi partners and mono partners
        cls.basketMulti = Basket.objects.create(id=1, owner=cls.test_user)
        cls.basketMulti.strategy = Selector().strategy()
        cls.basketMono = Basket.objects.create(id=2, owner=cls.test_user)
        cls.basketMono.strategy = Selector().strategy()

        # Setup Basketlines
        cls.line1 = Line.objects.create(basket=cls.basketMulti, product=cls.product1, stockrecord=cls.stockrecord_product1, line_reference="ref1")
        cls.line2 = Line.objects.create(basket=cls.basketMulti, product=cls.product2, stockrecord=cls.stockrecord_product2, line_reference="ref2")
        cls.line3 = Line.objects.create(basket=cls.basketMono, product=cls.product1, stockrecord=cls.stockrecord_product1, line_reference="ref3")
        cls.line4 = Line.objects.create(basket=cls.basketMono, product=cls.product1, stockrecord=cls.stockrecord_product1, line_reference="ref4")


    def test_calculate_order_mono(self):
        print("TEST TOPIC : is order total calculator returns the right object for a mono basket")
        calculator = OrderTotalCalculator()
        price_object = prices.Price(
        currency=settings.OSCAR_DEFAULT_CURRENCY,
        excl_tax=D(2*self.ht_1).quantize(D('0.01'), rounding=ROUND_HALF_UP),
        incl_tax=D(2*self.ttc_1).quantize(D('0.01'), rounding=ROUND_HALF_UP))
        shipping_charge = prices.Price(currency=settings.OSCAR_DEFAULT_CURRENCY, excl_tax=0, incl_tax=0)
        self.assertEqual(calculator.calculate(self.basketMono, shipping_charge), price_object)

    def test_calculate_order_multi(self):
        print("TEST TOPIC : is order total calculator returns the right object for a multi basket")
        calculator = OrderTotalCalculator()
        price_object = {}
        shipping_charge = prices.Price(currency=settings.OSCAR_DEFAULT_CURRENCY, excl_tax=0, incl_tax=0)

        price_object[self.partner1] = prices.Price(
            currency=settings.OSCAR_DEFAULT_CURRENCY,
            excl_tax=D(self.ht_1).quantize(D('0.01'), rounding=ROUND_HALF_UP),
            incl_tax=D(self.ttc_1).quantize(D('0.01'), rounding=ROUND_HALF_UP))

        price_object[self.partner2] = prices.Price(
            currency=settings.OSCAR_DEFAULT_CURRENCY,
            excl_tax=D(self.ht_2).quantize(D('0.01'), rounding=ROUND_HALF_UP),
            incl_tax=D(self.ttc_2).quantize(D('0.01'), rounding=ROUND_HALF_UP))

        price_object['parent'] = prices.Price(
            currency=settings.OSCAR_DEFAULT_CURRENCY,
            excl_tax=D(self.ht_1 + self.ht_2).quantize(D('0.01'), rounding=ROUND_HALF_UP),
            incl_tax=D(self.ttc_1 + self.ttc_2).quantize(D('0.01'), rounding=ROUND_HALF_UP))

        self.assertEqual(calculator.calculate(self.basketMulti, shipping_charge), price_object)
