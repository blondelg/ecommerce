# Generated by Django 2.2.13 on 2020-08-05 16:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('settings', '0002_marketplacesettings_product_tags'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='marketplacesettings',
            name='test',
        ),
    ]
