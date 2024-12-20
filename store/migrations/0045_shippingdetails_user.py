# Generated by Django 5.1.4 on 2024-12-20 21:38

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0044_shippingdetails'),
    ]

    operations = [
        migrations.AddField(
            model_name='shippingdetails',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
