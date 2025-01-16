# Generated by Django 4.2.17 on 2025-01-15 18:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0057_orderhistory_quantity'),
    ]

    operations = [
        migrations.CreateModel(
            name='herocontent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_added', models.DateTimeField(auto_now_add=True, null=True)),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='heroproduct', to='store.products')),
            ],
        ),
    ]
