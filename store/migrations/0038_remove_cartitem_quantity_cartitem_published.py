# Generated by Django 5.1.4 on 2024-12-19 21:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0037_products_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitem',
            name='quantity',
        ),
        migrations.AddField(
            model_name='cartitem',
            name='published',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]