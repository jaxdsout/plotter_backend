from django.urls import path
from .views import HomePage, UserRegister, UserVerify, UserLogin, Dashboard

urlpatterns = [
    path('', HomePage.as_view(), name='home'),
    path('user-signup/', UserRegister.as_view(), name='user_signup'),
    path('verify/<uid>/<token>', UserVerify.as_view(), name='user_verify'),
    path('login/', UserLogin.as_view(), name='user_login'),
    path('dashboard/', Dashboard.as_view(), name='dashboard')
]