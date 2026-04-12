from django.urls import path
from accounts import views


urlpatterns = [
    path('register/', views.UserCreate.as_view(), name='register'),
    path('login/', views.FindPostcodeLoginView.as_view(), name='login'),
]