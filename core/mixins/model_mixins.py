from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from guardian.shortcuts import get_users_with_perms
from simple_history.models import HistoricalRecords

from .manager_mixins import BasePermissionManager, SoftDeletionManager


class BasePermissionMixin(models.Model):
    """
    An abstract model that handles the querying only of objects that a user
    has access to.
    """

    objects = BasePermissionManager()

    class Meta:
        abstract = True

    @property
    def accessible_by(self):
        """
        Return users with any assigned object permissions.
        """

        return get_users_with_perms(self)


class DeletionMarkerMixin(models.Model):
    """
    An abstract model that contains the fields:
    - `deletion_marker`
    - `deleted_at`
    """

    deletion_marker = models.IntegerField(
        _("Deletion Marker"),
        blank=True,
        null=True,
        help_text=_("Soft-deletion marker."),
    )
    deleted_at = models.DateTimeField(
        _("Deleted At"),
        blank=True,
        null=True,
        help_text=_("Date and time when record was marked as deleted."),
    )

    objects = SoftDeletionManager()

    class Meta:
        abstract = True

    def delete(self):
        self.deletion_marker = 1
        self.deleted_at = timezone.now()

        if self.history:
            self._change_reason = "Deleted"

            ## TODO: Look into overriding the default behaviour of simple history.
            ## Default operation is ~ (Change). Find a way to manually set it to delete.
            # self._type = "-"

        self.save()


class HistoricalDataMixin(models.Model):
    """
    An abstract model that adds the tracking of changes to an instance.
    Contains the `history` field.
    """

    # Keeps track of changes to a record.
    # `inherit=True`` is used to allow the re-use of this mixin.
    # https://django-simple-history.readthedocs.io/en/latest/historical_model.html#allow-tracking-to-be-inherited
    history = HistoricalRecords(inherit=True)

    class Meta:
        abstract = True


class TimestampMixin(models.Model):
    """
    An abstract model that contains the fields:
    - `created_at`
    - `updated_at`
    """

    created_at = models.DateTimeField(
        _("Created At"),
        blank=True,
        null=True,
        editable=False,
        default=timezone.now,
        help_text=_("Date and time when record was created."),
    )
    updated_at = models.DateTimeField(
        _("Updated At"),
        blank=True,
        null=True,
        auto_now=True,
        help_text=_("Date and time when record was last updated."),
    )

    class Meta:
        abstract = True
