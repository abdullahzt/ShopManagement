"""Defines URL patterns for shop_maangement_main."""

from django.urls import path

from . import views

app_name = 'shop_management_main'
urlpatterns = [
    # Home page.
    path('', views.index, name='index'),
    # Products page.
    path('products/', views.products, name='products'),
    #Adding new product page.
    path('new_product/', views.new_product, name='new_product'),
    #Transaction Page.
    path('transaction_days/', views.transaction_days, name='transaction_days'),
    #Individual transactions
    # path('transactions/', views.transactions, name='transactions'),
]
