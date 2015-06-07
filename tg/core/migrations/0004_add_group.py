# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_entry_notes'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.SlugField()),
                ('category', models.SlugField()),
            ],
        ),
        migrations.AddField(
            model_name='entry',
            name='groups',
            field=models.ManyToManyField(to='core.Group'),
        ),
    ]
