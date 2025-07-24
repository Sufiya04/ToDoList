from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns=[
    path('',home),
    path('home',home,name='home'),
    path('about',about),
    path('contact',mailsend),
    path('register',register,name='register'),
    path('signin',signin),
    # path('login',userlogin,name='login'),
    path('signup',signup_view,name='signup'),
    path('login', student_login, name='login'),
    path('course',course,name='course'),
    path('profile',profile_view,name='profile'),
    path('edit_profile',edit_profile,name='edit_profile'),
    path('logout',logout_view,name='logout'),
    path('reset_password', reset_password, name='reset_password'),
    path('set_new_password', set_new_password, name='set_new_password'),
    path('dashboard', dashboard_view, name='dashboard'),  # Define student_dashboard view separately
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]


