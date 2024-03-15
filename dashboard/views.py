import logging
from decimal import Decimal
from datetime import datetime
from django.conf import settings
from django.urls import reverse
from django.db import transaction
from rest_framework import status
from django.contrib import messages
from django.http import HttpResponse
from django.utils.http import urlencode
from django.http import HttpResponseRedirect
from django.utils.encoding import force_bytes
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.db.models import Prefetch, Count, Q
from django.contrib.auth.models import Permission
from django.template import loader, RequestContext
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from authentication.functions import login_function
from django.contrib.auth.hashers import make_password
from authentication.serializers import GroupSerializer
from django.views.decorators.csrf import csrf_protect
from django.core.mail import BadHeaderError, send_mail
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.tokens import default_token_generator
from dashboard.functions import get_user_accounts, get_active_user_account
from authentication.models import User, Group, UserAccount, Institution, InstitutionType
# from institution.serializers import CustomerSerializer, InstitutionCustomerSerializer
# from cylinders.serializers import CylinderSerializer, CylinderSaleSerializer, CylinderReturnSerializer, CylinderCheckSerializer, CylinderTransferSerializer, CylinderRefillSerializer, CylindeReturnSerializer
from notifications.tasks import notify_users_through_sms

from core.models import Status
# from institution.models import , Customer, InstitutionCustomer, Depot, LoyaltyPoints
# from cylinders.models import Cylinder, CylinderSizes, CylinderSale, CylinderRefill, CylinderReturn, CylinderCheck

logger = logging.getLogger('dashboard-logger')



def page_not_found(request, exception):
    logger.info(f"PAGE NOT FOUND: {request}")
    response = render(request, '404.html', context=RequestContext(request))
    response.status_code = 404
    return response


def server_error(request):
    logger.info(f"SERVER ERROR OCCURRED: {request}")
    # response = render(request,
    #                   'base_templates/500.html'
    #                   )
    # response.status_code = 500
    #
    # return response
    return redirect('/')

def permission_denied(request, exception):
    logger.info(f"PERMISSION DENIED: {request}")
    response = render(request,
                      'base_templates/403.html'
                      )
    response.status_code = 403

    return redirect('/')



def login_view(request):
  if request.method == "POST":
      email = request.POST.get('email')
      password = request.POST.get('password')
      keep_me_logged_in = request.POST.get('keep_me_logged_in')

      if not email:
          messages.error(request, 'Email is required.')
          return redirect('dashboard-login')

      if not User.objects.filter(email=email).exists():
          messages.error(request, 'No user with this email exists.')
          return redirect('dashboard-login')

      is_user = authenticate(request, email=email, password=password)
      if is_user:
          login(request, is_user)

          # TODO add accounts page
          # redirect user to accoounts sellection page if account has mulltiple accounts or redirect to onlly existing account
          user_account_count = UserAccount.objects.filter(user=is_user).count()
          is_active = get_active_user_account(is_user)
          if is_active:
            #  reedirect to activ account
            if is_active['is_admin'] == True:
              return redirect('dashboard-admin-index')
            else:
              return redirect('dashboard-institution-home')
          else:
            return redirect('dashboard-user-accounts')
      else:
         messages.success(request, "User sucesfullly signed in.")
         return redirect('dashboard-login')
  else:
      context = {}
      return render(request, 'auth/login.html', context)
  



def forgot_password_view(request):
    if request.method == "POST":
      domain = request.headers['Host']
      email = request.POST.get('email')

      if not email:
          messages.error(request, 'Email is required.')
          return redirect('dashboard-forgot-password')
      
      if not User.objects.filter(email=email).exists():
          messages.error(request, 'No user with this email exists.')
          return redirect('dashboard-forgot-password')
      
      associated_users = User.objects.filter(Q(email=email))
      if associated_users.exists():
         for user in associated_users:
            subject = "Password Reset Requested"
            email_template_name = "auth/password_reset_email.txt"
            c = {
                "email": user.email,
                'domain': domain,
                'site_name': 'Interface',
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "user": user,
                'token': default_token_generator.make_token(user),
                'protocol': 'http',
            }
            email = render_to_string(email_template_name, c)
            try:
              send_mail(subject, email, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)
            except BadHeaderError:
              return HttpResponse('Invalid header found.')
          
            successfull_message = "We've emailed you instructions for setting your password. You should receive the email shortly!"
            messages.success(request, successfull_message)
            return redirect('dashboard-forgot-password-done')
    else:
      context = {}
      return render(request, 'auth/forgot_password.html', context)
   

def forgot_password_done_view(request, ref):
    context = {}
    return render(request, 'auth/password_reset_done.html', context)

def password_reset_confirm_view(request, ):
    context = {}
    return render(request, 'auth/password_reset_confirm.html', context)

def password_reset_done_view(request):
    context = {}
    return render(request, 'auth/password_reset_done.html', context)


def logout_view(request):
    logout(request)
    return redirect('dashboard-login') 


@login_required
def dashboard_home(request):
   return render("Home")


@login_required
def dashboard_user_accounts(request):
  # Get the logged-in user (if any)
  logged_in_user = request.user
  # Create a context dictionary with the user details
  user_account_data = get_user_accounts(logged_in_user)
  context = {
      'user': logged_in_user,
      'user_account_data':user_account_data,
  }
  return render(request, 'auth/user_accounts.html', context)


