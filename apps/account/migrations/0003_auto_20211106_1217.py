# Generated by Django 3.2.3 on 2021-11-06 10:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_company_description'),
    ]

    operations = [
        migrations.RenameField(
            model_name='client',
            old_name='data_created',
            new_name='date_created',
        ),
        migrations.RenameField(
            model_name='client',
            old_name='data_updated',
            new_name='date_updated',
        ),
        migrations.RenameField(
            model_name='company',
            old_name='data_created',
            new_name='date_created',
        ),
        migrations.RenameField(
            model_name='company',
            old_name='data_updated',
            new_name='date_updated',
        ),
        migrations.RenameField(
            model_name='employe',
            old_name='data_created',
            new_name='date_created',
        ),
        migrations.RenameField(
            model_name='employe',
            old_name='data_updated',
            new_name='date_updated',
        ),
    ]
