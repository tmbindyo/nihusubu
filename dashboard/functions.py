from django.shortcuts import redirect
from authentication.models import User, UserAccount

def get_user_accounts(user):
    user_accounts  = UserAccount.objects.filter(user=user)
    user_account_data = []
    for user_account in user_accounts:

        if user_account.user_account_type == 2:
            user_account_slug_rem = f"{user_account.institution.slug}-" if not user_account.is_admin else ""
        elif user_account.user_account_type == 3:
            user_account_slug_rem = f"{user_account.depot.slug}-" if not user_account.is_admin else ""

        group = user_account.user_group.name.replace(user_account_slug_rem, "")
        user_account_data.append({
            "id":user_account.id,
            "group":user_account.user_group.name,
            "group_name":group,
            "is_active":user_account.is_active,
            "is_admin":user_account.is_admin,
            "institution_name":user_account.institution.name if user_account.institution else None,
            "institution_slug":user_account.institution.slug if user_account.institution else None,
            "depot_name":user_account.depot.name if user_account.depot else None,
            "depot_slug":user_account.depot.slug if user_account.depot else None,
            "user_account_type_display_name": user_account.get_user_account_type_display(),
            "user_account_type_display": user_account.user_account_type,
        })
    return user_account_data


def get_active_user_account(user):
    active_user_account_data = None
    user_account  = UserAccount.objects.filter(user=user).filter(is_active=True).first()
    if user_account:
        permissions = user_account.user_group.permissions.all()
        permission_list = [permission.codename for permission in permissions]

        if user_account.user_account_type == 2:
            user_account_slug_rem = f"{user_account.institution.slug}-" if not user_account.is_admin else ""
        elif user_account.user_account_type == 3:
            user_account_slug_rem = f"{user_account.depot.slug}-" if not user_account.is_admin else ""

        group = user_account.user_group.name.replace(user_account_slug_rem, "")
        active_user_account_data = {
            "id":user_account.id,
            "group":user_account.user_group.name,
            "group_name":group,
            "is_active":user_account.is_active,
            "is_admin":user_account.is_admin,
            "permission_list":permission_list,
            "institution_name":user_account.institution.name if user_account.institution else None,
            "institution_slug":user_account.institution.slug if user_account.institution else None,
            "depot_name":user_account.depot.name if user_account.depot else None,
            "depot_slug":user_account.depot.slug if user_account.depot else None,
            "user_account_type_display_name": user_account.get_user_account_type_display(),
            "user_account_type_display": user_account.user_account_type,
        }
        return active_user_account_data
    else:
        return active_user_account_data



def admin_middleware(user):
    user_account  = UserAccount.objects.filter(user=user).filter(is_active=True).first()
    if user_account.user_account_type != 1:
        return redirect('dashboard-user-accounts')
    

def lpg_middleware(user):
    user_account  = UserAccount.objects.filter(user=user).filter(is_active=True).first()
    if user_account.user_account_type != 2:
        return redirect('dashboard-user-accounts')
    

def depot_middleware(user):
    user_account  = UserAccount.objects.filter(user=user).filter(is_active=True).first()
    if user_account.user_account_type != 3:
        return redirect('dashboard-user-accounts')