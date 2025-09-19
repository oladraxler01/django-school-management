from django.contrib import admin
from django.urls import path, include
from . views import *
from . import views

urlpatterns = [
    path('register.html', views.signup_view, name='signup'),          # ← ADD .html
    path('login.html', views.login_view, name='login'),             # ← ADD .html  
    path('forgot-password.html', views.forgot_password_test_view, name='forgot-password'),  # ← ADD .html
    path('reset-password/<str:token>.html', views.reset_password_view, name='reset-password'),  # ← ADD .html
    path('logout.html', views.logout_view, name='logout'),     


]

# path('signup/', signup_view, name='signup'),
#     path('login/', login_view, name='login'),

    
#     path('forgot-password/', forgot_password_view, name='forgot-password'),
#     path('reset-password/<str:token>/', reset_password_view, name='reset-password'),
#     path('logout/', logout_view, name='logout'),
# ]