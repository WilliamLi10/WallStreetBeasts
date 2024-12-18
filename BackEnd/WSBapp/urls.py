
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
    path('portfolio/', views.get_portfolio_view, name='get_portfolio_view'),
    path('edit_portfolio/', views.edit_portfolio_view, name='edit_portfolio_view'),
    path('reset_password/', views.reset_password_view, name='reset_password_view'),
    path('stock_search/', views.stock_search_view, name='stock_search_view'),
]

