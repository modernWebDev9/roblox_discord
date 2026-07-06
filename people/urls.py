#urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('people/<int:user_id>/userprofile/', views.user_profile, name='user_profile'),
    path('people/<int:user_id>/login/', views.login_page, name='login_page'),
    path('people/<int:user_id>/login/submit/', views.login_user, name='login_user'),
    path('people/<int:user_id>/logout/', views.logout_user, name='logout_user'),
]