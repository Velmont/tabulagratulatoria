# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='entry',
            options={'verbose_name_plural': 'entries'},
        ),
        migrations.RemoveField(
            model_name='entry',
            name='full_name',
        ),
        migrations.RemoveField(
            model_name='entry',
            name='sort_name',
        ),
        migrations.AddField(
            model_name='entry',
            name='first_name',
            field=models.CharField(default='', max_length=255, blank=True),
        ),
        migrations.AddField(
            model_name='entry',
            name='last_name',
            field=models.CharField(default='', max_length=255, blank=True),
        ),
        migrations.AddField(
            model_name='entry',
            name='phone',
            field=models.CharField(default='', max_length=32, blank=True),
        ),
        migrations.AddField(
            model_name='entry',
            name='place',
            field=models.CharField(default='', max_length=64, blank=True),
        ),
        migrations.AddField(
            model_name='entry',
            name='shown_name',
            field=models.CharField(default='', max_length=255, blank=True),
        ),
    ]
