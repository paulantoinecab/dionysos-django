from django.urls import path
from rest_framework.authtoken import views as rfViews


from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('table/<uuid:table_id>/', views.sit_to_table, name='Sit to table'),
    path('order/', views.create_order, name='Create payment intent'),
    path('account/create', views.create_account, name='Create user account'),
#    path('account/login', views.log_in, name='Log in'),
    path('account/logout', views.log_out, name='Log out'),
]
