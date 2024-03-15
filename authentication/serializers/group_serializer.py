from rest_framework import serializers
from django.contrib.auth.models import Group
from rest_framework.exceptions import ValidationError

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name']

    def validate_name(self, value):
        # Check if a group with the same name already exists
        existing_group = Group.objects.filter(name=value).first()

        if existing_group:
            # If the group exists, raise a validation error
            raise ValidationError('A group with this name already exists.')

        return value

    def create(self, validated_data):
        return Group.objects.create(**validated_data)