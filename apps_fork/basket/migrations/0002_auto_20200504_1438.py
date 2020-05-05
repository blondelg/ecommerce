# Generated by Django 2.2.12 on 2020-05-04 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('voucher', '0001_initial'),
        ('basket', '0001_initial'),
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