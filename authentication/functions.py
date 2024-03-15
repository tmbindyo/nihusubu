import re
from django.core.mail import send_mail
from django.contrib.sites.models import Site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from django.contrib.auth.models import Group, Permission
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator

from authentication.models import User, Institution


def stripWhiteSpaceFromString(text: str) -> str:
    return re.sub(' ', '', text)

def cleanPhoneNumber(phoneNumber: str) -> str:
    """
    Function is responsible to check the format of a phoneNumber and ensure it matches the system criteria
    Args:
        phoneNumber: 07XXXXXX 7XXXXXXXX 2547XXXXXXX +2547XXXXXXX

    Returns: 2547XXXXXX

    """
    cleanNumber = stripWhiteSpaceFromString(phoneNumber)
    if '+' in cleanNumber:
        cleanNumber = phoneNumber[1:len(cleanNumber)]

    if cleanNumber[0:2] == '254':
        pass

    if cleanNumber[0] == '0':
        cleanNumber = f'254{cleanNumber[1:len(cleanNumber)]}'

    if len(cleanNumber) == 9:
        cleanNumber = f'254{cleanNumber}'

    return cleanNumber



def validate_email_or_phone(input_variable):
    # Check if the input matches the email format
    email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$"
    is_email = re.match(email_pattern, input_variable)

    # Check if the input matches the phone number format (assuming 10 digits)
    phone_pattern = r"^\d{10}$"
    is_phone = re.match(phone_pattern, input_variable)

    if is_email:
        return "email", is_email.group(0)
    elif is_phone:
        return "phone", is_phone.group(0)
    else:
        return None, None


def login_function():

    return True




def send_verification_email(email, user):
    # Send verification email
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))

    current_site = Site.objects.get_current()
    domain = current_site.domain

    # domain = get_current_site(request).domain
    verification_link = f"http://{domain}/verify/{uid}/{token}/"
    
    subject = "Verify Your Email"

    # message = render_to_string("verification_email_template.html", {"verification_link": verification_link})
    message = render_to_string("verification_email.html", {"user": user, "verification_link": verification_link})


    send_mail(subject, message, "noreply@example.com", [user.email])
    return True


def send_reset_email(email, user):
    # Send verification email
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))

    current_site = Site.objects.get_current()
    domain = current_site.domain

    # domain = get_current_site(request).domain
    password_reset_link = f"http://{domain}/password_resetword/reset/{uid}/{token}/"
    
    subject = "Reset Your Email"

    # message = render_to_string("verification_email_template.html", {"verification_link": verification_link})
    message = render_to_string("password_reset_email.html", {"user": user, "password_reset_link": password_reset_link})

    send_mail(subject, message, "noreply@example.com", [user.email])
    return True


def send_verification_sms(identifier):
    return True



def register_function(username, identifier, password):
    preferred_contact = None
    preferred_contact, validated_identifier = validate_email_or_phone(identifier)


    if preferred_contact == "email":
    # if "@" in identifier:
        # validation
        user, created = User.objects.get_or_create(email=identifier, defaults={"username": username, "password": password})
        if created:
            # Assuming identifier is an email address
            # Register the user using email
            send_verification_email(identifier, user)

            return {
                "data": None,
                "status": 200,
                "message": "User registered and verification email sent"
            }
        else:
            return {
                "data": None,
                "status": 409,
                "message": "Email already registered"
            }
    elif preferred_contact == "phone":
    
        if identifier.isdigit() and len(identifier) == 10:
            phone_number = cleanPhoneNumber(identifier)
            user, created = User.objects.get_or_create(phone_number=phone_number, defaults={"username": username, "password": password})
            if created:
                send_verification_sms(identifier, user)
                return {
                    "data": None,
                    "status": 200,
                    "message": "User registered and verification SMS sent"
                }
            else:
                return {
                    "data": None,
                    "status": 409,
                    "message": "Phone number already registered"
                }
        else:
            return {
                    "data": None,
                    "status": 400,
                    "message": "Invalid phone number"
                }
    else:
        return {
                    "data": None,
                    "status": 400,
                    "message": "Invalid input"
                }
    return True



def password_reset():

    # if request.method == "POST":

    send_reset_email()
    
    return render(request, "password_reset.html", {"message": "Reset email sent"})







# role functiions

# group functions






def createGroup(institution_id, group_name):

    
    pass




# group functions
def getGroups(institution_id):
    institution = Institution.objects.filter(id=institution_id).first()
    if not institution:
        return {
            "data": None,
            "status": 404,
            "message": "Institution not found."
        }
    else:
        reference = institution.reference

        institution_groups_data = []
        institution_groups = Group.objects.filter(name__icontains=reference)
        for institution_group in institution_groups:
            institution_group_permissions_data = []
            # Get all permissions associated with the group
            institution_group_permissions = institution_group.permissions.all()
            for institution_group_permission in institution_group_permissions:
                institution_group_permissions_data.append({
                    "id":institution_group_permission.id,
                    "name":institution_group_permission.name,
                    "content_type":institution_group_permission.content_type,
                    "codename":institution_group_permission.codename,
                })
            institution_groups_data.append({
                "name":institution_group.name,
                "Permissions":institution_group_permissions,
            })
        
        return {
                "data": institution_groups_data,
                "status": 200,
                "message": "Institution groups data."
            }


def getGroup(group_id):
    institution_group = Group.objects.filter(id=group_id).first()
    if not institution_group:
        return {
                "data": None,
                "status": 404,
                "message": "Group not found."
            }
    institution_group_permissions_data = []
    # Get all permissions associated with the group
    institution_group_permissions = institution_group.permissions.all()
    for institution_group_permission in institution_group_permissions:
        institution_group_permissions_data.append({
            "id":institution_group_permission.id,
            "name":institution_group_permission.name,
            "content_type":institution_group_permission.content_type,
            "codename":institution_group_permission.codename,
        })

    institution_group_data = {
        "name":institution_group.name,
        "Permissions":institution_group_permissions,
    }
    return {
            "data": institution_group_data,
            "status": 200,
            "message": "Institution group data."
        }


def addPermissionToGroup(group_id, permission_id):
    group = Group.objects.filter(id=group_id).first()
    if not group:
        return {
            "data": None,
            "status": 404,
            "message": "Group not found."
        }
    
    permission = Permission.objects.filter(id=permission_id).first()
    if not permission:
        return {
            "data": None,
            "status": 404,
            "message": "Permission not found."
        }
    
    group.permissions.add(permission)


def addUserToGroup(user_id, group_id):
    user = User.objects.filter(id=user_id).first()
    if not user:
        return {
            "data": None,
            "status": 404,
            "message": "User not found."
        }
    group = Group.objects.filter(id=group_id).first()
    if not user:
        return {
            "data": None,
            "status": 404,
            "message": "User not found."
        }
    user.groups.add(group)


