# Generated by Django 3.2.9 on 2022-03-31 13:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CabinePlane',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(default='nameDefaultConfig', max_length=256)),
                ('devMod', models.BooleanField(default=False)),
                ('x', models.IntegerField(help_text='configuration in x or the total number of line seat')),
                ('y', models.IntegerField(help_text='configuration in y or the total of column of seats')),
                ('clipboard', models.CharField(choices=[('SEAT', 'seating'), ('SPACE', 'space or  couloir')], default='SEAT', max_length=10)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cabine_plane', to='account.company')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Cars',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now_add=True)),
                ('typeAppareil', models.CharField(max_length=200)),
                ('indexKm', models.CharField(max_length=200)),
                ('immatriculation', models.CharField(max_length=200)),
                ('codeAppareil', models.CharField(max_length=200)),
                ('etat', models.CharField(choices=[('OP', 'Operationnel'), ('NO', 'Non operationnel'), ('HS', 'Hors service')], max_length=10)),
                ('miseEnService', models.CharField(max_length=200)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pompany_cars', to='account.company')),
                ('configCab', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cars', to='dash.cabineplane')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CoverCity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now_add=True)),
                ('town', models.CharField(max_length=200, verbose_name='cover city')),
                ('code', models.CharField(max_length=200, null=True, verbose_name='code')),
                ('latitude', models.FloatField(default=None, null=True, verbose_name='latitude')),
                ('longitude', models.FloatField(default=None, null=True, verbose_name='latitude')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cities', to='account.company')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='JourneyClass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now_add=True)),
                ('code', models.CharField(max_length=10, verbose_name='code_class')),
                ('name', models.CharField(max_length=10, verbose_name='name_class')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='journey_class', to='account.company')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PointOfSale',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=200, verbose_name='nom')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='point_of_sale', to='account.company', verbose_name='point-of-sale')),
                ('town', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='town_pos', to='dash.covercity', verbose_name='town of sale')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Seat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=50, verbose_name='nom')),
                ('type', models.CharField(choices=[('SEAT', 'SEAT'), ('SPACE', 'SPACE')], max_length=10, verbose_name='type')),
                ('x', models.IntegerField(verbose_name='x')),
                ('y', models.IntegerField(verbose_name='y')),
                ('idConfigCab', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='seats', to='dash.cabineplane')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Routing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now_add=True)),
                ('distance', models.FloatField(default=0.0, verbose_name='distance(Km)')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='routing', to='account.company')),
                ('whereFrom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='whereFrom', to='dash.covercity', verbose_name='where from')),
                ('whereTo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='whereTo', to='dash.covercity', verbose_name='where to')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PointOfSaleWorker',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now_add=True)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='worker_saler', to='account.company', verbose_name='point-of-sale worker')),
                ('pointOfSale', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='worker_pos', to='dash.pointofsale', verbose_name='point-of-sale')),
                ('worker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='worker', to='account.employe', verbose_name='worker')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='JourneyTarif',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now_add=True)),
                ('devise', models.CharField(choices=[('CDF', 'CDF'), ('USD', 'USD')], default='CDF', max_length=5, verbose_name='money devise')),
                ('adult', models.FloatField(default=0.0, verbose_name='tarif_adult')),
                ('child', models.FloatField(default=0.0, verbose_name='tarif_child')),
                ('baby', models.FloatField(default=0.0, verbose_name='tarif_baby')),
                ('actif', models.BooleanField(default=0.0, verbose_name='actif_tarif')),
                ('journey_class', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tarif', to='dash.journeyclass')),
                ('route', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='routes', to='dash.routing', verbose_name='routes')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Journey',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now_add=True)),
                ('numJourney', models.CharField(max_length=50, verbose_name='number of journey')),
                ('dateDeparture', models.DateField(verbose_name='date of departure')),
                ('dateReturn', models.DateField(verbose_name='date of departure')),
                ('hoursDeparture', models.TimeField(verbose_name='hours of departure')),
                ('hoursReturn', models.TimeField(verbose_name='hours of return')),
                ('cars', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cars_journies', to='dash.cars', verbose_name='cars')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='journey', to='account.company')),
                ('routes', models.ManyToManyField(related_name='routing_journies', to='dash.Routing', verbose_name='routing')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
