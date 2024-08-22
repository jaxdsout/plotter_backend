from django.urls import path
from .views import HomePage, UserRegister, UserVerify, UserLogin, Dashboard, UserLogout, UserProfile

urlpatterns = [
    path('', HomePage.as_view(), name='home'),
    path('signup/', UserRegister.as_view(), name='user_signup'),
    path('verify/<uid>/<token>', UserVerify.as_view(), name='user_verify'),
    path('login/', UserLogin.as_view(), name='user_login'),
    path('logout/', UserLogout.as_view(), name='user_logout'),
    path('user/dashboard/', Dashboard.as_view(), name='dashboard'),
    path('user/profile/', UserProfile.as_view(), name='user_profile')
]