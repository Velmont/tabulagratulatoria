# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_only_one_slug_for_group'),
    ]

    operations = [
        migrations.AddField(
            model_name='entry',
            name='pay_address',
            field=models.TextField(default='', blank=True),
        ),
        migrations.AddField(
            model_name='entry',
            name='pay_name',
            field=models.CharField(default='', max_length=255, blank=True),
        ),
        migrations.AddField(
            model_name='entry',
            name='pay_postnummer',
            field=models.ForeignKey(related_name='+', blank=True, to='core.Postnummer', null=True),
        ),
        migrations.AlterField(
            model_name='entry',
            name='address',
            field=models.TextField(default='', blank=True),
        ),
        migrations.AlterField(
            model_name='entry',
            name='postnummer',
            field=models.ForeignKey(blank=True, to='core.Postnummer', null=True),
        ),
    ]
