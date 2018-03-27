"""Caldera URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.conf import settings
from django.conf.urls import include, url
import temp_monitor.views as views
import django_saml2_auth.views
from django.contrib.auth import views as auth_views
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'temperature', views.TempViewSet)

urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    url('^accounts/', include('django.contrib.auth.urls')),
    url(r'^logout/$', auth_views.LogoutView.as_view(next_page='/accounts/login?next=/overview/'), name='logout'),
]
