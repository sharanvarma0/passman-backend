"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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

# Serializers are in 'vault_serializers.py'
# viewsets are in 'vault_viewsets.py'

# Importing all viewsets defined and other functions. 

from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken import views
from backend.vault_viewsets import *


# Using the rest_framework provided router class here to automatically generate views from viewsets defined. Makes things a lot easier. I have used defaultRouter here.
# Might use another router in the future if it makes things easy. As you know, still learning :).

# One special url you would see is the obtain_auth_token url which is just picked from rest_framework.authtoken views library. This allows you to obtain an auth token for the user as soon as they 
# query the endpoint specified. This is not something I developed. Please do take a look at the django rest_framework documentation to know more about this.

router = routers.DefaultRouter()
router.register(r'vaults',VaultViewSet, basename='vault')
router.register(r'users', UserViewSet, basename='user')
router.register(r'records',VaultRecordViewSet, basename='records')
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api-token-auth/', views.obtain_auth_token),
]
