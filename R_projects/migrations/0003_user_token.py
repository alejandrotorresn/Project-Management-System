# Generated by Django 3.0.4 on 2020-03-27 02:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('R_projects', '0002_project_token'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='token',
            field=models.CharField(default=1, max_length=30),
            preserve_default=False,
        ),
    ]
