# Generated by Django 4.2.17 on 2025-01-15 19:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0060_pages'),
    ]

    operations = [
        migrations.AddField(
            model_name='pages',
            name='slug',
            field=models.SlugField(max_length=150, null=True),
        ),
    ]
