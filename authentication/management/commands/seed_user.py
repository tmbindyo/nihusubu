import uuid
from django.db import transaction
from django.contrib.auth.models import Group
from authentication.models import UserAccount
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from institution.models import InstitutionType, Institution

User = get_user_model()

class Command(BaseCommand):
    help = 'Seed the User model with initial data'

    def handle(self, *args, **options):
        # Add your model-specific seed data here
    
        # admin account
        user_data = [
            {
                'first_name': 'MyGas',
                'last_name': 'Admin',
                'is_superuser': True,
                'email': 'admin@my-gas.com',
                'password': make_password('password'),
            },
        ]

        # Seed the database
        for data in user_data:
            user_exits = User.objects.filter(email=data['email']).first()
            if not user_exits:
                user_exits = User.objects.create(**data)
            group = Group.objects.get(name='Admin')
            if group:
                # create user accounts
                user_account_data = {
                    "user":user_exits,
                    "user_group":group,
                    "is_admin":True,
                    "is_active":True,
                    "user_account_type":1,
                }

                user_account, created = UserAccount.objects.get_or_create(
                    user=user_exits,
                    user_group=group,
                    defaults=user_account_data
                )
                self.stdout.write(self.style.SUCCESS(f'admin user has been added'))














        

        # sample institution accounts
        institution_type = InstitutionType.objects.get(name="LPG Company")
        if institution_type:
            registerer = User.objects.filter(email='admin@my-gas.com').first()

            # institution data
            institution_data = {
                "institution_type":institution_type,
                "slug":"institution",
                "name":"Institution",
                "physical_location":"General Accident House",
                "phone_number":"0712123123",
                "email_address":"institution@institution.com",
                "registerer":registerer,
            }
            # admin account
            institution_user_data = {
                    'first_name': 'Test',
                    'last_name': 'LPG',
                    'is_superuser': True,
                    'email': 'lpg@my-gas.com',
                    'password': make_password('password'),
                }



            try:
                with transaction.atomic():
                    institution = Institution.objects.create(**institution_data)

                    # create institution group
                    group_name = f"{institution_data['slug']}-Admin"
                    test_group = Group(name=group_name)
                    test_group.save()
                    self.stdout.write(self.style.SUCCESS(f'test_group:{test_group}'))

                    # create user
                    user = User.objects.filter(email=institution_user_data["email"]).first()
                    if not user:
                        user = User.objects.create(**institution_user_data)
                        self.stdout.write(self.style.SUCCESS(f'user:{user}'))

                    # create user account
                    user_account_data = {
                        "user": user,
                        "user_group": test_group,
                        "institution": institution,
                        "is_active": True,
                        "user_account_type":2,
                    }

                    user_account = UserAccount.objects.create(**user_account_data)

            except Exception as e:
                self.stdout.write(self.style.SUCCESS(f'e:{e}'))
                print(f"e:{e}")


        self.stdout.write(self.style.SUCCESS(f'Test institution and instiitution data has bn deleted'))