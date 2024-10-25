
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('home/', views.landing_page, name='landing_page'),
    path('login/', views.login_view, name='login_view'),
    path('register/', views.registration_view, name='registration_view'),
    path('logout/', views.logout_view, name='logout_view'),
]

