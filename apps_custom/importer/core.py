from oscar.apps.catalogue.models import *
from oscar.apps.partner.models import *
from django.contrib.auth import authenticate
from django import forms
import csv
import os


class csv_uploader:

    """ define automated import interractions with the db """

    def __init__(self, file_path):

        self.path = file_path
        self.raw_dict = {}
        self.dialect = self.get_dialect()
        self.get_raw()

    def get_dialect(self):

        """ check file dialect """

        with open(self.path) as csvfile:
            return csv.Sniffer().sniff(csvfile.read())

    def get_raw(self):

        """ transform csv into a dict object """

        nb = 0
        with open(self.path) as csvfile:
            for line in csv.DictReader(csvfile, dialect=self.dialect):
                self.raw_dict[nb] = dict(line)
                nb += 1

    def delete_file(self):

        """ delete csv file at the end of the process """
        os.remove(self.path)

    def upload(self, upload_type):
        if upload_type.upper() == "CATALOGUE":
            self.upload_product()
        if upload_type.upper() == "STOCK":
            self.upload_stock()

    def upload_product(self):

        """ upload dict into product table """

        for dico in self.raw_dict.values():

            t_dict = dico
            t_dict.pop('structure', None)
            t_dict.pop('rating', None)
            t_dict.pop('date_created', None)
            t_dict.pop('date_updated', None)
            t_dict.pop('parent_id', None)

            t_dict['is_discountable'] = False
            t_dict['is_public'] = False
            t_dict['product_class_id'] = int(t_dict['product_class_id'])

            try:
                record = Product(**t_dict)
                record.save()

            except Exception as e:
                print(e)

        # remove file
        self.delete_file()

    def upload_stock(self):

        """ upload dict into stock table """

        for dico in self.raw_dict.values():

            t_dict = dico
            t_dict.pop('price_currency', None)
            t_dict.pop('cost_price', None)
            t_dict.pop('num_allocated', None)
            t_dict.pop('low_stock_threshold', None)
            t_dict.pop('date_created', None)
            t_dict.pop('date_updated', None)

            t_dict['product_id'] = int(t_dict['product_id'])
            t_dict['partner_id'] = int(t_dict['partner_id'])
            t_dict['num_in_stock'] = int(t_dict['num_in_stock'])

            try:
                record = StockRecord(**t_dict)
                record.save()

            except Exception as e:
                print(e)

        # remove file
        self.delete_file()
