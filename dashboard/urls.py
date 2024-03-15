from django.urls import path

from dashboard import views

urlpatterns = [


    path("login", views.login_view, name="dashboard-login"),
    path("logout", views.logout_view, name="dashboard-logout"),
    path("forgot/password", views.forgot_password_view, name="dashboard-forgot-password"),
    path("forgot/password/done", views.forgot_password_done_view, name="dashboard-forgot-password-done"),
    # path("password/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$", views.password_reset_confirm_view, name="dashboard-password-reset-confirm"),
    path("password/reset/1", views.password_reset_confirm_view, name="dashboard-password-reset-confirm"),
    path("password/reset/done", views.password_reset_done_view, name="dashboard-password-reset-done"),


    path("dashboard/user/accounts", views.dashboard_user_accounts, name="dashboard-user-accounts"),
    path("dashboard/user/account/<account_id>", views.dashboard_user_account, name="dashboard-user-account"),

    # admin dashboard
    path("dashboard/home", views.dashboard_home, name="dashboard-home"),

    path("admin/dashboard/index", views.admin_dashboard, name="dashboard-admin-index"),
    path("admin/dashboard/analytics", views.admin_dashboard_analytics, name="dashboard-admin-analytics"),
    path("admin/dashboard/commerce/1", views.admin_dashboard_commerce_1, name="dashboard-admin-commerce-1"),
    path("admin/dashboard/commerce/2", views.admin_dashboard_commerce_2, name="dashboard-admin-commerce-2"),
    path("admin/dashboard/sales", views.admin_dashboard_sales, name="dashboard-admin-sales"),
    path("admin/dashboard/minimal/1", views.admin_dashboard_minimal_1, name="dashboard-admin-minimal-1"),
    path("admin/dashboard/minimal/2", views.admin_dashboard_minimal_2, name="dashboard-admin-minimal-2"),
    path("admin/dashboard/crm", views.admin_dashboard_crm, name="dashboard-admin-crm"),

    # institution crud
    path("admin/institutions", views.admin_institutions, name="dashboard-admin-institutions"),
    path("admin/institution/<institution_id>", views.admin_institution, name="dashboard-admin-institution"),
    path("admin/add/institution", views.admin_add_institution, name="dashboard-admin-add-institution"),
    path('admin/admin/update/<institution_id>/', views.admin_update_institution, name='dashboard-admin-update-institution'),

    path("admin/depots", views.admin_institutions, name="dashboard-admin-depots"),

    path("admin/settings", views.admin_settings, name="dashboard-admin-settings"),
    




    # institution dashboard
    path("institution/home", views.institution_home, name="dashboard-institution-home"),
    path("institution/index", views.institution_index, name="dashboard-institution-index"),

    path("institution/cylinders", views.institution_cylinders, name="dashboard-institution-cylinders"),
    path('institution/cylinder/<cylinder_id>/', views.institution_view_cylinder, name='dashboard-institution-cylinder'),
    path("institution/add/cylinder", views.institution_add_cylinder, name="dashboard-institution-add-cylinder"),
    path('institution/cylinder/update/<cylinder_id>/', views.institution_update_cylinder, name='dashboard-institution-update-cylinder'),

    path('institution/cylinder/add/check', views.institution_cylinder_add_check, name='dashboard-institution-cylinder-add-check'),
    path('institution/cylinder/add/exchange', views.institution_cylinder_add_exchange, name='dashboard-institution-cylinder-add-exchange'),
    path('institution/cylinder/add/inspection', views.institution_cylinder_add_inspection, name='dashboard-institution-cylinder-add-inspection'),
    path('institution/cylinder/add/refill', views.institution_cylinder_add_refill, name='dashboard-institution-cylinder-add-refill'),
    path('institution/cylinder/add/sale', views.institution_cylinder_add_sale, name='dashboard-institution-cylinder-add-sale'),

    path("institution/depots", views.institution_depots, name="dashboard-institution-depots"),
    path('institution/depot/<depot_id>/', views.institution_view_depot, name='dashboard-institution-depot'),
    path("institution/add/depot", views.institution_add_depot, name="dashboard-institution-add-depot"),

    path("institution/users", views.institution_users, name="dashboard-institution-users"),
    path('institution/user/<user_id>/', views.institution_view_user, name='dashboard-institution-user'),
    path("institution/add/user", views.institution_add_user, name="dashboard-institution-add-user"),

    path("institution/roles", views.institution_roles, name="dashboard-institution-roles"),
    path('institution/role/<role_id>/', views.institution_view_role, name='dashboard-institution-role'),
    path("institution/add/role", views.institution_add_role, name="dashboard-institution-add-role"),

    path("institution/settings", views.institution_settings, name="dashboard-institution-settings"),




    
]