from django.urls import path, include

from api.views import PostcodeView

urlpatterns = [
    path('postcode/<str:postcode>/', PostcodeView.as_view(), name='get_postcode'),
]
