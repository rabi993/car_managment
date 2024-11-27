
from django.urls import path

from . import views
urlpatterns = [
    
    path('home/', views.home, name='homepage'),
    path('brand/<slug:brand_slug>/', views.home, name='brand_wise_car'),
]