from django.urls import path
from api.views import PostcodeView, PostcodeBatchView

urlpatterns = [
    path('postcode/<str:postcode>/', PostcodeView.as_view(), name='get_postcode'),
    path('batch/', PostcodeBatchView.as_view(), name='batch_endpoint'),
]
