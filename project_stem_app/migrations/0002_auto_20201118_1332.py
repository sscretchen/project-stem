# Generated by Django 3.1.3 on 2020-11-18 18:32

from django.db import migrations, models
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('project_stem_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='sessionyearmodel',
            managers=[
                ('object', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterField(
            model_name='attendance',
            name='attendance_date',
            field=models.DateField(auto_now_add=True),
        ),
    ]
