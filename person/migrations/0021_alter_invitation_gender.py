# Generated by Django 3.2.15 on 2022-08-21 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('person', '0020_auto_20220819_0930'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invitation',
            name='gender',
            field=models.CharField(choices=[('M', 'male'), ('F', 'female'), ('-', 'do not inform')], max_length=1, verbose_name='gender'),
        ),
    ]