@login_required
def dashboard_user_account(request, account_id):
  logged_in_user = request.user
  # set all accounts to inactive
  user_accoouts = UserAccount.objects.filter(user=logged_in_user).filter(is_active=True)
  if user_accoouts:
    user_accoouts.update(is_active=False)
  user_account = UserAccount.objects.filter(user=logged_in_user).filter(id=account_id).first()
  user_account.is_active=True
  user_account.save()

  user_account_true = UserAccount.objects.filter(user=logged_in_user).filter(is_active=True).first()

  if user_account.user_account_type == 1:
     return redirect('dashboard-admin-index')
  elif user_account.user_account_type == 2:
     return redirect('dashboard-institution-home')
  elif user_account.user_account_type == 3:
     return redirect('dashboard-depot-home')
  else:
    return redirect('dashboard-depot-home')   




   
   

@login_required
def admin_dashboard(request):
  # Get the logged-in user (if any)
  logged_in_user = request.user
  # Create a context dictionary with the user details
  user_account_data = get_user_accounts(logged_in_user)
  active_user_account_data = get_active_user_account(logged_in_user)
  if not active_user_account_data:
     return redirect('dashboard-user-accounts')
  # redirect if active account isn't an admin
  if active_user_account_data['is_admin'] == False:
    return redirect('dashboard-user-accounts')
  

  context = {
      'user': logged_in_user,
      'user_account_data':user_account_data,
      'active_user_account_data':active_user_account_data,
      # Add other data you want to pass to the template here
  }
  return render(request, 'dashboard/dashboards/dashboard.html', context)

@login_required
def admin_dashboard_analytics(request):
  # template = loader.get_template('base.html')
  template = loader.get_template('dashboard/dashboards/dashboard_analytics.html')
  return HttpResponse(template.render())

@login_required
def admin_dashboard_commerce_1(request):
  # template = loader.get_template('base.html')
  template = loader.get_template('dashboard/dashboards/dashboard_commerce_1.html')
  return HttpResponse(template.render())

@login_required
def admin_dashboard_commerce_2(request):
  # template = loader.get_template('base.html')
  template = loader.get_template('dashboard/dashboards/dashboard_commerce_2.html')
  return HttpResponse(template.render())

@login_required
def admin_dashboard_sales(request):
  # template = loader.get_template('base.html')
  template = loader.get_template('dashboard/dashboards/dashboard_sales.html')
  return HttpResponse(template.render())

@login_required
def admin_dashboard_minimal_1(request):
  # template = loader.get_template('base.html')
  template = loader.get_template('dashboard/dashboards/dashboard_minimal_1.html')
  return HttpResponse(template.render())

@login_required
def admin_dashboard_minimal_2(request):
  # template = loader.get_template('base.html')
  template = loader.get_template('dashboard/dashboards/dashboard_minimal_2.html')
  return HttpResponse(template.render())

@login_required
def admin_dashboard_crm(request):
  # template = loader.get_template('base.html')
  template = loader.get_template('dashboard/dashboards/dashboard_crm.html')
  return HttpResponse(template.render())




@login_required
def admin_institutions(request):
  # Get the logged-in user (if any)
  logged_in_user = request.user

  # accoount access
  user_account_data = get_user_accounts(logged_in_user)
  active_user_account_data = get_active_user_account(logged_in_user)
  if not active_user_account_data:
     return redirect('dashboard-user-accounts')
  # redirect if active account isn't an admin
  if active_user_account_data['is_admin'] == False:
    return redirect('dashboard-user-accounts')
  
  # get institution types
  institution_types_data = []
  institution_data = []
  institution_types = InstitutionType.objects.all()
  institutions = Institution.objects.all()
  for institution in institutions:
     institution_data.append({
        "id":institution.id,
        "name":institution.name,
        "slug":institution.slug,
        "physical_location":institution.physical_location,
        "phone_number":institution.phone_number,
        "email_address":institution.email_address,
        "institution_type":{
           "id":institution.institution_type.id,
            "name":institution.institution_type.name,
        },
     })

  for institution_type in institution_types:
     institution_types_data.append({
        "id":institution_type.id,
        "name":institution_type.name,
     })
  # Create a context dictionary with the user details
     
  context = {
      'user': logged_in_user,
      'institution_types':institution_types_data,
      'institutions':institution_data,
      # Add other data you want to pass to the template here
  }
  return render(request, 'dashboard/institutions.html', context)





