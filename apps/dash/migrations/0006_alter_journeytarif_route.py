# Generated by Django 3.2.9 on 2022-06-03 09:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dash', '0005_covercity_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='journeytarif',
            name='route',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tarif_routes', to='dash.routing', verbose_name='routes'),
        ),
    ]
