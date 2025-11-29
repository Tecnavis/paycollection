from api.v1.users_api.views import login_user

from django.contrib import admin
from django.urls import path,include
from django.http import HttpResponse

def home(request):
    return HttpResponse("Welcome to collection Management")

urlpatterns = [
    path('api/v1/login/', login_user, name='login_api'),
    path('admin/', admin.site.urls),
    path('api/v1/cashcollection/', include(('api.v1.cashcollection_api.urls'),namespace='cashcollection_api')),
    path('api/v1/users/', include(('api.v1.users_api.urls'),namespace='users_api')) , 
    path('api/v1/financials/', include(('api.v1.financials_api.urls'),namespace='financials_api')),
    path('api/v1/partner/', include(('api.v1.customer_api.urls'),namespace='partner_api')),
    path('',home,name='home'),
]
