# Generated by Django 3.2.5 on 2021-07-07 21:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('publicwork', '0010_auto_20210706_1730'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tempregofseeker',
            name='code',
        ),
        migrations.AddField(
            model_name='tempregofseeker',
            name='solicited_on',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='tempregofseeker',
            name='phone',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='tempregofseeker',
            name='state',
            field=models.CharField(max_length=2),
        ),
    ]
