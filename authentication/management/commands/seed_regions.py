# management/commands/seed_regions.py
import json
from django.core.management.base import BaseCommand
from authentication.models import Region

class Command(BaseCommand):
    help = 'Seed the database with regions from a JSON file'

    def handle(self, *args, **options):
        # Path to your JSON file
        json_file_path = 'data/regions.json'

        with open(json_file_path) as f:
            regions_data = json.load(f)

        for region_data in regions_data:
            region = Region.objects.filter(id=region_data['id']).first()

            if not region:
                region = Region(
                    id=region_data['id'],
                    name=region_data['name'],
                    translations=region_data['translations'],
                    wikiDataId=region_data['wikiDataId']
                )
                region.save()

        self.stdout.write(self.style.SUCCESS('Regions seeded successfully.'))
