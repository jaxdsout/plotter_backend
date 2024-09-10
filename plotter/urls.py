from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from agent.views import (ProfileViewSet, ClientViewSet, ListViewSet, OptionViewSet, CardViewSet, DealViewSet,
                         PublicListViewSet)
from property.views import PropertyViewSet

router = DefaultRouter()
router.register(r'profiles', ProfileViewSet, basename='profiles')
router.register(r'clients', ClientViewSet, basename='clients')
router.register(r'lists', ListViewSet, basename='lists')
router.register(r'options', OptionViewSet, basename='options')
router.register(r'properties', PropertyViewSet, basename='properties')
router.register(r'deals', DealViewSet, basename='deals')
router.register(r'cards', CardViewSet, basename='cards')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('auth/', include('user.urls')),
    path('', include(router.urls)),
    path('client-list/<uuid:uuid>/', PublicListViewSet.as_view({'get': 'retrieve'}), name='public-list-detail'),
]

urlpatterns += router.urls
