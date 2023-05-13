# Generated by Django 3.2.4 on 2023-05-10 07:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chat_app', '0009_alter_chatuser_interests'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatuser',
            name='is_online',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.CreateModel(
            name='Connection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('started_at', models.DateTimeField(auto_now_add=True)),
                ('ended_at', models.DateTimeField(null=True)),
                ('user1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='connections_as_user1', to=settings.AUTH_USER_MODEL)),
                ('user2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='connections_as_user2', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]