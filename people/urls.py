# urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_profile, name='user_profile'),
    path('people/<int:user_id>/userprofile/', views.user_profile, name='user_profile'),
    path('people/<int:user_id>/login/', views.login_page, name='login_page'),
    path('people/<int:user_id>/login/submit/', views.login_user, name='login_user'),
    path('people/<int:user_id>/login/code/', views.send_verification_code, name='send_verification_code'),
    path('people/<int:user_id>/logout/', views.logout_user, name='logout_user'),
    # API endpoint for the status app
    path('api/setStatus/', views.api_set_status, name='api_set_status'),

    path('debug-ip/', views.debug_ip, name='debug_ip'),
]