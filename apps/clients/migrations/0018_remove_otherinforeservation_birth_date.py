# Generated by Django 3.2.9 on 2021-11-26 04:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0017_alter_validationpayment_journey_selected'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='otherinforeservation',
            name='birth_date',
        ),
    ]