# Generated by Django 2.2.13 on 2020-08-17 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('settings', '0016_auto_20200817_1237'),
    ]

    operations = [
        migrations.AlterField(
            model_name='marketplacesettings',
            name='favicon',
            field=models.FileField(blank=True, help_text='Favicon', null=True, upload_to='', verbose_name='wagtailimages.Image'),
        ),
    ]