@login_required
def admin_add_institution(request):
  # Get the logged-in user (if any)
  logged_in_user = request.user
  # accoount access
  user_account_data = get_user_accounts(logged_in_user)
  active_user_account_data = get_active_user_account(logged_in_user)
  if not active_user_account_data:
     return redirect('dashboard-user-accounts')
  # redirect if active account isn't an admin
  if active_user_account_data['is_admin'] == False:
    return redirect('dashboard-user-accounts')
  
  if request.method == "POST":
    logger.info(f"request {request}")

    # institution iinformation
    institution_name = request.POST.get('institution_name')
    institution_type_id = request.POST.get('institution_type')
    phone_number = request.POST.get('phone_number')
    email_address = request.POST.get('email_address')
    physical_location = request.POST.get('physical_location')

    # institution admin information
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    admin_email = request.POST.get('admin_email')
    admin_phone_number = request.POST.get('admin_phone_number')

    # save iinstitution record
    # generate institution slug, used for th group name
    slug = institution_name.lower()
    slug = slug.replace(" ","-")

    institution_type = InstitutionType.objects.get(id=institution_type_id)

    # institution name
    if Institution.objects.filter(name=institution_name).exists() or Depot.objects.filter(name=institution_name).exists():
          messages.error(request, 'An institution with this name exists.')
          print(messages)
          # return messages
          return redirect('dashboard-admin-institutions')
    
    institution_data = {
      "slug":slug,
      "institution_type":institution_type,
      "name":institution_name,
      "phone_number":phone_number,
      "email_address":email_address,
      "physical_location":physical_location,
      "registerer":logged_in_user,
    }
    
    user_data = {
          'first_name': first_name,
          'last_name': last_name,
          'is_superuser': False,
          'email': admin_email,
          'phone_number': admin_phone_number,
          'password': make_password('password'),
    }

    try:
      with transaction.atomic():
        # create institution
        institution = Institution.objects.create(**institution_data)

        # create institution group
        # group_name: [institution_name]-[group/role name] i.e rubis-admin
        group_name = f"{slug}-Admin"
        group = Group(name=group_name)
        group.save()

        # get content types to assign peermissions
        model_classes = [Group, Cylinder, CylinderSizes, CylinderSale, CylinderRefill, CylinderReturn, CylinderCheck, Customer, Depot, LoyaltyPoints]
        permissions = [permission for model_class in model_classes for permission in Permission.objects.filter(content_type=ContentType.objects.get_for_model(model_class))]
        group.permissions.add(*permissions)

        # create user if not exists
        user, created = User.objects.get_or_create(email=admin_email, defaults=user_data)

        # create user account
        user_account_data = {
           "user":user,
           "user_group":group,
           "institution":institution,
           "is_active":True,
           "user_account_type":2,
        }
        user_account = UserAccount.objects.create(**user_account_data)
        
        # send messages

        # Check if the user was just created
        if created:
            # New user, send a welcome message
            welcome_message = f"Welcome to {institution.name}! 🌟 Discover a world of convenience and quality service with us. Your safety and satisfaction are our top priorities. Explore our offerings and feel free to reach out for any assistance. Enjoy your experience!"
            notify_users_through_sms(welcome_message, [user.phone_number])

            # Additional message to invite the new user to the organization
            invite_message = f"You've been invited to join {institution.name}. Click [link_to_invite_page] to accept the invitation and start using our services."
            notify_users_through_sms(invite_message, [user.phone_number])
        else:
            # Existing user, inform about the organization
            existing_user_message = f"Welcome back to {institution.name}! 🌟 Explore the latest updates and offerings. Feel free to reach out if you have any questions or need assistance. Enjoy your experience!"
            notify_users_through_sms(existing_user_message, [user.phone_number])

        # email notification to verify
      
    except Exception as e:
       transaction.set_rollback(True)
       logger.debug(f"e:{e}")

    
    return redirect('dashboard-admin-institution', institution.id)


@login_required
def admin_institution(request, institution_id):
  institution = Institution.objects.get(id=institution_id)

  institution_types_data = []
  institution_types = InstitutionType.objects.all()
  for institution_type in institution_types:
     institution_types_data.append({
        "id":institution_type.id,
        "name":institution_type.name,
     })

  logged_in_user = request.user

  # get institution depots
  depots = Depot.objects.filter(owner=institution)


  context = {
    'user': logged_in_user,
    'institution':institution,
    'institution_types':institution_types_data,
    'depots':depots,
  }
   
  return render(request, 'dashboard/institution.html', context)


@login_required
def admin_update_institution(request, institution_id):
   pass
   

@login_required
def admin_settings():
  pass











# institution dashboard views
@login_required
def institution_home(request):
  # Get the logged-in user (if any)
  logged_in_user = request.user
  
  # Create a context dictionary with the user details
  user_account_data = get_user_accounts(logged_in_user)
  active_user_account_data = get_active_user_account(logged_in_user)
  if not active_user_account_data:
     return redirect('dashboard-user-accounts')
  # redirect if active account isn't institution
  if active_user_account_data['is_admin'] == True:
    return redirect('dashboard-user-accounts')
  
  context = {
      'user': logged_in_user,
      'user_account_data': user_account_data,
      'active_user_account_data': active_user_account_data,
  }
  return render(request, 'institution/index.html', context)


@login_required
def institution_index(request):
  # Get the logged-in user (if any)
  logged_in_user = request.user
  # Create a context dictionary with the user details
  user_account_data = get_user_accounts(logged_in_user)
  active_user_account_data = get_active_user_account(logged_in_user)
  if active_user_account_data['is_admin'] == True:
    return redirect('dashboard-user-accounts')


  context = {
      'user': logged_in_user,
      'user_account_data': user_account_data,
      'active_user_account_data': active_user_account_data,
  }

  return render(request, 'institution/index.html', context)



