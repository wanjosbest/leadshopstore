# Generated by Django 5.1.4 on 2024-12-20 12:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0039_cartitem_quantity'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitem',
            name='cart',
        ),
    ]
