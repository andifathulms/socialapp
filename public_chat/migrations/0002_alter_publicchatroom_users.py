# Generated by Django 3.2.7 on 2021-09-22 18:55

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('public_chat', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publicchatroom',
            name='users',
            field=models.ManyToManyField(blank=True, help_text='users who are connected to chat room.', null=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
