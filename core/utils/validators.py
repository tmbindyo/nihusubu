import phonenumbers
import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from phonenumbers import carrier, geocoder, timezone


def validate_phone_number(phone_number, country_code=None) -> dict:
    """
    Function that validates a single phone number.

    Parameters:
    ---
    phone_number : str, required
        The phone number to validate.
    country_code : str, optional
        The ISO country code to which the phone number belongs.
        Not necessary if the number includes the country code in the format of +xxx,
        but it is good practice to include it

    Returns:
    ---
    dict
        A dictionary (object) containing the keys:

        valid : bool
            Indicates whether the phone number is valid or not.
        message : str
            A message that can be raised or returned as the error message.
        details : dict
            Details of the phone number. Returns data only if the phone number is valid.

            formatted : str
                The phone number formatted to ISO standards.
            ph_timezone : list
                A list of timezones where in the phone number's region.
            ph_country : str
                The country to which the phone number belongs.
            ph_carrier : str
                The carrier (service provider) the phone number belongs to.
    """

    try:
        parsed = phonenumbers.parse(phone_number, country_code)
        is_valid = phonenumbers.is_valid_number(parsed)

        if is_valid:
            # Returned formatted number is in the format if +254xxxxxxxxx
            formatted = phonenumbers.format_number(
                parsed, phonenumbers.PhoneNumberFormat.E164
            )
            ph_timezone = list(timezone.time_zones_for_number(parsed))
            ph_country = geocoder.description_for_number(parsed, "en")
            ph_carrier = carrier.name_for_number(parsed, "en")

            return {
                "valid": True,
                "message": "Valid phone number provided.",
                "details": {
                    "formatted": formatted,
                    "timezone": ph_timezone,
                    "country": ph_country,
                    "carrier": ph_carrier,
                },
            }
        else:
            return {
                "valid": False,
                "message": "Invalid phone number provided.",
                "details": {},
            }

    except phonenumbers.phonenumberutil.NumberParseException:
        return {
            "valid": False,
            "message": "Invalid phone number provided.",
            "details": {},
        }


def phone_number_model_validator(value: str):
    """
    Function that validates a phone number, specifically adapted for use in
    database models.

    Parameters:
    ---
    value: str, required
        The phone number being validated.
    """

    _validate = validate_phone_number(value)

    if not _validate.get("valid"):
        raise ValidationError(
            _(
                "%(value)s is invalid. Please ensure it follows the E164 format."
            ),
            params={"value": value},
        )


def validate_email_address(email_address) -> dict:
    """
    Function that validates a single email address.

    Parameters:
    ---
    email_address : str, required
        The email address to validate.

    Returns:
    ---
    dict
        A dictionary (object) containing the keys:

        valid : bool
            Indicates whether the email address is valid or not.
        message : str
            A message that can be raised or returned as the error message.
    """

    if email_address is None:
        return {"valid": False, "message": "An empty email address is invalid."}

    else:
        # Using a regex expression to validate the pattern of the address
        match = re.match(
            "^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$",
            email_address,
        )

        if match is None:
            return {
                "valid": False,
                "message": "Invalid email address provided.",
            }
        else:
            return {"valid": True, "message": "Valid email address provided."}
