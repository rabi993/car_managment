from django.urls import path, include
from .views import UserRegistrationView, UserLoginView, UserBankAccountUpdateView, user_logout,pass_change,buy_list,return_item
# from django.contrib.auth.views import LogoutView
urlpatterns = [
    
    path('register/', UserRegistrationView.as_view(), name='register' ),
    path('login/', UserLoginView.as_view(), name='login'),
    # path('logout/', UserLogoutView.as_view(), name='logout'),
    path('logout/', user_logout, name='logout'),
    # path('profile/', Profile, name='profile' ),
    path('profile/', UserBankAccountUpdateView.as_view(), name='profile' ),
    path('profile/pass_change/', pass_change, name='pass_change'),
    path('profile/buy-list/', buy_list, name='buy_list'),
    # path('profile/buy-list/<int:car_id>/', buy_list, name='buy_list'),
    path('return-item/<int:cart_item_id>/', return_item, name='return_item'),

]