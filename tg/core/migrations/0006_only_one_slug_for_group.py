# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def fill_in_slug(apps, schema_editor):
    Group = apps.get_model('core', 'Group')
    for group in Group.objects.all():
        group.slug = "%s:%s" % (group.category, group.name)
        group.save()


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_add_num_issues_and_tg'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='slug',
            field=models.SlugField(default=''),
            preserve_default=False,
        ),
        migrations.RunPython(fill_in_slug),
        migrations.RemoveField(
            model_name='group',
            name='category',
        ),
        migrations.RemoveField(
            model_name='group',
            name='name',
        ),
    ]
