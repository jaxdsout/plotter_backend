from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from agent.views import ProfileViewSet, ClientViewSet, ListViewSet, OptionViewSet
from property.views import PropertyViewSet

router = DefaultRouter()
router.register(r'profiles', ProfileViewSet, basename='profiles')
router.register(r'clients', ClientViewSet, basename='clients')
router.register(r'lists', ListViewSet, basename='lists')
router.register(r'options', OptionViewSet, basename='options')
router.register(r'properties', PropertyViewSet, basename='properties')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('auth/', include('djoser.urls')),
    path('auth/jwt/', include('djoser.urls.jwt')),
    path('plotter/', include(router.urls)),
    path('', include('frontend.urls'))
]

urlpatterns += router.urls
