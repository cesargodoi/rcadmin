# Generated by Django 3.2.16 on 2022-11-25 23:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('person', '0033_auto_20221122_1450'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='person',
            name='reg',
        ),
    ]
