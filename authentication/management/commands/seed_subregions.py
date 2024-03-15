# seed_subregions.py
import json
from django.core.management.base import BaseCommand
from authentication.models import SubRegion, Region

class Command(BaseCommand):
    help = 'Seed subregions data from JSON file'

    def handle(self, *args, **options):
        file_path = 'data/subregions.json'
        
        with open(file_path, 'r', encoding='utf-8') as file:
            subregions_data = json.load(file)
        
        for subregion_data in subregions_data:
            region_id = subregion_data['region_id']
            region = Region.objects.get(pk=region_id)
            translations = subregion_data['translations']

            sub_region = SubRegion.objects.filter(id=subregion_data['id']).first()
            if not sub_region:
            
                sub_region = SubRegion.objects.create(
                    id=subregion_data['id'],
                    name=subregion_data['name'],
                    region=region,
                    translations=translations,
                    wikiDataId=subregion_data['wikiDataId']
                )
        
        self.stdout.write(self.style.SUCCESS('Subregions data seeded successfully'))