@login_required
def institution_cylinders(request):
  # Get the logged-in user (if any)
  logged_in_user = request.user
  # Create a context dictionary with the user details
  user_account_data = get_user_accounts(logged_in_user)
  active_user_account_data = get_active_user_account(logged_in_user)
  if not active_user_account_data:
     return redirect('dashboard-user-accounts')
  # redirect if active account isn't institution
  if active_user_account_data['is_admin'] == True:
    return redirect('dashboard-user-accounts')

  # get institution 
  institution = get_object_or_404(Institution, slug=active_user_account_data['institution_slug'])
  # get institution cylinders
  cylinders = Cylinder.objects.filter(owner=institution)
  # get cylinder sizes
  cylinder_sizes = CylinderSizes.objects.all()
  # get cylinder statuses
  statuses = Status.objects.all()
  # get institution depots
  institution_depots = Depot.objects.filter(owner=institution)
  # get institution customers
  institution_customers = InstitutionCustomer.objects.filter(is_institution=True).filter(institution=institution)
  # get institution depots
  depots = Depot.objects.filter(owner=institution)

  context = {
     "user":logged_in_user,
     "depots":depots,
     "statuses":statuses,
     "cylinders":cylinders,
     "cylinder_sizes":cylinder_sizes,
     "user_account_data":user_account_data,
     "institution_depots":institution_depots,
     "institution_customers":institution_customers,
     "active_user_account_data":active_user_account_data,
     }
  return render(request, 'institution/cylinders.html', context)



@login_required
@csrf_protect
def institution_add_cylinder(request):
  # Get the logged-in user (if any)
  logged_in_user = request.user
  active_user_account_data = get_active_user_account(logged_in_user)
  if request.method == "POST":
    logger.info(f"request {request}")

    # Extract the 'purchase_date' from the request and convert the format
    raw_purchase_date = request.POST.get('purchase_date')
    parsed_purchase_date = datetime.strptime(raw_purchase_date, '%m/%d/%Y').strftime('%Y-%m-%d')
    # Extract the 'last_inspection' from the request and convert the format
    raw_last_inspection = request.POST.get('last_inspection')
    parsed_last_inspection = datetime.strptime(raw_last_inspection, '%m/%d/%Y').strftime('%Y-%m-%d')
    # Extract the 'next_inspection' from the request and convert the format
    raw_next_inspection = request.POST.get('next_inspection')
    parsed_next_inspection = datetime.strptime(raw_next_inspection, '%m/%d/%Y').strftime('%Y-%m-%d')

    raw_purchase_price = request.POST.get('purchase_price')
    parsed_purchase_price = Decimal(raw_purchase_price) if raw_purchase_price else None

    # get institution 
    institution = get_object_or_404(Institution, slug=active_user_account_data['institution_slug'])


    data = {
      'serial_number':request.POST.get('serial_number'),
      'size':request.POST.get('cylinder_size'),
      'purchase_date':parsed_purchase_date,
      'purchase_price':parsed_purchase_price,
      'last_inspection_date':parsed_last_inspection,
      'next_inspection_due_date':parsed_next_inspection,
      'status':request.POST.get('status'),
      'condition':request.POST.get('condition'),
      'notes':request.POST.get('notes'),
      'registerer':logged_in_user.id,
      'owner':institution.id,
    }

    serializer = CylinderSerializer(data=data)
    if serializer.is_valid():
      cylinder_instance = serializer.save()
      # Redirect on success
      messages.success(request, 'Cylinder added successfully!')
      return redirect('dashboard-institution-cylinder', cylinder_id=cylinder_instance.id)
    else:
      # Return validation errors if the data is not valid
      messages.error(request, 'Error adding the cylinder. Please check the form.')
      
      
      # get institution 
      institution = Institution.objects.filter(slug=active_user_account_data['institution_slug']).first()
      # get institution cylinders
      cylinders = Cylinder.objects.filter(owner=institution)
      # get cylinder sizes
      cylinder_sizes = CylinderSizes.objects.all()
      # get cylinder statuses
      statuses = Status.objects.all()
      context = {
        "user":logged_in_user,
        "statuses":statuses,
        "cylinders":cylinders,
        "cylinder_sizes":cylinder_sizes,
        "active_user_account_data":active_user_account_data,
        "errors":serializer.errors,
        "form_data":data,
        }
      return render(request, 'institution/cylinders.html', context, status=status.HTTP_400_BAD_REQUEST)


@login_required
def institution_view_cylinder(request, cylinder_id):
  # Get the logged-in user (if any)
  logged_in_user = request.user
  # Create a context dictionary with the user details
  user_account_data = get_user_accounts(logged_in_user)
  active_user_account_data = get_active_user_account(logged_in_user)
  if not active_user_account_data:
     return redirect('dashboard-user-accounts')
  # redirect if active account isn't institution
  if active_user_account_data['is_admin'] == True:
    return redirect('dashboard-user-accounts')

  # get institution 
  institution = get_object_or_404(Institution, slug=active_user_account_data['institution_slug'])
  # get institution cylinders
  cylinder = Cylinder.objects.filter(owner=institution).filter(id=cylinder_id).first()
  cylinder = get_object_or_404(Cylinder, id=cylinder_id)
  # get institution depots
  depots = Depot.objects.filter(owner=institution)
  # get institution depots
  cylinders = Cylinder.objects.filter(owner=institution)
        
  # get cylinder sizes
  cylinder_sizes = CylinderSizes.objects.all()
  # get cylinder statuses
  statuses = Status.objects.all()
  context = {
     "depots":depots,
     "user":logged_in_user,
     "statuses":statuses,
     "cylinders":cylinders,
     "cylinder":cylinder,
     "cylinder_sizes":cylinder_sizes,
     "user_account_data":user_account_data,
     "active_user_account_data":active_user_account_data,
     }

  return render(request, 'institution/cylinder.html', context)


