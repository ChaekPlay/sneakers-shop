# Generated by Django 5.0.6 on 2024-05-29 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0009_order_delivery_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='return',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
