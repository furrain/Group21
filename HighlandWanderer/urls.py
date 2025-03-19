from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('category/<str:category_name>/', views.category_view, name='category'),
    path('search/', views.search_results, name='search_results'),
    path('location/<int:location_id>/', views.location_detail, name='location_detail'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    # Built-in authentication views.
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # Admin functionalities.
    path('admin/add_category/', views.add_category, name='add_category'),
    path('admin/add_location/', views.add_location, name='add_location'),
    path('about/', views.about_us, name='about_us'),
]