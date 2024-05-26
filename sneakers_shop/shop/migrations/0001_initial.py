# Generated by Django 5.0.6 on 2024-05-26 20:33

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('size', models.CharField(max_length=20)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('available_count', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Manager',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('delivery_date', models.DateTimeField()),
                ('delivery_status', models.CharField(choices=[('PACK', 'packing'), ('OTW', 'on the way'), ('DELD', 'delivered'), ('CANC', 'canceled')], max_length=4)),
                ('client_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='shop.client')),
                ('manager_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='shop.manager')),
            ],
        ),
        migrations.CreateModel(
            name='ProductInOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_count', models.IntegerField()),
                ('order_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='shop.order')),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='shop.product')),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='products',
            field=models.ManyToManyField(through='shop.ProductInOrder', to='shop.product'),
        ),
        migrations.CreateModel(
            name='Return',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason', models.TextField()),
                ('date', models.DateTimeField()),
                ('status', models.CharField(choices=[('ACCEPT', 'accepted'), ('DECLINE', 'declined')], max_length=7)),
                ('client_id', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, to='shop.client')),
                ('manager_id', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, to='shop.manager')),
                ('order_id', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, to='shop.order')),
                ('product_id', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, to='shop.product')),
            ],
        ),
    ]
