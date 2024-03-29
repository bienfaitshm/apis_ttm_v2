# Generated by Django 3.2.9 on 2022-06-03 07:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0011_auto_20220601_1008'),
    ]

    operations = [
        migrations.CreateModel(
            name='JourneyClientFolderMoreSerializer',
            fields=[
                ('journeyclientfolder_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='clients.journeyclientfolder')),
            ],
            options={
                'abstract': False,
            },
            bases=('clients.journeyclientfolder',),
        ),
        migrations.AlterField(
            model_name='seletectedjourney',
            name='folder',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reservations', to='clients.journeyclientfolder', verbose_name='folder'),
        ),
    ]
