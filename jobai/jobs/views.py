from rest_framework import generics
from rest_framework.views import APIView
from .models import Jobs
from .serializers import JobSerializer
from .indeed import indeed_crawl
import threading
from rest_framework.response import Response
from rest_framework import status



class JobCreateAPIView(APIView):
    def get(self, request, *args, **kwargs):
        queryset = Jobs.objects.all()
        serializer = JobSerializer(queryset, many=True)
        return Response(serializer.data)


class StartCrawl(APIView):
    def get(self,request,*args,**kwargs):
        threading.Thread(target=indeed_crawl).start()
        return Response("Crawler started!", status=status.HTTP_200_OK)