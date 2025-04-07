from django.urls import path
from . import views

app_name = 'cashcollection_api'


urlpatterns = [
    path("cashcollections/", views.cash_collection_list, name="cashcollection_list"),
    path("cashcollections/<int:id>/details/", views.cash_collection_detail, name="cashcollection_detail"),
    path("cashcollections/<int:id>/delete/", views.cashcollection_delete, name="cashcollection_delete"),
    path("cashcollection/create/", views.enroll_customer_in_scheme, name="cashcollection_create"),
    
    path("schemes/", views.scheme_list, name="scheme_list"),
    path("schemes/<int:id>/", views.scheme_update, name="scheme_update"),
    path("schemes/create/", views.scheme_create, name="scheme_create"),

    path("cashcollection/bycustomer/create/", views.cash_collection_entry_create, name="cash-collection-entry"),
    path("cashcollection/bycustomer/", views.cash_collection_entry_list, name="cash-collection-entry-list"),
    # payment history
    path("customer-scheme-payments/", views.customer_scheme_payment_list, name="customer-scheme-payments"),
    path('customer-schemes/', views.get_customer_schemes, name='customer-scheme-list'),

] 