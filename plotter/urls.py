from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from agent.views import (ProfileViewSet, ClientViewSet, ListViewSet, OptionViewSet, CardViewSet, DealViewSet,
                         PublicListViewSet)
from property.views import PropertyViewSet, CommissionViewSet
from user.views import UserDeleteView
from task.views import TaskViewSet

router = DefaultRouter()
router.register(r'profiles', ProfileViewSet, basename='profiles')
router.register(r'clients', ClientViewSet, basename='clients')
router.register(r'lists', ListViewSet, basename='lists')
router.register(r'options', OptionViewSet, basename='options')
router.register(r'properties', PropertyViewSet, basename='properties')
router.register(r'commissions', CommissionViewSet, basename='commissions')
router.register(r'deals', DealViewSet, basename='deals')
router.register(r'cards', CardViewSet, basename='cards')
router.register(r'tasks', TaskViewSet, basename='tasks')




urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('', include('djoser.urls.jwt')),
    path('users/<int:pk>/delete/', UserDeleteView.as_view(), name='custom_user_delete'),
    path('client-list/<uuid:uuid>/', PublicListViewSet.as_view({'get': 'retrieve'}), name='public-list-detail'),
]

urlpatterns += router.urls
