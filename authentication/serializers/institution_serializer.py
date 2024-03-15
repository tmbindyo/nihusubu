import re
from django.conf import settings
from rest_framework import serializers

from authentication.models import (
    InstitutionType,
    Institution,
    # Customer,
    # InstitutionCustomer,
    # Depot,

)

# This reference style is recommended for model files as opposed to
# django.contrib.auth.get_user_model. See:
# https://learndjango.com/tutorials/django-best-practices-referencing-user-model
User = settings.AUTH_USER_MODEL

class InstitutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institution
        fields = (
            'id',
            'institution_type',
            'slug',
            'name',
            'physical_location',
            'phone_number',
            'email_address',
            'registerer'
        )
        read_only_fields = ('id',)

    def validate_name(self, value):
        """
        Check that the name is not empty.
        """
        if not value.strip():
            raise serializers.ValidationError("Name cannot be empty.")
        return value

    def validate_institution_type(self, value):
        """
        Check that the institution_type exists.
        """
        if value:
            try:
                InstitutionType.objects.get(pk=value.pk)
            except InstitutionType.DoesNotExist:
                raise serializers.ValidationError("Institution type does not exist.")
        return value

    def validate_registerer(self, value):
        """
        Check that the registerer (User) exists.
        """
        if not value:
            raise serializers.ValidationError("Registerer is required.")
        # Assuming User is the model name for your user model
        try:
            User.objects.get(pk=value.pk)
        except User.DoesNotExist:
            raise serializers.ValidationError("Registerer user does not exist.")
        return value

    def validate_phone_number(self, value):
        """
        Validate phone number format.
        """
        # Remove any whitespace or special characters from the phone number
        cleaned_phone_number = re.sub(r'\D', '', value)

        # Validate the phone number format
        if not re.match(r'^((\+?254)|0)\d{9}$', cleaned_phone_number):
            raise serializers.ValidationError(
                "Phone number must be in one of the formats: 254701012345, 0701012345, +254701012345"
            )

        # If the number starts with 0, prepend with +254
        if cleaned_phone_number.startswith('0'):
            cleaned_phone_number = '+254' + cleaned_phone_number[1:]

        return cleaned_phone_number

    def validate(self, data):
        """
        Check uniqueness constraints and related record existence.
        """
        # Check uniqueness of the name
        if Institution.objects.filter(name=data['name']).exists():
            raise serializers.ValidationError("Name must be unique.")

        # Generate slug from name and check uniqueness
        if 'name' in data:
            institution_name = data['name']
            slug = institution_name.lower().replace(" ", "-")
            # Remove special characters
            slug = ''.join(char for char in slug if char.isalnum() or char == '-')
            data['slug'] = slug

            # Check if the generated slug is unique
            if Institution.objects.filter(slug=slug).exists():
                raise serializers.ValidationError("Slug must be unique.")

        return data
    


