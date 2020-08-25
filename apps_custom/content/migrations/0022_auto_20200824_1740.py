# Generated by Django 2.2.13 on 2020-08-24 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0021_contentprojet_achievement_percent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contentprojet',
            name='achievement_percent',
            field=models.DecimalField(decimal_places=3, default=0, max_digits=4),
        ),
    ]
