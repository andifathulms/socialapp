# Generated by Django 3.2.7 on 2021-10-08 07:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('follower', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FollowingList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('following', models.ManyToManyField(blank=True, related_name='following', to=settings.AUTH_USER_MODEL)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='userfollowing', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
