from django.core.management.base import BaseCommand
from django.apps import apps
from django.conf import settings
import json
from pathlib import Path


class Command(BaseCommand):
    help = 'Добавляет в БД список стран'

    def handle(self, *args, **options):
        static_url = settings.STATICFILES_DIRS[0]
        filename = Path(static_url, 'users/data/countries.json')

        with open(filename, 'r') as json_file:
            countries_data = json.load(json_file)
            Country = apps.get_model('users', 'Country')
            for country_data in countries_data:
                Country.objects.create(
                    name=country_data['name'],
                    code=country_data['code']
                )

        self.stdout.write(self.style.SUCCESS('Successfully loaded initial countries'))