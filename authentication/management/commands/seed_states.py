# management/commands/seed_regions.py
import json
from django.core.management.base import BaseCommand
from authentication.models import State, Country

class Command(BaseCommand):
    help = 'Import states from a JSON file'


    def handle(self, *args, **kwargs):
        json_file_path = 'data/states.json'

        with open(json_file_path, 'r') as file:
            states_data = json.load(file)

        for state_data in states_data:
            country_id = state_data['country_id']
            country = Country.objects.get(id=country_id)

            state = State.objects.filter(id=state_data['id']).first()
            if not state:
                state = State(
                    id=state_data['id'],
                    name=state_data['name'],
                    country=country,
                    state_code=state_data['state_code'],
                    type=state_data['type'],
                    latitude=state_data['latitude'],
                    longitude=state_data['longitude']
                )
                state.save()

        self.stdout.write(self.style.SUCCESS('States imported successfully'))
