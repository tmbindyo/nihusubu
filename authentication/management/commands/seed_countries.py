# seed_subregions.py
import json
from django.core.management.base import BaseCommand
from authentication.models import SubRegion, Region, Country, Timezone

class Command(BaseCommand):
    help = 'Import countries from a JSON file'

    def handle(self, *args, **kwargs):
        json_file_path = 'data/countries.json'

        with open(json_file_path, 'r') as file:
            countries_data = json.load(file)

        for country_data in countries_data:
            region_id = country_data.get('region_id')
            subregion_id = country_data.get('subregion_id')
            subregion = None

            region = Region.objects.filter(id=region_id).first()
            if region:
                subregion = SubRegion.objects.filter(id=subregion_id, region=region).first()

                country = country.objects.filter(id=country_data['id']).first()

                if not country:
                    country = country(
                        id=country_data['id'],
                        name=country_data['name'],
                        iso3=country_data['iso3'],
                        iso2=country_data['iso2'],
                        numeric_code=country_data['numeric_code'],
                        phone_code=country_data['phone_code'],
                        capital=country_data['capital'],
                        currency=country_data['currency'],
                        currency_name=country_data['currency_name'],
                        currency_symbol=country_data['currency_symbol'],
                        tld=country_data['tld'],
                        native=country_data['native'],
                        region=region,
                        subregion=subregion,
                        nationality=country_data['nationality'],
                        latitude=country_data['latitude'],
                        longitude=country_data['longitude'],
                        emoji=country_data['emoji'],
                        emojiU=country_data['emojiU'],
                        translations=country_data['translations']
                    )
                    country.save()

                    # Adding timezones to the country if timezone data exists
                    if 'timezones' in country_data and country_data['timezones']:
                        for timezone_data in country_data['timezones']:
                            timezone, _ = Timezone.objects.get_or_create(
                                zoneName=timezone_data['zoneName'],
                                gmtOffset=timezone_data['gmtOffset'],
                                gmtOffsetName=timezone_data['gmtOffsetName'],
                                abbreviation=timezone_data['abbreviation'],
                                tzName=timezone_data['tzName']
                            )
                            country.timezone.add(timezone)
            
            else:
                self.stdout.write(self.style.ERROR(f'Error on id:{country_data["id"]}, no region:{region_id}'))

        self.stdout.write(self.style.SUCCESS('Countries imported successfully'))
