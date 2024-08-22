from django.urls import path
from .views import HomePage, UserRegister, UserVerify, UserLogin

urlpatterns = [
    path('', HomePage.as_view(), name='home'),
    path('user-signup/', UserRegister.as_view(), name='user_signup'),
    path('verify/<uid>/<token>', UserVerify.as_view(), name='user_verify'),
    path('user-login/', UserLogin.as_view(), name='user_login')
]