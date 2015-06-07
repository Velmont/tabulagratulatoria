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

        csv.register_dialect('tabs', delimiter='\t')
        with open(fn) as fp:
            reader = csv.DictReader(fp, dialect='tabs')
            objects = []
            for row in reader:
                objects.append(create_postnummer_from_dict(row))
            Postnummer.objects.bulk_create(objects)
        print("Imported %d postnummers." % len(objects))


def create_postnummer_from_dict(data):
    p = Postnummer(
        postnr=data['POSTNR'].strip().replace(' ', ''),
        poststad=data['POSTSTAD'],
        bruksomrade=data['BRUKSOMRÅDE'],
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
