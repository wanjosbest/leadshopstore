# Generated by Django 4.2.17 on 2025-01-17 19:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0070_alter_pages_page_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='paid',
        ),
    ]
