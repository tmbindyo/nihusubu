from django.db import models
from django.db.models.query import QuerySet
from guardian.shortcuts import get_objects_for_user

from core.utils import return_model_perms


class BasePermissionManager(models.Manager):
    """
    Base manager that handles querying only of objects that a user has 
    access to.
    """

    def get_user_objects(self, user, perms=None) -> QuerySet:
        """
        Query all objects that belong to a user.

        Parameters
        ---
        user: required
            User to check.
        perms: Iterable | str, optional
            Permissions to check.
            Defaults to all available model permissions.
        
        Usage
        ---
        `Model.objects.get_user_objects(user)`
        `Model.objects.get_user_objects(user, "model.perm")`
        `Model.objects.get_user_objects(user, ["model.perm", "model.other_perm"])`
        """

        from django.contrib.auth.models import Permission

        qs = super().get_queryset()

        if not perms:
            perms = return_model_perms(self.model)

        user_objs = get_objects_for_user(user=user, perms=perms, klass=qs)

        return user_objs


class SoftDeletionManager(models.Manager):
    """
    Manager for objects with the `deletion_marker` field.
    Should you specify a manager for a model, you will need to inherit from
    this class.
    """

    def get_queryset(self) -> QuerySet:
        return super().get_queryset().filter(deletion_marker=None)
