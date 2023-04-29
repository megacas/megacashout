# myapp/management/commands/import_products.py

from django.core.management.base import BaseCommand
from store.models import Product
import csv

class Command(BaseCommand):
    help = 'Import products from a data file'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to the data file')

    def handle(self, *args, **options):
        file_path = options['file_path']

        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                Product.objects.create(
                    name=row['name'],
                    Balance=row['Balance'],
                    price=row['price'],
                    Title = row['Title'],
                    Info = row['Info'],
                    slug = row['slug'],
                )

        self.stdout.write(self.style.SUCCESS('Products imported successfully.'))
