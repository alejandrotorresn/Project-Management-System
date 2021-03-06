# Generated by Django 3.0.4 on 2020-04-02 23:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('R_projects', '0006_auto_20200327_1025'),
    ]

    operations = [
        migrations.CreateModel(
            name='User_Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=30)),
            ],
        ),
        migrations.RemoveField(
            model_name='user',
            name='projects',
        ),
        migrations.RemoveField(
            model_name='user',
            name='token',
        ),
        migrations.AddField(
            model_name='user',
            name='director',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='project',
            name='director',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='R_projects.User'),
        ),
        migrations.DeleteModel(
            name='Director',
        ),
        migrations.AddField(
            model_name='user_project',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='R_projects.Project'),
        ),
        migrations.AddField(
            model_name='user_project',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='R_projects.User'),
        ),
    ]
