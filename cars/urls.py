from django.contrib import admin
from django.urls import path, include
from . import views
# from transactions.views import BuyCarView
urlpatterns = [
    # path('add/', views.add_car, name='add_car'),
    path('add/', views.AddCarCreateView.as_view(), name='add_car'),
    # path('edit/<int:id>', views.edit_car, name='edit_car'),
    path('edit/<int:id>', views.EditCarView.as_view(), name='edit_car'),
    # path('delete/<int:id>', views.delete_car, name='delete_car'),
    path('delete/<int:id>', views.DeleteCarView.as_view(), name='delete_car'),
    path('cars/details/<int:pk>', views.DetailCarView.as_view(), name='detail_car'),
    path('cars/buy/<int:car_id>/', views.buy_now, name='buy_now'),
    
    # path('buy-car/<int:car_id>/', BuyCarView.as_view(), name='buy_car'),
    
   
]