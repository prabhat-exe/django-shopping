"""
URL configuration for shopping project.

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
from myapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin_login',views.admin_login,name='admin_login'),
    path('admin_dashboard',views.admin_dashboard,name='admin_dashboard'),
    path('admin_add_section',views.admin_add_section,name='add_section'),
    path('admin_add_product',views.admin_add_product,name='add_product'),
    path('admin_view_product',views.admin_view_product,name='view_product'),
    path('admin_edit_product/<id>',views.admin_edit_product,name='edit_product'),
    path('delete_product/<id>',views.delete_product,name='delete_product'),
    path('',views.home,name='home'),
    path('signup',views.signup,name='signup'),
    path('login',views.login,name='login'),
    path('logout',views.logout,name='logout'),
    path('profile',views.profile_view,name='profile'),
    path('cart',views.cart,name='cart'),
    path('change_pass',views.change_pass,name='change_pass'),
    path('emailotp',views.emailOtp,name='emailotp')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
