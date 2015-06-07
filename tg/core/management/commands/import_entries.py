from __future__ import unicode_literals

import csv
import os
import re

from django.core.management.base import BaseCommand, CommandError

from core.models import Entry
from core.models import Postnummer


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
        address=data.get('address').decode('utf8'),
        email=data.get('email').decode('utf8'),
        phone=data.get('tlf').decode('utf8'),
    )
    last_address_line = p.address.split(',')[-1]
    m = re.match('\W(\d{4})\W(.+)$', last_address_line)
    if m:
        try:
            postnr = Postnummer.objects.get(postnr=m.group(1))
            place = m.group(2)
            if postnr.poststad.lower() == place.lower():
                p.postnummer = postnr
            else:
                print("Expected place {}, got {} for {}."
                      .format(postnr.poststad, place, p.address))
        except Postnummer.DoesNotExist:
            print("Could not find postnr %s, for address %s" %
                  (m.group(1), p.address))
    if data['smth']:
        p.phone += " / %s" % data['smth']
    name = data['name'].decode('utf8')
    if ',' in name:
        try:
            p.last_name, p.first_name = name.split(',')
        except ValueError:
            print("Couldn't split name %s" % name)
            p.shown_name = name
    else:
        p.shown_name = name

    return p
