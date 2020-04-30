#-*- coding: utf-8 -*-
from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.views import generic
from oscar.core.loading import get_classes
from django.urls import reverse
from custom_apps.importer.core import csv_uploader
from oscar.apps.dashboard.catalogue.views import ProductListView as CoreProductListView
from custom_apps.importer.forms import UploadTypeSelectForm
import os

#(UploadTypeSelectForm, ) = get_classes('custom_apps.importer.forms', ('UploadTypeSelectForm',))
#(UploadTypeSelectForm, ) = get_classes('custom_apps.importer.forms', ('UploadTypeSelectForm',))


class ProductListView(CoreProductListView):

    uploadtype_form_class = UploadTypeSelectForm

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['uploadtype_form'] = self.uploadtype_form_class()
        return ctx


class ProductUploadCSVRedirectView(generic.RedirectView):
    permanent = False
    UploadType_form_class = UploadTypeSelectForm

    def get_redirect_url(self):
        if self.request.method == 'POST' and self.request.FILES['myfile']:
            csvFile = self.request.FILES['myfile']
            form = UploadTypeSelectForm(self.request.POST)
            if form.is_valid():
                upload_type = form.cleaned_data['type']

            # check file size
            if csvFile.size > settings.CSV_MAX_SIZE*1024000:

                # return an error message
                return reverse('dashboard:catalogue-product-list')

            fs = FileSystemStorage(location = settings.CSV_ROOT)
            filename = fs.save(csvFile.name, csvFile)
            uploaded_file_url = os.path.join(settings.CSV_ROOT, filename)

            uploader = csv_uploader(uploaded_file_url)
            uploader.upload(upload_type)

            # import csv


            return reverse('dashboard:catalogue-product-list')
        return reverse('dashboard:catalogue-product-list')