@login_required
@csrf_protect
def institution_update_cylinder(request, cylinder_id):
  # Get the logged-in user (if any)
  logged_in_user = request.user
  # Create a context dictionary with the user details
  user_account_data = get_user_accounts(logged_in_user)
  active_user_account_data = get_active_user_account(logged_in_user)
  if request.method == "POST":

    try:
        cylinder_instance = Cylinder.objects.get(pk=cylinder_id)
    except Cylinder.DoesNotExist:
        return Response({"error": "Cylinder not found"}, status=status.HTTP_404_NOT_FOUND)

    # Extract the 'purchase_date' from the request and convert the format
    raw_purchase_date = request.POST.get('purchase_date')
    parsed_purchase_date = datetime.strptime(raw_purchase_date, '%m/%d/%Y').strftime('%Y-%m-%d')
    # Extract the 'last_inspection' from the request and convert the format
    raw_last_inspection = request.POST.get('last_inspection')
    parsed_last_inspection = datetime.strptime(raw_last_inspection, '%m/%d/%Y').strftime('%Y-%m-%d')
    # Extract the 'next_inspection' from the request and convert the format
    raw_next_inspection = request.POST.get('next_inspection')
    parsed_next_inspection = datetime.strptime(raw_next_inspection, '%m/%d/%Y').strftime('%Y-%m-%d')

    raw_purchase_price = request.POST.get('purchase_price')
    parsed_purchase_price = Decimal(raw_purchase_price) if raw_purchase_price else None
    
    data = {
      'serial_number':request.POST.get('serial_number'),
      'size':request.POST.get('cylinder_size'),
      'purchase_date':parsed_purchase_date,
      'purchase_price':parsed_purchase_price,
      'last_inspection_date':parsed_last_inspection,
      'next_inspection_due_date':parsed_next_inspection,
      'status':request.POST.get('status'),
      'condition':request.POST.get('condition'),
      'notes':request.POST.get('notes'),
      # 'registerer':logged_in_user.id,
      # 'owner':institution.id,
    }

    # validation
    # Instantiate the serializer with the existing instance
    serializer = CylinderSerializer(cylinder_instance, data=data)
    # Validate the data
    if serializer.is_valid():
        # Save the updated data
        cylinder_instance = serializer.save()
        messages.success(request, 'Cylinder updated successfully!')
        return redirect('dashboard-institution-cylinder', cylinder_id=cylinder_instance.id)
    else:
      # Return validation errors if the data is not valid
      
      
      # get cylinder sizes
      cylinder_sizes = CylinderSizes.objects.all()
      # get cylinder statuses
      statuses = Status.objects.all()
      context = {
        "user":logged_in_user,
        "statuses":statuses,
        "cylinder":cylinder_instance,
        "cylinder_sizes":cylinder_sizes,
        "user_account_data":user_account_data,
        "active_user_account_data":active_user_account_data,
        "errors":serializer.errors,
        }

      return render(request, 'institution/cylinder.html', context)
    


@login_required
@csrf_protect
def institution_cylinder_add_check(request, cylinder_id):
  # Get the logged-in user (if any)
  logged_in_user = request.user
  # Create a context dictionary with the user details
  user_account_data = get_user_accounts(logged_in_user)
  active_user_account_data = get_active_user_account(logged_in_user)
  if request.method == "POST":
    return redirect('dashboard-institution-cylinder', cylinder_id)


@login_required
@csrf_protect
def institution_cylinder_add_exchange(request):
  # Get the logged-in user (if any)
  logged_in_user = request.user
  # Create a context dictionary with the user details
  user_account_data = get_user_accounts(logged_in_user)
  active_user_account_data = get_active_user_account(logged_in_user)
  if request.method == "POST":
     
    return redirect('dashboard-institution-cylinder', cylinder_id)


@login_required
@csrf_protect
def institution_cylinder_add_inspection(request, cylinder_id):
  # Get the logged-in user (if any)
  logged_in_user = request.user
  # Create a context dictionary with the user details
  user_account_data = get_user_accounts(logged_in_user)
  active_user_account_data = get_active_user_account(logged_in_user)
  if request.method == "POST":
    return redirect('dashboard-institution-cylinder', cylinder_id)

@login_required
@csrf_protect
def institution_cylinder_add_refill(request):
  # Get the logged-in user (if any)
  logged_in_user = request.user
  # Create a context dictionary with the user details
  user_account_data = get_user_accounts(logged_in_user)
  active_user_account_data = get_active_user_account(logged_in_user)
  if request.method == "POST":

    return redirect('dashboard-institution-cylinder', 1)

