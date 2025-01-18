from django.contrib import admin
from django.urls import path, include
from PharmacyInterface import views
from django.views.generic import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url='/home/', permanent=False)),
    #path('', views.home, name='home'),
    #path('products/', include('PharmacyInterface.urls')),
    path('admin/', admin.site.urls),
    #path('', include('PharmacyInterface.urls')),
    path('api/', include('pharmacyApp.urls')),
    path('home/', include('PharmacyInterface.urls')),
]
