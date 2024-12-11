# Generated by Django 5.1.4 on 2024-12-10 23:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_products_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='product_image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, null=True, unique=True)),
                ('image', models.ImageField(null=True, unique=True, upload_to='img')),
            ],
        ),
    ]
