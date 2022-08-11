# Generated by Django 3.2.14 on 2022-08-09 17:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('center', '0010_remove_center_secretary'),
        ('person', '0011_alter_person_reg'),
        ('event', '0006_alter_event_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='active'),
        ),
        migrations.AlterField(
            model_name='activity',
            name='multi_date',
            field=models.BooleanField(default=False, verbose_name='multi date'),
        ),
        migrations.AlterField(
            model_name='activity',
            name='name',
            field=models.CharField(max_length=50, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='event',
            name='activity',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='event.activity', verbose_name='activity'),
        ),
        migrations.AlterField(
            model_name='event',
            name='center',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='center.center', verbose_name='center'),
        ),
        migrations.AlterField(
            model_name='event',
            name='date',
            field=models.DateField(verbose_name='date'),
        ),
        migrations.AlterField(
            model_name='event',
            name='deadline',
            field=models.DateTimeField(blank=True, null=True, verbose_name='dead line'),
        ),
        migrations.AlterField(
            model_name='event',
            name='description',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='description'),
        ),
        migrations.AlterField(
            model_name='event',
            name='frequencies',
            field=models.ManyToManyField(blank=True, through='event.Frequency', to='person.Person', verbose_name='frequencies'),
        ),
        migrations.AlterField(
            model_name='event',
            name='qr_code',
            field=models.ImageField(blank=True, upload_to='event_qr_codes', verbose_name='qr code'),
        ),
        migrations.AlterField(
            model_name='frequency',
            name='aspect',
            field=models.CharField(choices=[('--', '--'), ('A1', '1st. Aspect'), ('A2', '2nd. Aspect'), ('A3', '3rd. Aspect'), ('A4', '4th. Aspect'), ('GR', 'Grail'), ('A5', '5th. Aspect'), ('A6', '6th. Aspect')], default='--', max_length=2, verbose_name='aspect'),
        ),
        migrations.AlterField(
            model_name='frequency',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='event.event', verbose_name='event'),
        ),
        migrations.AlterField(
            model_name='frequency',
            name='observations',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='observations'),
        ),
        migrations.AlterField(
            model_name='frequency',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='person.person', verbose_name='person'),
        ),
        migrations.AlterField(
            model_name='frequency',
            name='ranking',
            field=models.IntegerField(default=0, verbose_name='ranking'),
        ),
    ]