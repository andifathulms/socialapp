# Generated by Django 3.2.7 on 2021-11-06 05:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0004_alter_forumpost_view'),
    ]

    operations = [
        migrations.AddField(
            model_name='subject',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='uploads/subject_img/'),
        ),
    ]
