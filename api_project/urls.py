from django.urls import path, include

urlpatterns = [
    # BDJobs Hot Jobs API
    path('n8n/', include('apps.n8n_integration.urls')),
    
    # BD Government Jobs API
    path('bdgovjob/', include('apps.bdgovjob.urls')),
]