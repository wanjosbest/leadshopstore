# Generated by Django 4.2.17 on 2025-01-18 05:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0073_newslettersubscription'),
    ]

    operations = [
        migrations.CreateModel(
            name='footerpages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('page', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='footerpages', to='store.pages')),
            ],
        ),
    ]
