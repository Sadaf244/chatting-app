# Generated by Django 3.2.4 on 2023-05-08 18:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ChatUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('full_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phone', models.CharField(max_length=20, unique=True)),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], max_length=1)),
                ('country', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=255)),
                ('interests', models.CharField(choices=[('Food', 'Food'), ('Travel', 'Travel'), ('Movies', 'Movies')], max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
