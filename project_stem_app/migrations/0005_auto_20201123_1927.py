# Generated by Django 3.1.3 on 2020-11-24 00:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_stem_app', '0004_auto_20201122_1450'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentleavereport',
            name='leave_status',
            field=models.IntegerField(default=0),
        ),
    ]
