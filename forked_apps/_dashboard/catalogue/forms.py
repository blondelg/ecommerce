#-*- coding: utf-8 -*-
from uploads.core.models import Document
from django import forms


class CsvForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('description', 'document', )
