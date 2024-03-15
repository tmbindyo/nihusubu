import uuid
import hashlib
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.validators import EmailValidator
from django.contrib.auth.models import Permission
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import Group, GroupManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from pgcrypto.fields import (
    CharPGPSymmetricKeyField,
    EmailPGPSymmetricKeyField,
    TextPGPSymmetricKeyField,
)
from typing import Iterable

from core.mixins import (
    BasePermissionMixin,
    DeletionMarkerMixin,
    HistoricalDataMixin,
    TimestampMixin,
)
from core.utils import (
    phone_number_model_validator,
    assign_model_perms,
)
from authentication.managers import UserManager


class Region(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    translations = models.JSONField()
    wikiDataId = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class SubRegion(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    translations = models.JSONField()
    wikiDataId = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Timezone(models.Model):
    zoneName = models.CharField(max_length=100)
    gmtOffset = models.IntegerField()
    gmtOffsetName = models.CharField(max_length=50)
    abbreviation = models.CharField(max_length=50)
    tzName = models.CharField(max_length=100)

class Country(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    iso3 = models.CharField(max_length=20)
    iso2 = models.CharField(max_length=20)
    numeric_code = models.CharField(max_length=20)
    phone_code = models.CharField(max_length=20)
    capital = models.CharField(max_length=255)
    currency = models.CharField(max_length=20)
    currency_name = models.CharField(max_length=255)
    currency_symbol = models.CharField(max_length=50)
    tld = models.CharField(max_length=20)
    native = models.CharField(max_length=255, null=True)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    subregion = models.ForeignKey(SubRegion, on_delete=models.CASCADE, null=True)
    nationality = models.CharField(max_length=255)
    latitude = models.DecimalField(max_digits=10, decimal_places=8)
    longitude = models.DecimalField(max_digits=11, decimal_places=8)
    emoji = models.CharField(max_length=20)
    emojiU = models.CharField(max_length=20)
    translations = models.JSONField()
    timezone = models.ManyToManyField(Timezone)  # Many-to-many relationship with Timezone model

    def __str__(self):
        return self.name


class State(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    state_code = models.CharField(max_length=10)
    type = models.CharField(max_length=100, null=True, blank=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=8, null=True)
    longitude = models.DecimalField(max_digits=11, decimal_places=8, null=True)

    def __str__(self):
        return self.name


class City(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    latitude = models.DecimalField(max_digits=10, decimal_places=8)
    longitude = models.DecimalField(max_digits=11, decimal_places=8)
    wikiDataId = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.name
    

# Create your models here.
class InstitutionType(
    DeletionMarkerMixin,
    HistoricalDataMixin,
    TimestampMixin,
):
    """
    Contains details of institution types.
    """

    id = models.UUIDField(_("ID"), primary_key=True, default=uuid.uuid4)
    name = models.CharField(
        _("Institution Type"),
        max_length=70,
        blank=False,
        null=False,
        help_text=_("Institution Type")
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Institution Type"
        verbose_name_plural = "Institution Types"


class Institution(
    BasePermissionMixin,
    DeletionMarkerMixin,
    HistoricalDataMixin,
    TimestampMixin,
):
    """
    Contains details of insitutions.
    """

    id = models.UUIDField(_("ID"), primary_key=True, default=uuid.uuid4)
    institution_type = models.ForeignKey(
        InstitutionType,
        on_delete=models.PROTECT,
        blank=False,
        null=False,
        help_text=_("Type of institution."),
    )
    name = models.CharField(
        _("Institution Name"),
        max_length=255,
        blank=False,
        null=False,
        help_text=_("Name of institution."),
    )
    physical_address = models.CharField(
        _("Physical Address"),
        max_length=255,
        blank=True,
        null=True,
        help_text=_("Physical location of institution, such as building name, road name, etc."),
    )
    postal_address = models.CharField(
        _("Postal Address"),
        max_length=255,
        blank=True,
        null=True,
        help_text=_("Postal address of insitution."),
    )
    phone_number = models.CharField(
        _("Phone Number"),
        max_length=15,
        validators=[phone_number_model_validator],
        blank=True,
        null=True,
        help_text=_("Phone number of institution."),
    )
    email_address = models.CharField(
        _("Email Address"),
        max_length=255,
        blank=True,
        null=True,
        help_text=_("Email address of institution."),
    )
    website = models.CharField(
        _("Email Address"),
        max_length=255,
        blank=True,
        null=True,
        help_text=_("Website of institution."),
    )
    is_coordinating_institution = models.BooleanField(
        _("Coordinating Institution?"),
        default=False,
        help_text=_(
            "Indicates whether institution is a coordinator. "
            "Equivalent to superuser status."
        ),
    )
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    ## TODO: Add physical location data e.g. county

    class Meta:
        ordering = ["name"]
        verbose_name = "Institution"
        verbose_name_plural = "Institutions"

    @property
    def global_role(self):
        """
        Return the "basic" role associated with an institution.
        """

        group = self.group_set.first()

        qs = Role.objects.filter(pk=group.pk).first()

        return qs



class User(
    AbstractBaseUser,
    PermissionsMixin,
    DeletionMarkerMixin,
    HistoricalDataMixin,
    TimestampMixin
):
    """
    Contains system user details.
    """

    email_validator = EmailValidator()

    id = models.UUIDField(_("ID"), primary_key=True, default=uuid.uuid4)
    first_name = CharPGPSymmetricKeyField(
        _("First Name"),
        max_length=255,
        blank=False,
        null=False,
        help_text=_("First name of user.")
    )
    middle_name = CharPGPSymmetricKeyField(
        _("Middle Name"),
        max_length=255,
        blank=True,
        null=True,
        help_text=_("Middle name of user.")
    )
    last_name = CharPGPSymmetricKeyField(
        _("Last Name"),
        max_length=255,
        blank=False,
        null=False,
        help_text=_("Last name of user.")
    )
    email = EmailPGPSymmetricKeyField(
        _("Email"),
        unique=True,
        max_length=255,
        validators=[email_validator],
        error_messages={
            "unique": _("A user with the provided email already exists.")
        },
        help_text=_("Email address of user.")
    )
    phone_number = CharPGPSymmetricKeyField(
        _("Phone Number"),
        max_length=15,
        validators=[phone_number_model_validator],
        blank=False,
        null=False,
        help_text=_("Phone number of user.")
    )
    is_active = models.BooleanField(
        _("Is Active?"),
        default=False,
        help_text=_(
            "Indicates whether user is active. Determines if user can sign in."
        )
    )
    is_staff = models.BooleanField(
        _("Is Staff?"),
        default=False,
        help_text=_("Indicates whether user can sign in to admin site.")
    )

    groups = models.ManyToManyField(Group, related_name='accounts_user_groups')
    user_permissions = models.ManyToManyField(Permission, related_name='accounts_user_permissions')

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "phone_number"]

    class Meta:
        ordering = ["first_name", "last_name"]
        verbose_name = _("User")
        verbose_name = _("Users")

    def __str__(self) -> str:
        return f"User: {self.first_name}"

    @property
    def full_name(self):
        return (
            f"{self.first_name} {self.middle_name} {self.last_name}"
            if self.middle_name
            else f"{self.first_name} {self.last_name}"
        )

    @property
    def avatar(self) -> str:
        email_hash = hashlib.md5(self.email.encode("utf-8")).hexdigest()

        # Using Gravatar as the avatar provider
        # https://en.gravatar.com/
        # Another option one could consider: Boring Avatars
        # https://boringavatars.com/
        img_url = (
            f"https://www.gravatar.com/avatar/{email_hash}?d=identicon&s=250"
        )

        return img_url

    @property
    def roles(self):
        """
        Role(s) assigned to a user.
        """

        groups = self.groups.all()

        qs = Role.objects.filter(
            id__in=[group.id for group in groups],
            institution=None,
        ).all()

        return qs

    def assign_perms(self, assignee, perms : Iterable = None):
        """
        Method to assign all `User` permissions to an `assignee`, who is either
        a user or a role.

        Parameters
        ---
        assignee: User | Role, required
            The user or role to assign permissions.
        perms: Iterable, optional
            Permissions to assign.
            Defaults to all available model permissions.
        """

        assign_model_perms(self, assignee, self)


USER_ACCOUNT_TYPE = (
    (1, "Admin"),
    (2, "Institution"),
    (3, "Depot"),
)


class UserAccount(DeletionMarkerMixin, HistoricalDataMixin, TimestampMixin):
    id = models.UUIDField(_("ID"), primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True)
    institution = models.ForeignKey(Institution, on_delete=models.SET_NULL, null=True, blank=True)
    # depot = models.ForeignKey(Depot, on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    user_account_type = models.IntegerField(
        _("User Account Type"), choices=USER_ACCOUNT_TYPE, blank=False, null=True
    )
    # Add any other fields specific to the user profile

    def __str__(self):
        return f"{self.user.email} - {self.user_group.name}" if self.user_group else self.user.email
    

class InvalidResetAttempt(TimestampMixin):
    """
    Contains details of invalid password reset attempts.
    """

    id = models.UUIDField(_("ID"), primary_key=True, default=uuid.uuid4)
    email = EmailPGPSymmetricKeyField(
        _("Email"),
        max_length=255,
        blank=False,
        null=False,
        editable=False,
        help_text=_("Email address used in sign-in attempt.")
    )
    ## TODO: Log IP address?

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Invalid Password Reset Attempt"
        verbose_name_plural = "Invalid Password Reset Attempts"


class PasswordResetToken(TimestampMixin):
    """
    Contains details of password reset tokens.
    """

    id = models.UUIDField(_("ID"), primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        blank=False,
        null=False,
        editable=False,
        help_text=_("User that generated reset token.")
    )
    token = TextPGPSymmetricKeyField(
        _("Token"),
        blank=False,
        null=False,
        editable=False,
        help_text=_("Password reset token issued.")
    )
    expires_at = models.DateTimeField(
        _("Token Expires At"),
        blank=False,
        null=False,
        editable=False,
        help_text=_("Expiration date and time of token.")
    )
    used_at = models.DateTimeField(
        _("Token Used At"),
        blank=True,
        null=True,
        editable=False,
        help_text=_("Date and time when token was used.")
    )
    ## TODO: Log IP address?

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Password Reset Token"
        verbose_name_plural = "Password Reset Tokens"


## START OF `Role` ##
# Since the `Role` model defined below is a proxy model, it is not possible to
# add columns to the `Group` model in the traditional way of declaring
# a column. (HistoricalData works a bit differently.)
# This adds columns to the `Group` model.
# See: https://stackoverflow.com/questions/2181039/how-do-i-extend-the-django-group-model
# `institution`
if not hasattr(Group, "institution"):
    # Adding the `institution` field to allow more concise
    # sharing of object permissions.
    institution_field = models.ForeignKey(
        Institution,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        help_text=_("Institution associated with a role."),
    )
    institution_field.contribute_to_class(Group, "institution")

if not hasattr(Group, "is_active"):
    is_active_field = models.BooleanField(
        _("Is Active"),
        default=False,
        help_text=_("Whether the group is active or not."),
    )
    is_active_field.contribute_to_class(Group, "is_active")
    
# `created_at`
if not hasattr(Group, "created_at"):
    created_at_field = models.DateTimeField(
        _("Created At"),
        blank=True,
        null=True,
        editable=False,
        default=timezone.now,
        help_text=_("Date and time when record was created."),
    )
    created_at_field.contribute_to_class(Group, "created_at")

# `updated_at`
if not hasattr(Group, "updated_at"):
    updated_at_field = models.DateTimeField(
        _("Updated At"),
        blank=True,
        null=True,
        help_text=_("Date and time when record was last updated."),
    )
    updated_at_field.contribute_to_class(Group, "updated_at")

# `deletion_marker`
if not hasattr(Group, "deletion_marker"):
    deletion_marker_field = models.IntegerField(
        _("Deletion Marker"),
        blank=True,
        null=True,
        help_text=_("Soft-deletion marker.,"),
    )
    deletion_marker_field.contribute_to_class(Group, "deletion_marker")

# `deleted_at`
if not hasattr(Group, "deleted_at"):
    deleted_at_field = models.DateTimeField(
        _("Deleted At"),
        blank=True,
        null=True,
        help_text=_("Date and time when record was marked as deleted."),
    )
    deleted_at_field.contribute_to_class(Group, "deleted_at")

class Role(Group, HistoricalDataMixin):
    """
    Proxy model that inherits from `django.contrib.auth.models.Group`.
    As a proxy model, no table called `accounts_roles` exists. Rather, the
    `auth_group` table is populated.
    This approach allows us to use Django's built-in permissions management
    tooling.

    Fields available are:
    - `id`
    - `name`
    - `permissions`
    - `institution`
    - `created_at`
    - `updated_at`
    - `deletion_marker`
    - `deleted_at`
    """

    objects = GroupManager()

    class Meta:
        proxy = True
        ordering = ["name"]
        verbose_name = "Role"
        verbose_name_plural = "Roles"

## END OF `Role` ##
        





