# Generated by Django 5.1.4 on 2024-12-16 11:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0019_alter_products_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='wanjos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, null=True)),
                ('parent', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='childrent', to='store.wanjos')),
            ],
        ),
    ]
