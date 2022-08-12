# Generated by Django 3.2.14 on 2022-08-09 12:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('center', '0010_remove_center_secretary'),
        ('person', '0008_alter_person_short_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='aspect',
            field=models.CharField(choices=[('--', '--'), ('A1', '1st. Aspect'), ('A2', '2nd. Aspect'), ('A3', '3rd. Aspect'), ('A4', '4th. Aspect'), ('GR', 'Grail'), ('A5', '5th. Aspect'), ('A6', '6th. Aspect')], default='--', max_length=2, verbose_name='aspect'),
        ),
        migrations.AlterField(
            model_name='person',
            name='aspect_date',
            field=models.DateField(blank=True, null=True, verbose_name='date'),
        ),
        migrations.AlterField(
            model_name='person',
            name='center',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='center.center', verbose_name='center'),
        ),
        migrations.AlterField(
            model_name='person',
            name='name',
            field=models.CharField(max_length=100, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='person',
            name='observations',
            field=models.TextField(blank=True, verbose_name='observations'),
        ),
        migrations.AlterField(
            model_name='person',
            name='reg',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='register'),
        ),
        migrations.AlterField(
            model_name='person',
            name='short_name',
            field=models.CharField(blank=True, editable=False, max_length=80, null=True, verbose_name='short name'),
        ),
    ]
