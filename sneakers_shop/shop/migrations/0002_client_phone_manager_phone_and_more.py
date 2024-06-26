# Generated by Django 5.0.6 on 2024-05-27 10:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='phone',
            field=models.CharField(default='Введите телефон', max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='manager',
            name='phone',
            field=models.CharField(default='Введите телефон', max_length=20),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='order',
            name='delivery_status',
            field=models.CharField(choices=[('PACK', 'packing'), ('OTW', 'on the way'), ('DELD', 'delivered'), ('CANC', 'canceled')], default='PACK', max_length=4),
        ),
        migrations.AlterField(
            model_name='product',
            name='available_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='return',
            name='status',
            field=models.CharField(choices=[('PENDING', 'pending'), ('ACCEPT', 'accepted'), ('DECLINE', 'declined')], default='PENDING', max_length=7),
        ),
    ]
