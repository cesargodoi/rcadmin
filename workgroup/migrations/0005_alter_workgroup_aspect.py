# Generated by Django 3.2.5 on 2021-08-01 20:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workgroup', '0004_alter_workgroup_workgroup_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workgroup',
            name='aspect',
            field=models.CharField(choices=[('--', '--'), ('A1', '1st. Aspect'), ('A2', '2nd. Aspect'), ('A3', '3rd. Aspect'), ('A4', '4th. Aspect'), ('GR', 'Grail'), ('A5', '5th. Aspect'), ('A6', '6th. Aspect')], default='--', max_length=2),
        ),
    ]
