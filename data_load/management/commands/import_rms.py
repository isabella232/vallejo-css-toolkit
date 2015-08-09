import re
import csv

from django.core.management.base import BaseCommand

from geo.utils.geocode import geocode
from workflow.models import Case, CaseStatus

def import_rms(f):

    dialect = csv.Sniffer().sniff(f.read(1048576), delimiters=",")
    f.seek(0)
    reader = csv.reader(f, dialect)

    next(reader)

    for i, row in enumerate(reader):
        incnum, address = row

        r = re.match('(?P<street_number>\d*) (?P<street_name>.*)', address)

        if not r:
            print 'no parse: ', address
            continue

        street_number = int(r.groupdict().get('street_number'))
        street_name = r.groupdict().get('street_name')

        lat, lng = None, None

        results = geocode(street_number, street_name.lower())

        if results:
            lat = results[0].get('lat')
            lng = results[0].get('lng')

        active_status = CaseStatus.objects.get(name='Active')

        Case.objects.get_or_create(
            description='pd call for service',
            resolution='pd call for service',
            status=active_status,
            lat=lat,
            lng=lng,
            dept=1
        )

class Command(BaseCommand):
    # COPY (Select incnum, location from rms_incident where location is not null limit 200) TO '/Users/andrew/Desktop/rms.csv' DELIMITER ',' CSV HEADER;

    def add_arguments(self, parser):
        parser.add_argument('--file', type=file)

    def handle(self, *args, **options):
        if not options.get('file'):
            return

        import_rms(options['file'])
