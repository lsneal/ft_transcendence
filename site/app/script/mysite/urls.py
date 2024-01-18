"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [
    path('', views.home),
    path('test/', views.test),
    path('admin/', admin.site.urls),
    path('bands/', views.band_list, name='band-list'),
    path('bands/add/', views.band_create, name='band-create'), 
    path('bands/<int:id>/', views.band_detail, name='band-detail'),
    path('bands/<int:id>/update/', views.band_update, name='band-update'),
    path('bands/<int:id>/delete/', views.band_delete, name='band-delete'),
    path('about-us/', views.about, name='about-us'),
    path('listings/', views.listings, name='listing'),
    path('listings/<int:id>/', views.listings_detail, name='list-detail'),
    path('listings/<int:id>/update/', views.listings_update, name='list-update'),
    path('listings/add/', views.listing_create, name='list-create'),
    path('contact-us/', views.contact, name='contact-us'),
    path('email-sent/', views.email_sent, name='email-sent'),
]
