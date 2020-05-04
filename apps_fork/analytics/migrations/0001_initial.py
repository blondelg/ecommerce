# Generated by Django 2.2.12 on 2020-05-04 14:33

from decimal import Decimal
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('catalogue', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductView',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField(default='0', null=True, verbose_name='User id')),
                ('product_id', models.IntegerField(null=True, verbose_name='Product id')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Date Created')),
            ],
            options={
                'verbose_name': 'Product view',
                'verbose_name_plural': 'Product views',
            },
        ),
        migrations.CreateModel(
            name='UserSearch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('query', models.CharField(db_index=True, max_length=255, verbose_name='Search term')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Date Created')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'User search query',
                'verbose_name_plural': 'User search queries',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UserRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num_product_views', models.PositiveIntegerField(default=0, verbose_name='Product Views')),
                ('num_basket_additions', models.PositiveIntegerField(default=0, verbose_name='Basket Additions')),
                ('num_orders', models.PositiveIntegerField(db_index=True, default=0, verbose_name='Orders')),
                ('num_order_lines', models.PositiveIntegerField(db_index=True, default=0, verbose_name='Order Lines')),
                ('num_order_items', models.PositiveIntegerField(db_index=True, default=0, verbose_name='Order Items')),
                ('total_spent', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=12, verbose_name='Total Spent')),
                ('date_last_order', models.DateTimeField(blank=True, null=True, verbose_name='Last Order Date')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'User record',
                'verbose_name_plural': 'User records',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UserProductView',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Date Created')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalogue.Product', verbose_name='Product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'User product view',
                'verbose_name_plural': 'User product views',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ProductRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num_views', models.PositiveIntegerField(default=0, verbose_name='Views')),
                ('num_basket_additions', models.PositiveIntegerField(default=0, verbose_name='Basket Additions')),
                ('num_purchases', models.PositiveIntegerField(db_index=True, default=0, verbose_name='Purchases')),
                ('score', models.FloatField(default=0.0, verbose_name='Score')),
                ('product', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='stats', to='catalogue.Product', verbose_name='Product')),
            ],
            options={
                'verbose_name': 'Product record',
                'verbose_name_plural': 'Product records',
                'ordering': ['-num_purchases'],
                'abstract': False,
            },
        ),
    ]
