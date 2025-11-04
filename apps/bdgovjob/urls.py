from django.urls import path
from .api_views import (
    SendDataView, 
    GetDataView,
    GetTodayDataView,
    GetYesterdayDataView,
    GetWeekDataView,
    GetMonthDataView,
    GetDateDataView,
    GetStatsView,
)

urlpatterns = [
    # Data submission endpoint
    path('send-data/', SendDataView.as_view(), name='bdgovjob_send_data'),
    
    # Smart filtering endpoints
    path('get-data/', GetDataView.as_view(), name='bdgovjob_get_data'),
    path('get-data/today/', GetTodayDataView.as_view(), name='bdgovjob_get_today'),
    path('get-data/yesterday/', GetYesterdayDataView.as_view(), name='bdgovjob_get_yesterday'),
    path('get-data/week/', GetWeekDataView.as_view(), name='bdgovjob_get_week'),
    path('get-data/month/', GetMonthDataView.as_view(), name='bdgovjob_get_month'),
    path('get-data/date/<str:date_str>/', GetDateDataView.as_view(), name='bdgovjob_get_date'),
    
    # Statistics endpoint
    path('stats/', GetStatsView.as_view(), name='bdgovjob_stats'),
]

