from django.urls import path
from api.views import PostcodeView, PostcodeBatchView, RequestCSV, CheckCsvStatus

urlpatterns = [
    path('postcode/<str:postcode>/', PostcodeView.as_view(), name='get_postcode'),
    path('batch/', PostcodeBatchView.as_view(), name='batch_endpoint'),
    path('csv/', RequestCSV.as_view(), name='request_csv'),
    path('csv-status/<str:task_id>/', CheckCsvStatus.as_view(), name='check_status'),
]