@login_required
@csrf_protect
def institution_cylinder_add_sale(request):
  # Get the logged-in user (if any)
  logged_in_user = request.user
  # Create a context dictionary with the user details
  user_account_data = get_user_accounts(logged_in_user)
  active_user_account_data = get_active_user_account(logged_in_user)
  if request.method == "POST":

    # get institution 
    institution = get_object_or_404(Institution, slug=active_user_account_data['institution_slug'])

    # cast poost parameeters
    raw_date = request.POST.get('date')
    parsed_date = datetime.strptime(raw_date, '%m/%d/%Y').strftime('%Y-%m-%d')

    # customer exists
    is_existing_customer = request.POST.get('is_existing_customer')

    # new depot customer information
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    phone_number = request.POST.get('phone_number')

    customer_id = request.POST.get('customer')

    customer_data = {
       "first_name":first_name,
       "last_name":first_name,
       "phone_number":first_name,
    }

    form_data = {
        'sale_date':parsed_date,
        'depot':request.POST.get('depot'),
        'cylinder_id':request.POST.get('cylinder_id'),
        'is_existing_customer':is_existing_customer,
        'customer':customer_id,
        'first_name':first_name,
        'last_name':last_name,
        'phone_number':phone_number,
      }
    

    try:
      with transaction.atomic():

        # if not user, create
        if is_existing_customer == 'on':
          institution_customer = InstitutionCustomer.objects.filter(id=customer_id).first()
          customer = institution_customer.customer
          if not institution_customer:
            # Return validation errors if the data is not valid
            messages.error(request, 'Error adding the cylinder sale. Please check the form.')
        else:
          # create customer
          customer = Customer.objects.filter(phone_number=phone_number).first()
          if not customer: 
            cusotmer_serializer = CustomerSerializer(data=customer_data)
            if not cusotmer_serializer:
               messages.error(request, 'Error adding the cylinder sale. Please check the form.')

          institution_customer_data = {
              "is_institution":True,
              "institution":institution,
              "customer":institution,
          }
          institution_customer = InstitutionCustomerSerializer(data=institution_customer_data)

        data = {
          'cylinder_id':request.POST.get('cylinder_id'),
          'sale_date':parsed_date,
          'depot':request.POST.get('depot'),
          'customer':customer.id,
          'registerer':logged_in_user.id,
          'is_existing_customer':is_existing_customer,
          'customer':institution_customer,
        }

        serializer = CylinderSaleSerializer(data=data)
        if serializer.is_valid():
          cylinder_sale_instance = serializer.save()
          # Redirect on success
          messages.success(request, 'Cylinder Sale added successfully!')
          previous_page = request.META.get('HTTP_REFERER')  # Get the URL of the previous page
          return HttpResponseRedirect(previous_page)
        else:
          # Return validation errors if the data is not valid
          messages.error(request, 'Error adding the cylinder sale. Please check the form.')
          error_query_params = urlencode({'errors': serializer.errors, 'form_data':form_data})
          previous_page = request.META.get('HTTP_REFERER')  # Get the URL of the previous page
          redirect_url = f"{previous_page}?{error_query_params}"
          return HttpResponseRedirect(redirect_url)
        
    except Exception as e:
        print(f"e:{e}")
        logger.debug(f"e:{e}")
      
    return redirect('dashboard-institution-cylinders', )


def institution_cylinder_add_sale_cylinder(request, cylinder_id):
    # Get the logged-in user (if any)
    logged_in_user = request.user

    # Create a context dictionary with the user details
    user_account_data = get_user_accounts(logged_in_user)
    active_user_account_data = get_active_user_account(logged_in_user)

    if request.method == "POST":
      # get institution
      institution = get_object_or_404(Institution, slug=active_user_account_data['institution_slug'])

      # cast post parameters
      raw_date = request.POST.get('date')
      parsed_date = datetime.strptime(raw_date, '%m/%d/%Y').strftime('%Y-%m-%d')

      # customer exists
      is_existing_customer = request.POST.get('is_existing_customer')

      # new depot customer information
      first_name = request.POST.get('first_name')
      last_name = request.POST.get('last_name')
      phone_number = request.POST.get('phone_number')

      customer_id = request.POST.get('customer')

      customer_data = {
          "first_name": first_name,
          "last_name": last_name,
          "phone_number": phone_number,
      }

      form_data = {
          'sale_date': parsed_date,
          'depot': request.POST.get('depot'),
          'cylinder_id': request.POST.get('cylinder_id'),
          'is_existing_customer': is_existing_customer,
          'customer': customer_id,
          'first_name': first_name,
          'last_name': last_name,
          'phone_number': phone_number,
      }

      try:
          with transaction.atomic():
            # if not user, create
            if is_existing_customer == 'on':
                institution_customer = InstitutionCustomer.objects.filter(id=customer_id).first()
                customer = institution_customer.customer
                if not institution_customer:
                    # Return validation errors if the data is not valid
                    messages.error(request, 'Error adding the cylinder sale. Please check the form.')
            else:
                # create customer
                customer = Customer.objects.filter(phone_number=phone_number).first()
                if not customer:
                    customer_serializer = CustomerSerializer(data=customer_data)
                    if customer_serializer.is_valid():
                        customer = customer_serializer.save()

                institution_customer_data = {
                    "is_institution": True,
                    "institution": institution,
                    "customer": institution,
                }
                institution_customer_instance = InstitutionCustomerSerializer(data=institution_customer_data)
                if institution_customer_instance.is_valid():
                    institution_customer_instance = institution_customer_instance.save()

            data = {
                'cylinder_id': request.POST.get('cylinder_id'),
                'sale_date': parsed_date,
                'depot': request.POST.get('depot'),
                'customer': customer.id,
                'registerer': logged_in_user.id,
                'is_existing_customer': is_existing_customer,
                'customer': institution_customer,
            }

            cylinder_sale_serializer = CylinderSaleSerializer(data=data)
            if cylinder_sale_serializer.is_valid():
                cylinder_sale_instance = cylinder_sale_serializer.save()
                # Redirect on success
                messages.success(request, 'Cylinder Sale added successfully!')
                previous_page = request.META.get('HTTP_REFERER')  # Get the URL of the previous page
                return HttpResponseRedirect(previous_page)
            else:
                # Return validation errors if the data is not valid
                messages.error(request, 'Error adding the cylinder sale. Please check the form.')

                # get institution depots
                depots = Depot.objects.filter(owner=institution)
                # get cylinder sizes
                cylinder_sizes = CylinderSizes.objects.all()
                # get cylinder statuses
                statuses = Status.objects.all()
                context = {
                    "depots": depots,
                    "user": logged_in_user,
                    "statuses": statuses,
                    "cylinder": cylinder_id,
                    "cylinder_sizes": cylinder_sizes,
                    "user_account_data": user_account_data,
                    "active_user_account_data": active_user_account_data,
                    'errors': cylinder_sale_serializer.errors,
                    "form_data": form_data,
                }

                return render(request, 'institution/cylinder.html', context)
    
      except Exception as e:
          # Handle any exceptions
          messages.error(request, f'Error: {str(e)}')



