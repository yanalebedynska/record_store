from django.contrib import admin
from django.urls import path, include
from PharmacyInterface import views

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', include('PharmacyInterface.urls')),
    path('admin/', admin.site.urls),
    path('', include('PharmacyInterface.urls')),
    path('api/', include('pharmacyApp.urls')),
]