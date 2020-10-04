from django.urls import path
from rest_framework.authtoken import views as rfViews


from . import views

urlpatterns = [
    path('table/<uuid:table_id>/', views.sit_to_table, name='Sit to table'),
    path('order/', views.create_order, name='Create payment intent'),
    path('account/create', views.create_account, name='Create user account'),
    path('account/userinfo', views.get_user_info, name='User info'),
    path('stripe/ephemeralkey', views.stripe_create_ephemeral_key, name="Create Stripe ephemeral key"),
]
