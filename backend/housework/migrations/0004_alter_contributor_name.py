# Generated by Django 5.1.4 on 2025-01-08 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('housework', '0003_rename_scale_houseworkrecord_points'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contributor',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
