from __future__ import unicode_literals

import csv
import os

import reversion
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from core.models import Entry
from core.models import Group
from core.models import Postnummer


class Command(BaseCommand):
    args = '<CSV file>'

    def init(self):
        self.groups = [Group.objects.get(slug__contains='no_tingar')]

    def handle(self, *args, **options):
        fn = args[0]
        if not os.path.isfile(fn):
            raise CommandError("File not found ({0})".format(fn))
        objects = []
        with open(fn) as fp:
            reader = csv.DictReader(fp)
            self.init()
            for row in reader:
                data = self.process(row)
                objects.append(self.create_entry_from_dict(data))
        # Figure out similarity
        names = [e.last_name for e in objects]
        num_entries = Entry.objects.filter(last_name__in=(names)).count()
        similarity = self.similarity(num_entries, len(names))
        if similarity > 0.9:
            print("Found {}% of the entries already in the database. "
                  "Halting, since this doesn't seem well thought out."
                  .format(similarity*100))
            return

        with reversion.create_revision():
            reversion.set_comment(u"Import av NOB")
            with transaction.atomic():
                for entry in objects:
                    entry.save()
            with transaction.atomic():
                for entry in objects:
                    entry.groups.add(*[g.pk for g in self.groups])
                    entry.save()
        print("Imported %d entries." % len(objects))
        print("- pks: %s" % ','.join(str(o.pk) for o in objects))

    @staticmethod
    def similarity(a, b):
        return 1-(float(abs(a-b))/max(a,b))

    def process(self, data):
        # Do some basic fixups
        for key, value in data.items():
            data[key] = value.decode('utf8').strip() if value else ''
        fields = [f.name for f in Entry._meta.local_fields]
        obj = {}
        for field in fields:
            try:
                value = getattr(self, 'process_%s' % field)(data)
            except AttributeError:
                value = data.get(field)
            if value is not None:
                obj[field] = value
        return self.final_process(obj, data)

    def process_postnummer(self, data):
        return data['Postnr'] or None

    def process_pay_postnummer(self, data):
        return data['Levering-Postnr'] or None

    def final_process(self, obj, data):
        name = ', '.join(data[k] for k in ('Firmanavn', 'Firmanavn 2') if
                         data[k])
        try:
            last_name, first_name = [n.strip() for n in name.split(',', 1)]
        except ValueError:
            last_name, first_name = name, ''
        pay_address = '\n'.join(data[k] for k in ('Adresse1', 'Adresse2',
                                                  'Adresse3', 'Land')
                                if data[k])
        address = '\n'.join(data[k] for k in ('Levering-Adresse1',
                                              'Levering-Adresse2',
                                              'Levering-Adresse3',
                                              'Levering-Land') if data[k])
        if pay_address and not address:
            address, pay_address = pay_address, address
        if data['Leverings attention'] and address:
            address = 'c/o %s\n%s' % (data['Leverings attention'],
                                      address)
        if data['Faktura attention']:
            pay_address = 'c/o %s\n%s' % (data['Faktura attention'],
                                          pay_address or address)
        if data['Levering-Firmanavn']:
            obj['shown_name'] = data['Levering-Firmanavn']
            obj['pay_name'] = name
            obj['pay_address'] = pay_address
        obj['postnummer'] = data['Levering-Postnr'] or data['Postnr']
        if data['Levering-Postnr'] and data['Postnr']:
            obj['pay_postnummer'] = data['Postnr']
        obj['address'] = address
        obj['first_name'] = first_name
        obj['last_name'] = last_name
        return obj


    def create_entry_from_dict(self, data):
        postnr = data.pop('postnummer', None)
        pay_postnr = data.pop('pay_postnummer', None)
        p = Entry(**data)
        def getpostnr(postnr):
            if not postnr:
                return
            try:
                return Postnummer.objects.get(postnr=postnr)
            except Postnummer.DoesNotExist:
                print("Could not find postnr %s, for address %s" %
                      (postnr, p.address))
        p.postnummer = getpostnr(postnr)
        p.pay_postnummer = getpostnr(pay_postnr)
        return p
