# Generated by Django 3.2.15 on 2022-08-15 10:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('person', '0015_tempregofperson_center'),
    ]

    operations = [
        migrations.AddField(
            model_name='tempregofperson',
            name='imported',
            field=models.BooleanField(default=False),
        ),
    ]