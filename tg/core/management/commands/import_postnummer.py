# encoding=utf-8
from __future__ import unicode_literals
from __future__ import print_function

import csv
import os

import pytz
from django.utils.dateparse import parse_datetime
from django.utils.timezone import make_aware
from django.core.management.base import BaseCommand, CommandError

from core.models import Postnummer


class Command(BaseCommand):
    args = '<Tab seperated Erik Bolstad postnr-CSV files>'

    def handle(self, *args, **options):
        fn = args[0]
        if not os.path.isfile(fn):
            raise CommandError("File not found ({0})".format(fn))
        try:
            last_update = (Postnummer.objects.filter(
                    sist_oppdatert__isnull=False)
                .latest('sist_oppdatert')
                .sist_oppdatert)
            last_update = parse_datetime('2015-01-01 10:00:00Z')
        except Postnummer.DoesNotExist:
            last_update = None
        csv.register_dialect('tabs', delimiter=str('\t'))
        with open(fn) as fp:
            reader = csv.DictReader(fp, dialect='tabs')
            objects = []
            for row in reader:
                ps = create_postnummer_from_dict(row)
                if (last_update and ps.sist_oppdatert
                    and last_update < ps.sist_oppdatert):
                    try:
                        obj = Postnummer.objects.get(postnr=ps.postnr)
                    except Postnummer.DoesNotExist:
                        obj = ps
                        ps.save()
                        print("Creating %s." % ps.postnr)
                    else:
                        for k, v in ps.__dict__.items():
                            if k == 'id' or k[0] == '_':
                                continue
                            setattr(obj, k, v)
                        print("Updating %s %d." % (obj.postnr, obj.id))
                        obj.save()
                    objects.append(obj)
                elif not last_update:
                    objects.append(ps)
            if not last_update:
                Postnummer.objects.bulk_create(objects)
        print("Imported %d postnummers." % len(objects))


def create_postnummer_from_dict(data):
    p = Postnummer(
        postnr=data['POSTNR'].strip().replace(' ', ''),
        poststad=data['POSTSTAD'],
        bruksomrade=data['BRUKSOMRADE'],
        bydel=data['BYDEL'],
        kommnr=data['KOMMNR'],
        kommune=data['KOMMUNE'],
        fylke=data['FYLKE'],
        lat=float(data['LAT']),
        lon=float(data['LON']),
        datakvalitet=data['DATAKVALITET'],
    )
    if data['FOLKETAL']:
        p.folketal = int(data['FOLKETAL'].strip())
    try:
        updated = parse_datetime(data['SIST OPPDATERT'])
    except ValueError:
        pass
    else:
        p.sist_oppdatert = make_aware(updated, pytz.timezone('Europe/Oslo'))
    return p
