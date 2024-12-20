# Generated by Django 5.1.4 on 2024-12-11 00:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0011_subcategory_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='featured_products',
            name='image',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fetured_product_image', to='store.product_image'),
        ),
    ]
