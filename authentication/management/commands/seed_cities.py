# management/commands/seed_regions.py
import json
from django.core.management.base import BaseCommand
from authentication.models import State, City

class Command(BaseCommand):
    help = 'Seeds cities data from cities.json'

    def handle(self, *args, **kwargs):
        json_file_path = 'data/cities.json'

        with open(json_file_path, 'r') as f:
            cities_data = json.load(f)

        for city_data in cities_data:
            state_id = city_data['state_id']
            state = State.objects.get(id=state_id)

            city = City.objects.filter(id=city_data['id']).first()
            if not city: 
                city = City.objects.create(
                    id=city_data['id'],
                    name=city_data['name'],
                    latitude=city_data['latitude'],
                    longitude=city_data['longitude'],
                    wikiDataId=city_data['wikiDataId'],
                    state=state
                )

            self.stdout.write(self.style.SUCCESS(f'Successfully created city: {city.name}'))
