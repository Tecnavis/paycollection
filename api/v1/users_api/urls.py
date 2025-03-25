from django.urls import path
from . import views
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView,TokenVerifyView


app_name = 'users_api'


urlpatterns = [
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('login/', views.login_user, name='login'),
    path('auth/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    
    path('users/',views.get_user_profile,name='user_list'),
    path("users/<int:id>/",views.get_user_profile_by_id,name='user-detail'),
    path("profile/", views.user_profile, name="user-profile"), 


    path('staffs/create/', views.create_staff_user, name='create_staff_user'),
    path('staffs/', views.list_staff_users, name='list_staff_users'),
    path('staffs/<int:id>/', views.update_staff_user, name='update_staff_user'),
    path('staffs/<int:id>/delete/', views.delete_staff_user, name='delete_staff_user'),
   

    path('admin/create/', views.create_admin_user, name='create_admin_user'),
    path('admin/<int:id>/delete/', views.delete_admin_user, name='delete_admin_user'),
    path('admin/<int:id>/', views.update_admin_user, name='update_admin_user'),

    path('change-password/', views.change_password, name='change_password'),
    # path('reset-password/', views.reset_password, name='reset_password'),
   
]
