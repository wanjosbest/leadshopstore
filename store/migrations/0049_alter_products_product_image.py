# Generated by Django 4.2.17 on 2025-01-10 17:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0048_rename_address_shippingdetails_address_line_1_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='product_image',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Product_image', to='store.product_image'),
        ),
    ]
