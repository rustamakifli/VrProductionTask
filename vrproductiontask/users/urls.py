
from django.urls import path,re_path
from users.views import (
    account,
    logout,
    UserLoginView,
    ContactView,
    UserRegisterView
)

urlpatterns = [
    path('account/', account, name='account'),
    path('logout/', logout, name='logout'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('register/', UserRegisterView.as_view(), name='register'),
]
