from django.urls import path, include

urlpatterns = [
    path('', include('djoser.urls')),
    # path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include('djoser.urls.jwt')),

]

