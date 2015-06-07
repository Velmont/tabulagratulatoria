# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_add_first_and_last_name_etc'),
    ]

    operations = [
        migrations.AddField(
            model_name='entry',
            name='notes',
            field=models.TextField(default='', blank=True),
        ),
    ]
