from django.urls import path
from .api_views import (
    SendDataView, 
    GetDataView,
    GetTodayDataView,
    GetYesterdayDataView,
    GetWeekDataView,
    GetMonthDataView,
    GetDateDataView,
)

urlpatterns = [
    # Data submission endpoint
    path('send-data/', SendDataView.as_view(), name='send_data'),
    
    # Smart filtering endpoints
    path('get-data/', GetDataView.as_view(), name='get_data'),  # Supports query params
    path('get-data/today/', GetTodayDataView.as_view(), name='get_today'),
    path('get-data/yesterday/', GetYesterdayDataView.as_view(), name='get_yesterday'),
    path('get-data/week/', GetWeekDataView.as_view(), name='get_week'),
    path('get-data/month/', GetMonthDataView.as_view(), name='get_month'),
    path('get-data/date/<str:date_str>/', GetDateDataView.as_view(), name='get_date'),
]