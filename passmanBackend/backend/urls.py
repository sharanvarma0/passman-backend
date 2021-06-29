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

router = routers.DefaultRouter()
router.register(r'vaults',VaultViewSet, basename='vault')
router.register(r'users', UserViewSet, basename='user')
router.register(r'records',VaultRecordViewSet, basename='records')
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api-token-auth/', views.obtain_auth_token),
]
