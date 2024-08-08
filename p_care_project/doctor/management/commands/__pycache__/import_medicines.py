# doctor/management/commands/import_medicines.py

import csv
from django.core.management.base import BaseCommand
from doctor.models import Medicine

class Command(BaseCommand):
    help = 'Import medicines from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')

    def handle(self, *args, **options):
        csv_file = options['csv_file']
        with open(csv_file, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                Medicine.objects.create(name=row['name'], description=row['description'])
        self.stdout.write(self.style.SUCCESS('Successfully imported medicines'))
