"""website URL Configuration

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
from django.contrib import admin
from django.urls import path, include
from signup.views import signaction
from login.views import loginaction, welcome
from django.shortcuts import redirect

def admin_dashboard_redirect(request):
    return redirect('/hotelweb/admin/dashboard/')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', signaction, name='register'), 
    path('login/', loginaction, name='login'),
    path('', welcome, name='home'),
    path('welcome/', welcome, name='welcome'),
    path('hotelweb/', include('hotelweb.urls')),  # Include hotelweb URLs with prefix
    path('welcome/admin_dashboard/', admin_dashboard_redirect, name='admin_dashboard_redirect'),
]
