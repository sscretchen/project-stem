# Generated by Django 3.1.3 on 2020-11-22 19:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_stem_app', '0003_auto_20201118_1750'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='attendance_date',
            field=models.DateField(),
        ),
    ]
