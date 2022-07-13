# Generated by Django 3.2.9 on 2022-06-01 08:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0010_auto_20220520_1511'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='seletectedjourney',
            name='state',
        ),
        migrations.AddField(
            model_name='seletectedjourney',
            name='status',
            field=models.CharField(choices=[('InOption', 'En option'), ('Voided', 'voide'), ('Emis', 'Emis')], default='InOption', max_length=20, verbose_name='status reservation'),
        ),
    ]
