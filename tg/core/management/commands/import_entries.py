from __future__ import print_function
from __future__ import unicode_literals

import csv
import os
import re

from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import MultipleObjectsReturned

import core.models
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
            total_n = 0
            for row in reader:
                total_n += 1
                e = create_entry_from_dict(row)
                try:
                    e2 = Entry.objects.get(first_name=e.first_name,
                      last_name=e.last_name)
                    print(("Already exists %s %d!" % (e, e2.pk)).encode('utf8'))
                    continue
                except Entry.DoesNotExist:
                    pass
                except MultipleObjectsReturned:
                    print("Multiple items for %s!" % e)
                    continue;
                if e.email:
                    try:
                        e2 = Entry.objects.get(email=e.email)
                        print("Email already exists %s %d!" % (e, e2.pk))
                        continue
                    except Entry.DoesNotExist:
                        pass
                print("Legg til %s" % e)
                e.notes = 'imp:samlaget'
                objects.append(e)
            Entry.objects.bulk_create(objects)
        print("Imported %d entries of %d." % (len(objects), total_n))


def create_entry_from_dict(data):
    p = Entry(
        address=data.get('address').decode('utf8'),
        email=data.get('email').decode('utf8'),
        phone=data.get('tlf').decode('utf8'),
    )
    if data.get('smth'):
        p.phone += " / %s" % data['smth']
    if data.get('first_name'):
        p.first_name = data['first_name'].decode('utf8')
        p.last_name = data['last_name'].decode('utf8')
    else:
        name = data['name'].decode('utf8')
        if ',' in name:
            try:
                p.last_name, p.first_name = name.split(',')
            except ValueError:
                print("Couldn't split name %s" % name)
                p.shown_name = name
        else:
            p.shown_name = name
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
    if data.get('postnr'):
        postnr = data['postnr'].zfill(4)
        try:
            p.postnummer = Postnummer.objects.get(postnr=postnr)
        except Postnummer.DoesNotExist:
            print("Could not find postnr %s for %s" % (data['postnr'], p))
    return p
