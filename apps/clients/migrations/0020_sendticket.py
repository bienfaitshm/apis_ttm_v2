# Generated by Django 3.2.9 on 2022-10-28 08:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0019_alter_seletectedjourney_folder'),
    ]

    operations = [
        migrations.CreateModel(
            name='SendTicket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now_add=True)),
                ('sended', models.BooleanField(default=False, verbose_name='sended Ticket')),
                ('to', models.CharField(blank=True, max_length=200, null=True, verbose_name='sended Ticket')),
                ('journey', models.OneToOneField(help_text='the selected journey reservations', on_delete=django.db.models.deletion.CASCADE, related_name='send_ticket', to='clients.seletectedjourney', verbose_name='reservations')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
