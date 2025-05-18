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
    path("cashcollection/bycustomer/<int:pk>/", views.cash_collection_entry_update, name="cash-collection-entry-update"),
    path("cashcollection/bycustomer/<int:pk>/delete/", views.cash_collection_entry_delete, name="cash-collection-entry-delete"),
    
    
    path("customer-transactions/", views.customer_transaction_list, name="customer-transaction-list"),
    path("customer-transactions/<int:pk>/", views.customer_transaction_update, name="customer-transaction-update"),
    path("customer-transactions/<int:pk>/delete/", views.customer_transaction_delete, name="customer-transaction-delete"),
    
    # Payment history
    path("customer-scheme-payments/", views.customer_scheme_payment_list, name="customer-scheme-payments"),
    path("customer-scheme-payment/", views.customer_scheme_payment_list_logged_in_user, name="customer-scheme-payments-by-id"),
    path('customer-schemes/', views.get_customer_schemes, name='customer-scheme-list'),

    # Daily Collection Entry
    path("collections/", views.collection_list, name="collection_list"),
    path("collections/create/", views.collection_create, name="collection_create"),
    path("collections/<int:pk>/", views.collection_detail_or_update_or_delete, name="collection_detail_update_delete"),
    path("collections/summary/", views.collection_summary, name="collection_summary"),

    
]