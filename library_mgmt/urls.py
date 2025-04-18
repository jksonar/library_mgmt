
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from library.views import LogoutViaGet

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('library.urls')),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
]