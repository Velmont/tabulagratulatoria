# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0001_initial'),
        ('core', '0002_add_first_and_last_name_etc'),
    ]

    operations = [
        migrations.AddField(
            model_name='entry',
            name='notes',
            field=models.TextField(default='', blank=True),
        ),
        migrations.AddField(
            model_name='entry',
            name='tags',
            field=taggit.managers.TaggableManager(
                to='taggit.Tag',
                through='taggit.TaggedItem',
                help_text='A comma-separated list of tags.',
                verbose_name='Tags'),
        ),
    ]
