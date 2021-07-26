# Generated by Django 3.2.5 on 2021-07-15 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('person', '0002_alter_historic_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='status',
            field=models.CharField(choices=[('---', '---'), ('ACT', 'active'), ('LIC', 'licensed'), ('DEA', 'dead'), ('DIS', 'disconnected'), ('REM', 'removed')], default='ACT', max_length=3),
        ),
    ]
