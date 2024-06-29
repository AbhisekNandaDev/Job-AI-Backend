from django.urls import path
from .views import JobCreateAPIView,StartCrawl

urlpatterns = [
    path('api/jobs/', JobCreateAPIView.as_view(), name='create-a-job'),
    path('api/jobs/startcrawl/', StartCrawl.as_view(), name='create-a-job')
]