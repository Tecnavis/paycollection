from django.urls import path
from . import views

app_name = 'customer_api'


urlpatterns = [
    path("customers/", views.customer_list, name="customer_list"),
    path("customers/<int:id>/", views.customer_detail, name="customer_detail"),
    path("customers/<int:id>/delete/", views.customer_delete, name="customer_delete"),
    path("customers/create/", views.customer_create, name="customer_create"),
    path("customers/<int:id>/update/", views.customer_update, name="customer_update"),

    path('partner/', views.list_agents, name='agent-list'),
    path('partners/create/', views.create_agent, name='agent-create'),
    path('partners/<int:id>/', views.update_agent, name='agent-update'),
    path('partners/<int:id>/delete/', views.delete_agent, name='agent-delete'),
    path('partners/<int:id>/details/', views.agent_detail, name='agent-details'),

] 