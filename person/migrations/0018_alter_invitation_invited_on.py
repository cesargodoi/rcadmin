# Generated by Django 3.2.15 on 2022-08-16 19:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('person', '0017_auto_20220816_0631'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invitation',
            name='invited_on',
            field=models.DateTimeField(auto_now=True, verbose_name='invited on'),
        ),
    ]
