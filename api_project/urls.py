from django.urls import path, include

urlpatterns = [
    path('n8n/', include('apps.n8n_integration.urls')),
]