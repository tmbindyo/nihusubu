from django.contrib.auth.base_user import BaseUserManager
from django.db import transaction
from guardian.shortcuts import assign_perm

from core.mixins import BasePermissionManager, SoftDeletionManager


class UserManager(BaseUserManager, BasePermissionManager, SoftDeletionManager):
    @transaction.atomic
    def _create_user(self, email, password, **extra_fields):
        extra_fields.setdefault("is_active", False)
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        # Assign the user the permission to change their record.
        assign_perm("accounts.change_user", user)

        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        ## TODO: Send out verification email upon creation of superuser.

        return self._create_user(email, password, **extra_fields)
