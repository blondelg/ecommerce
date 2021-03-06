# Generated by Django 2.2.13 on 2020-08-04 08:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('voucher', '0001_initial'),
        ('basket', '0003_basket_project'),
    ]

    operations = [
        migrations.AddField(
            model_name='basket',
            name='vouchers',
            field=models.ManyToManyField(blank=True, to='voucher.Voucher', verbose_name='Vouchers'),
        ),
        migrations.AlterUniqueTogether(
            name='line',
            unique_together={('basket', 'line_reference')},
        ),
    ]