def institution_settings(request):
  # template = loader.get_template('base.html')
  template = loader.get_template('institution/index.html')
  return HttpResponse(template.render())





@login_required
def institution_depots(request):
  # Get the logged-in user (if any)
  logged_in_user = request.user
  # Create a context dictionary with the user details
  user_account_data = get_user_accounts(logged_in_user)
  active_user_account_data = get_active_user_account(logged_in_user)
  if not active_user_account_data:
     return redirect('dashboard-user-accounts')
  # redirect if active account isn't institution
  if active_user_account_data['is_admin'] == True:
    return redirect('dashboard-user-accounts')

  print(f"active_user_account_data:{active_user_account_data}")

  # get institution 
  institution = Institution.objects.filter(slug=active_user_account_data['institution_slug']).first()
  # get institution depots
  depots = Depot.objects.filter(owner=institution)
  # get cylinder statuses
  statuses = Status.objects.all()

  # get institution users
  institution_users = (
    UserAccount.objects
    .filter(institution=institution, is_active=True)
    .select_related('user')
    .values('user', 'user__first_name', 'user__last_name', 'user__id')
    .distinct()
  )

  context = {
     "user":logged_in_user,
     "statuses":statuses,
     "depots":depots,
     "institution_users":institution_users,
     "user_account_data":user_account_data,
     "active_user_account_data":active_user_account_data,
     }
  return render(request, 'institution/depots.html', context)


@login_required
@csrf_protect
def institution_add_depot(request):
    # Get the logged-in user (if any)
    logged_in_user = request.user
    # accoount access
    user_account_data = get_user_accounts(logged_in_user)
    active_user_account_data = get_active_user_account(logged_in_user)
    if request.method == "POST":
      logger.info(f"request {request}")

      # get institution 
      institution = Institution.objects.filter(slug=active_user_account_data['institution_slug']).first()

      # depot iinformation
      depot_name = request.POST.get('depot_name')
      phone_number = request.POST.get('phone_number')
      email_address = request.POST.get('email_address')
      physical_location = request.POST.get('physical_location')
      is_existing_user = request.POST.get('is_existing_user')

      # new depot admin information
      first_name = request.POST.get('first_name')
      last_name = request.POST.get('last_name')
      admin_email = request.POST.get('admin_email')

      # new depot admin information
      admin_users = request.POST.getlist('admin_users[]')

      slug = depot_name.lower()
      slug = slug.replace(" ","-")

      # depot name
      if Depot.objects.filter(name=depot_name).exists() or Institution.objects.filter(name=depot_name).exists():
          messages.error(request, 'A depot with this name exists.')
          # return messages
          return redirect('dashboard-admin-depots')

      depot_data = {
        "slug":slug,
        "name":depot_name,
        "phone_number":phone_number,
        "email_address":email_address,
        "physical_location":physical_location,
        "owner":institution,
        "registerer":logged_in_user,
      }
      print(depot_data)
      print(f"is_existing_user:{is_existing_user}")
      print(f"admin_users:{admin_users}")

      user_data = {
          'first_name': first_name,
          'last_name': last_name,
          'is_superuser': False,
          'email': admin_email,
          'password': make_password('password'),
      }

      # return True
      try:
        with transaction.atomic():
          
          # create depot
          depot = Depot.objects.create(**depot_data)

          # create institution group
          # group_name: [institution_name]-[group/role name] i.e rubis-admin
          group_name = f"{slug}-Admin"
          group = Group(name=group_name)
          group.save()

          # get content types to assign peermissions
          model_classes = [Group, Cylinder, CylinderSizes, CylinderSale, CylinderRefill, CylinderReturn, CylinderCheck, Customer, Depot, LoyaltyPoints]
          permissions = [permission for model_class in model_classes for permission in Permission.objects.filter(content_type=ContentType.objects.get_for_model(model_class))]
          group.permissions.add(*permissions)

          # create user
          # user exists
          if is_existing_user == 'on':
            # if the user/ users exists
            # Get the selected user IDs from the multiselect
            admin_users = request.POST.getlist('admin_users[]')
            print(f"admin_users:{admin_users}")
            for admin_user in admin_users:
              user = User.objects.filter(id=admin_user).first()
              print(f"user:{user}")

              # create user account
              user_account_data = {
                "user":user,
                "user_group":group,
                "depot":depot,
                "user_account_type":3,
              }
              user_account = UserAccount.objects.create(**user_account_data)
          else:
            # create user if not exists
            user, created = User.objects.get_or_create(email=admin_email, defaults=user_data)

            # create user account
            user_account_data = {
              "user":user,
              "user_group":group,
              "depot":depot,
              "user_account_type":3,
            }

            user_account = UserAccount.objects.create(**user_account_data)

            # Check if the user was just created
            if created:
                # New user, send a welcome message
                welcome_message = f"Welcome to {institution.name}! 🌟 Discover a world of convenience and quality service with us. Your safety and satisfaction are our top priorities. Explore our offerings and feel free to reach out for any assistance. Enjoy your experience!"
                notify_users_through_sms(welcome_message, [user.phone_number])

                # Additional message to invite the new user to the organization
                invite_message = f"You've been invited to join {institution.name}. Click [link_to_invite_page] to accept the invitation and start using our services."
                notify_users_through_sms(invite_message, [user.phone_number])
            else:
                # Existing user, inform about the organization
                existing_user_message = f"Welcome back to {institution.name}! 🌟 Explore the latest updates and offerings. Feel free to reach out if you have any questions or need assistance. Enjoy your experience!"
                notify_users_through_sms(existing_user_message, [user.phone_number])         
      except Exception as e:
        print(f"e:{e}")
        logger.debug(f"e:{e}")


      return redirect('dashboard-institution-depots')


