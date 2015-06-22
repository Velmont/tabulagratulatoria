# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_add_group'),
    ]

    operations = [
        migrations.AddField(
            model_name='entry',
            name='num_issues',
            field=models.PositiveSmallIntegerField(default=False),
        ),
        migrations.AddField(
            model_name='entry',
            name='want_tg',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='entry',
            name='groups',
            field=models.ManyToManyField(to='core.Group', blank=True),
        ),
    ]
