from django.urls import path
from . import views

urlpatterns = [
    path('', views.book_list, name='book_list'),
    path('book/<slug:slug>/', views.book_detail, name='book_detail'),
    path('create-checkout-session/<int:book_id>/', 
         views.create_checkout_session, name='create_checkout_session'),
    path('payment-success/<int:book_id>/', 
         views.payment_success, name='payment_success'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('download/<int:book_id>/', views.download_book, name='download_book'),
]