@login_required
def institution_view_depot(request, depot_id):
   pass




@login_required
def institution_users(request):
  # Get the logged-in user (if any)
  logged_in_user = request.user
  # Create a context dictionary with the user details
  user_account_data = get_user_accounts(logged_in_user)
  active_user_account_data = get_active_user_account(logged_in_user)
  if not active_user_account_data:
     return redirect('dashboard-user-accounts')
  # redirect if active account isn't institution
  if active_user_account_data['is_admin'] == True:
    return redirect('dashboard-user-accounts')

  # get institution 
  institution = Institution.objects.filter(slug=active_user_account_data['institution_slug']).first()
  # get institution users

  # Fetch user data for the current institution
  users_data = (
      UserAccount.objects
      .filter(institution=institution, is_active=True)
      .select_related('user')
      .prefetch_related('user_group')
      .order_by('user__email')
  )
  
  context = {
     "user":logged_in_user,
     "institution_users":users_data,
     "user_account_data":user_account_data,
     "active_user_account_data":active_user_account_data,
     }
  return render(request, 'institution/users.html', context)


@login_required
def institution_view_user(request, user_id):
   pass

@login_required
@csrf_protect
def institution_add_user(request):
  pass




@login_required
def institution_roles(request):
  # Get the logged-in user (if any)
  logged_in_user = request.user
  # Create a context dictionary with the user details
  user_account_data = get_user_accounts(logged_in_user)
  active_user_account_data = get_active_user_account(logged_in_user)
  if not active_user_account_data:
     return redirect('dashboard-user-accounts')
  # redirect if active account isn't institution
  if active_user_account_data['is_admin'] == True:
    return redirect('dashboard-user-accounts')

  # get institution 
  institution = Institution.objects.filter(slug=active_user_account_data['institution_slug']).first()
  # get institution users

  # Fetch all groups belonging to the specified institution
  institution_groups = Group.objects.filter(useraccount__institution=institution).distinct()


  # institution = Institution.objects.get(slug=active_user_account_data['institution_slug'])
  groups_for_institution = Group.objects.filter(useraccount__institution=institution)
  print(groups_for_institution)


  context = {
     "user":logged_in_user,
     "institution_groups":institution_groups,
     "user_account_data":user_account_data,
     "active_user_account_data":active_user_account_data,
     }
  return render(request, 'institution/roles.html', context)


@login_required
def institution_view_role(request, role_id):
   # Get the logged-in user (if any)
  logged_in_user = request.user
  # accoount access
  user_account_data = get_user_accounts(logged_in_user)
  active_user_account_data = get_active_user_account(logged_in_user)

  group = Group.objects.filter(id=role_id).first()
  context = {
     "user":logged_in_user,
     "group":group,
     "user_account_data":user_account_data,
     "active_user_account_data":active_user_account_data,
     }
  return render(request, 'institution/role.html', context)



@login_required
@csrf_protect
def institution_add_role(request):

  # Get the logged-in user (if any)
  logged_in_user = request.user
  # accoount access
  user_account_data = get_user_accounts(logged_in_user)
  active_user_account_data = get_active_user_account(logged_in_user)
  if request.method == "POST":
    role_name = request.POST.get('name')

    # get institution
    institution = Institution.objects.filter(slug=active_user_account_data['institution_slug']).first()

    # group_name: [institution_name]-[group/role name] i.e rubis-admin
    group_name = f"{institution.slug}-{role_name}"

    form_data = {
      'name':role_name,
    }
    data = {
      'name':group_name,
    }

    serializer = GroupSerializer(data=data)
    if serializer.is_valid():
      group_instance = serializer.save()

      # Redirect on success
      messages.success(request, 'Role {role_name} has been created successfully!')
      return redirect('dashboard-institution-role', group_id=group_instance.id)
    else:
      # Return validation errors if the data is not valid
      messages.error(request, 'Error adding the role. Please check the form.')

      # Fetch all groups belonging to the specified institution
      institution_groups = Group.objects.filter(useraccount__institution=institution).distinct()

      context = {
        "user":logged_in_user,
        "institution_groups":institution_groups,
        "user_account_data":user_account_data,
        "active_user_account_data":active_user_account_data,
        "errors":serializer.errors,
        "form_data":form_data,
        }
      print(context)
      return render(request, 'institution/roles.html', context, status=status.HTTP_400_BAD_REQUEST)










