from django.urls import path
from .api_views import SendDataView, GetDataView

urlpatterns = [
    path('send-data/', SendDataView.as_view(), name='send_data'),
    path('get-data/', GetDataView.as_view(), name='get_data'),
]