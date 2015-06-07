# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', model_utils.fields.StatusField(max_length=100, default='new', choices=[('new', 'new'), ('checked', 'checked')], no_check_for_status=True)),
                ('full_name', models.CharField(max_length=255)),
                ('sort_name', models.CharField(max_length=255, default='', blank=True)),
                ('email', models.EmailField(max_length=254, default='', blank=True)),
                ('address', models.CharField(max_length=255, default='', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Postnummer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('postnr', models.CharField(max_length=6)),
                ('poststad', models.CharField(max_length=50)),
                ('bruksomrade', models.CharField(max_length=50)),
                ('folketal', models.SmallIntegerField(blank=True, null=True)),
                ('bydel', models.CharField(max_length=50)),
                ('kommnr', models.CharField(max_length=50)),
                ('kommune', models.CharField(max_length=50)),
                ('fylke', models.CharField(max_length=50)),
                ('lat', models.FloatField()),
                ('lon', models.FloatField()),
                ('datakvalitet', models.SmallIntegerField()),
                ('sist_oppdatert', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='entry',
            name='postnummer',
            field=models.ForeignKey(to='core.Postnummer', null=True),
        ),
    ]
