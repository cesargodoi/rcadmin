# Generated by Django 3.2.3 on 2021-06-06 19:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('person', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historic',
            name='description',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
