# Generated by Django 3.2.9 on 2022-04-29 10:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dash', '0005_covercity_image'),
        ('clients', '0005_seletectedjourney_state'),
    ]

    operations = [
        migrations.AddField(
            model_name='seletectedjourney',
            name='journey_class',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to='dash.journeyclass', verbose_name="journe's class"),
        ),
    ]
