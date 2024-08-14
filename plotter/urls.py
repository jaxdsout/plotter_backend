from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('auth/', include('user.urls')),
    path('property/', include('property.urls')),
    path('plotter/', include('agent.urls'))
]
