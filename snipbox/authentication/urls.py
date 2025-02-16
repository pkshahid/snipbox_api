from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView

from authentication.views import RegisterView

urlpatterns = [
    path('register', RegisterView.as_view(), name="register"),
    path('login', TokenObtainPairView.as_view(), name="login"),
]
