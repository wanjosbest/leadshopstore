# Generated by Django 5.1.4 on 2024-12-18 17:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0032_alter_review_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='email',
            field=models.EmailField(max_length=254, null=True),
        ),
    ]
