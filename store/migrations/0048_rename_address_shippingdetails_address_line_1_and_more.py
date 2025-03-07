# Generated by Django 5.1.3 on 2025-01-09 15:41

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0047_orderhistory'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shippingdetails',
            old_name='address',
            new_name='address_line_1',
        ),
        migrations.RenameField(
            model_name='shippingdetails',
            old_name='fullname',
            new_name='recipient_name',
        ),
        migrations.RemoveField(
            model_name='shippingdetails',
            name='cart',
        ),
        migrations.AddField(
            model_name='shippingdetails',
            name='address_line_2',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='shippingdetails',
            name='country',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='shippingdetails',
            name='phone_number',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='shippingdetails',
            name='postal_code',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='orderhistory',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Shipped', 'Shipped'), ('Delivered', 'Delivered')], default='Pending', max_length=50),
        ),
        migrations.AlterField(
            model_name='shippingdetails',
            name='city',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='shippingdetails',
            name='email',
            field=models.EmailField(max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='shippingdetails',
            name='state',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='shippingdetails',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
