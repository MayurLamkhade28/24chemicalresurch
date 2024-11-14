"""
URL configuration for home project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from web import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.HomeView.as_view(), name='home'),
    path('report/<int:rep_id>/<slug:url_slug>/', views.ReportDetailView.as_view(), name='report_detail'),
    path('add_to_cart/<int:rep_id>/', views.AddToCartView.as_view(), name='cart'),
    path('cart/', views.CartView.as_view(), name='cart'),
    path('update-price/', views.UpdatePriceView.as_view(), name='update_price'),
    path('remove/', views.Remove.as_view(), name='remove'),
    path('buy_now/', views.BuyNowView.as_view(), name='buy_now'),
]
