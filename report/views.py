from django.shortcuts import render
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView

# Create your views here.
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from knox.auth import TokenAuthentication
from .models import ReportMoudel
from .serializer import ReportSerializer
from rest_framework.response import Response
from rest_framework.views import APIView


class ListReportAPIView(ListAPIView):
    queryset = ReportMoudel.objects.filter()
    serializer_class = ReportSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend,OrderingFilter,SearchFilter]
    filterset_fields = ['title', 'message']
    search_fields = ['title', 'message']
    OrderingFilter = ('title')


class ReportAPIView(ListAPIView):
    def post(self, request):
        data= request.data
        serializer = ReportSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=201)
        return Response(serializer.errors,status=400)