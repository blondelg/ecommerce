# Generated by Django 2.2.13 on 2020-08-04 08:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0003_taggeditem_add_unique_index'),
        ('content', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductTag',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('taggit.tag',),
        ),
    ]
