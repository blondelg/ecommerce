# Generated by Django 2.2.13 on 2020-08-22 15:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('settings', '0021_marketplacesettings_index_project'),
    ]

    operations = [
        migrations.AlterField(
            model_name='marketplacesettings',
            name='index_project',
            field=models.ForeignKey(blank=True, help_text="Lien vers l'index des projets", null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='content.ContentIndexProject'),
        ),
    ]
