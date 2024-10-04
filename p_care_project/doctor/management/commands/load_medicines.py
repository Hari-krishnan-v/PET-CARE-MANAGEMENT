import csv
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from doctor.models import Medicine

class Command(BaseCommand):
    help = 'Load medicines from a CSV file'

    def handle(self, *args, **kwargs):
        file_path = os.path.join(settings.BASE_DIR, 'doctor', 'veterinary_medicines.csv')
        self.stdout.write(self.style.NOTICE(f"Looking for file at: {file_path}"))
        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR(f"File not found: {file_path}"))
            return

        with open(file_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                Medicine.objects.create(
                    name=row['name'],
                    dosage=row['dosage'],
                    description=row['description']
                )
        self.stdout.write(self.style.SUCCESS('Successfully loaded medicines'))
