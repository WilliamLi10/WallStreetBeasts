
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('home/', views.landing_page, name='landing_page'),
    path('login/', views.login_view, name='login_view'),
    path('register/', views.registration_view, name='registration_view'),
    path('logout/', views.logout_view, name='logout_view'),
    path("verify_email/", views.verify_email_view, name='verify_email_view'),
    path('request_new_code/', views.request_new_code_view, name='request_new_code_view'),
    path('stocks/', views.stocks_data_view, name='stocks_data_view'),
]

