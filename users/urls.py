from django.urls import path
from .views import PhoneLoginView

urlpatterns = [
    path("login/", PhoneLoginView.as_view(), name="phone-login"),
]
