# Generated by Django 3.2.4 on 2023-05-10 08:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat_app', '0010_auto_20230510_1242'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chatuser',
            name='is_online',
        ),
        migrations.AlterField(
            model_name='chatuser',
            name='is_active',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
