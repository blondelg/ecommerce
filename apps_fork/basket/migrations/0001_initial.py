<<<<<<< HEAD
# Generated by Django 2.2.12 on 2020-05-04 14:38
=======
# Generated by Django 2.2.12 on 2020-05-06 15:51
>>>>>>> 51c1f3c

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import oscar.core.utils
import oscar.models.fields.slugfield


class Migration(migrations.Migration):

    initial = True

    dependencies = [
<<<<<<< HEAD
        ('partner', '0001_initial'),
        ('catalogue', '0002_auto_20200504_1437'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
=======
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('partner', '0001_initial'),
        ('catalogue', '0002_auto_20200506_1550'),
>>>>>>> 51c1f3c
    ]

    operations = [
        migrations.CreateModel(
            name='Basket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('Open', 'Open - currently active'), ('Merged', 'Merged - superceded by another basket'), ('Saved', 'Saved - for items to be purchased later'), ('Frozen', 'Frozen - the basket cannot be modified'), ('Submitted', 'Submitted - has been ordered at the checkout')], default='Open', max_length=128, verbose_name='Status')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Date created')),
                ('date_merged', models.DateTimeField(blank=True, null=True, verbose_name='Date merged')),
                ('date_submitted', models.DateTimeField(blank=True, null=True, verbose_name='Date submitted')),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='baskets', to=settings.AUTH_USER_MODEL, verbose_name='Owner')),
            ],
            options={
                'verbose_name': 'Basket',
                'verbose_name_plural': 'Baskets',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Line',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('line_reference', oscar.models.fields.slugfield.SlugField(max_length=128, verbose_name='Line Reference')),
                ('quantity', models.PositiveIntegerField(default=1, verbose_name='Quantity')),
                ('price_currency', models.CharField(default=oscar.core.utils.get_default_currency, max_length=12, verbose_name='Currency')),
                ('price_excl_tax', models.DecimalField(decimal_places=2, max_digits=12, null=True, verbose_name='Price excl. Tax')),
                ('price_incl_tax', models.DecimalField(decimal_places=2, max_digits=12, null=True, verbose_name='Price incl. Tax')),
                ('date_created', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Date Created')),
                ('basket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lines', to='basket.Basket', verbose_name='Basket')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='basket_lines', to='catalogue.Product', verbose_name='Product')),
                ('stockrecord', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='basket_lines', to='partner.StockRecord')),
            ],
            options={
                'verbose_name': 'Basket line',
                'verbose_name_plural': 'Basket lines',
                'ordering': ['date_created', 'pk'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='LineAttribute',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=255, verbose_name='Value')),
                ('line', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attributes', to='basket.Line', verbose_name='Line')),
                ('option', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalogue.Option', verbose_name='Option')),
            ],
            options={
                'verbose_name': 'Line attribute',
                'verbose_name_plural': 'Line attributes',
                'abstract': False,
            },
        ),
    ]
