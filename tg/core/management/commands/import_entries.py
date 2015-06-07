import csv
import os

import pytz
from django.utils.dateparse import parse_datetime
from django.utils.timezone import make_aware
from django.core.management.base import BaseCommand, CommandError

from core.models import Entry


class Command(BaseCommand):
    args = '<CSV file>'

    def handle(self, *args, **options):
        fn = args[0]
        if not os.path.isfile(fn):
            raise CommandError("File not found ({0})".format(fn))

        with open(fn) as fp:
            reader = csv.DictReader(fp)
            objects = []
            for row in reader:
                objects.append(create_entry_from_dict(row))
            Entry.objects.bulk_create(objects)
        print("Imported %d entries." % len(objects))


def create_entry_from_dict(data):
    p = Entry(
        full_name=data['name'],
        address=data.get('address'),
        email=data.get('email'),
    )
    return p
