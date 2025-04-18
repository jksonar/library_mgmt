from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_page, name='landing'),
    path('books/', views.book_list, name='book_list'),
    path('books/<int:book_id>/', views.book_detail, name='book_detail'),
    path('issue/<int:book_id>/', views.issue_book, name='issue_book'),
    path('my-books/', views.my_books, name='my_books'),
    path('return/<int:issue_id>/', views.return_book, name='return_book'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
]
