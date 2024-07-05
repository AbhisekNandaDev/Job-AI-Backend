from django.urls import path
from .views import SignupApiView,VerifyOtpAPIView,LoginAPIView

urlpatterns = [
    path('signup/', SignupApiView.as_view(), name='signup'),
    path('verify-signup/',VerifyOtpAPIView.as_view(),name="verify-otp-signup"),
    path('login/', LoginAPIView.as_view(), name='login'),
]