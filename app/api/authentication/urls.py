"""app URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path, include
from .views import RegistrationAPIView, LoginAPIView, VerifyAPIView, UserRetrieveUpdateAPIView

"""when using classes at urlpattern, you always include .as_view() as fucntion,
else if using normal functions, use brackets."""

urlpatterns = [
    path('signup', RegistrationAPIView.as_view(), name='user-registration'),
    path('login', LoginAPIView.as_view(), name='user-login'),
    path('verify/<str:token>', VerifyAPIView.as_view(), name='user-verification'),
    path('retrieve', UserRetrieveUpdateAPIView.as_view(), name='users-retrieve-search'),
]
