# Generated by Django 3.2.7 on 2021-10-09 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('publicwork', '0016_auto_20210801_1727'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicofseeker',
            name='occurrence',
            field=models.CharField(choices=[('OBS', 'observation'), ('NEW', 'new'), ('MBR', 'member'), ('INS', 'installing'), ('ITD', 'installed'), ('STD', 'stand by'), ('RST', 'restriction')], default='MBR', max_length=3),
        ),
        migrations.AlterField(
            model_name='seeker',
            name='country',
            field=models.CharField(choices=[('BR', 'Brazil')], default='BR', max_length=2),
        ),
        migrations.AlterField(
            model_name='seeker',
            name='status',
            field=models.CharField(blank=True, choices=[('OBS', 'observation'), ('NEW', 'new'), ('MBR', 'member'), ('INS', 'installing'), ('ITD', 'installed'), ('STD', 'stand by'), ('RST', 'restriction')], max_length=3),
        ),
        migrations.AlterField(
            model_name='tempregofseeker',
            name='country',
            field=models.CharField(choices=[('BR', 'Brazil')], default='BR', max_length=2),
        ),
    ]
