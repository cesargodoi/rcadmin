# Generated by Django 3.2.7 on 2021-10-09 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('center', '0004_auto_20210801_1727'),
    ]

    operations = [
        migrations.AlterField(
            model_name='center',
            name='country',
            field=models.CharField(choices=[('BR', 'Brazil')], default='BR', max_length=2),
        ),
    ]