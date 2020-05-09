from django.test import TestCase
from django.contrib.auth.models import User
from apps_fork.catalogue.models import Product
from apps_fork.catalogue.models import ProductClass
from apps_fork.partner.models import Partner
from apps_fork.partner.models import StockRecord
from django.conf import settings



class ProductTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Setup users
        cls.test_user = User.objects.create_user(username='Monsieur_test', password = 't3st')

        # Setup partners
        cls.partner1 = Partner.objects.create(id=1, name='partner1')

        # Setup product class
        cls.product_class = ProductClass.objects.create(name='class 1')

        # Setup Products
        cls.product1 = Product.objects.create(upc='abcde', title='Produit 1', product_class=cls.product_class, partner=cls.partner1)

        # Setup Stockrecords
        tax_rate = settings.OSCAR_DEFAULT_TAX_RATE
        cls.ttc_1 = 10
        cls.ht_1 = cls.ttc_1 / (1 + tax_rate)
        cls.stockrecord_product1 = StockRecord.objects.create(product=cls.product1, partner=cls.partner1, price_excl_tax=cls.ht_1, price_retail=cls.ttc_1, num_in_stock=5)


    def test_stock_level(self):
        print("TEST TOPIC : is stock_level Prodctdecorator returns the actual stock level")
        self.assertEqual(self.product1.stock_level, 5)
