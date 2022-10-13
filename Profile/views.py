from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django_filters.rest_framework import \
    DjangoFilterBackend  # ,SearchFilter,OrderingFilter
from knox.auth import TokenAuthentication
from rest_framework import views, viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import ListAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response

from knox_allauth.models import CustomUser

from .models import Erfarenhet, Intressen, Kompetenser_intyg, Studier
from .serializer import (AllProfileInfoSerializer, ErfarenhetSerializer,
                         IntressenSerializer, Kompetenser_intygSerializer,
                         ProfileSerializer, StudierSerializer)


class ProfilesListAPIView(ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = ProfileSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['site_id','profession']

    filter_backends = [DjangoFilterBackend,SearchFilter,OrderingFilter]
    OrderingFilter = ('first_name')
    filterset_fields = ['first_name', 'site_id', 'about','profession', 'city','state','country']
    search_fields = ['first_name', 'site_id', 'about','profession', 'city','state','country']


class ProfilesAPIView(views.APIView):
    def get(self, request):
        Profiles = CustomUser.objects.all()

        serializer = ProfileSerializer(Profiles,many=True)
        return Response(serializer.data, status=200)
    def post(self, request):
        data= request.data

        serializer = ProfileSerializer(data=data)
        if serializer.is_valid() and int(request.user.id) == int(request.data['username']):
            request.data['picture_medium'] = request.data['picture'] 
            request.data['picture_small'] = request.data['picture'] 
            request.data['picture_tag'] = request.data['picture'] 
            serializer.save()
            return Response(serializer.data,status=201)
        return Response(serializer.errors,status=400)

    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['site_id', 'in_stock']
class AllProfileInfoAPIView(views.APIView):
    def get_object(self,site_id):
        try:
            return CustomUser.objects.get(site_id=site_id)
        except CustomUser.DoesNotExist as e:
            return Response( {"error":"Given Profile was not found."},status=404)
    def get(self, request,site_id=None):
        instance = self.get_object(site_id)
        serializer = AllProfileInfoSerializer(instance)
        return Response(serializer.data, status=200)
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticatedOrReadOnly]

class ProfileAPIView(views.APIView):
    def get_object(self,site_id):
        try:
            return CustomUser.objects.get(site_id=site_id)
        except CustomUser.DoesNotExist as e:
            return Response( {"error":"Given Profile was not found."},status=404)
    def get(self, request,site_id=None):
        instance = self.get_object(site_id)
        serializer = ProfileSerializer(instance)
        return Response(serializer.data, status=200)

    def put(self, request,site_id=None):
        data= request.data
        instance = self.get_object(site_id)
        serializer = ProfileSerializer(instance,data=data)
        if serializer.is_valid():
            request.data['picture_medium'] = request.data['picture'] 
            request.data['picture_small'] = request.data['picture'] 
            request.data['picture_tag'] = request.data['picture'] 
            serializer.save()
            return Response(serializer.data,status=200)
        return Response(serializer.errors,status=400)
    def patch(self, request,site_id=None):
        data= request.data
        instance = self.get_object(site_id)
        print(instance)
        serializer = ProfileSerializer(instance,data=data, partial=True)
        if serializer.is_valid():
            #print(instance)

            #if request.data['picture'] != instance.picture:
             #   request.data['picture_medium'] = request.data['picture'] 
              #  request.data['picture_small'] = request.data['picture'] 
               # request.data['picture_tag'] = request.data['picture']
            serializer.save()
            return Response(serializer.data,status=200)
        return Response(serializer.errors,status=400)
    def delete(self,request,site_id=None):
        instance = self.get_object(site_id)
        instance.delete()
        return HttpResponse(status=204)
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticatedOrReadOnly]

class Kompetenser_intygsListAPIView(ListAPIView):
    queryset = Kompetenser_intyg.objects.all()
    serializer_class = Kompetenser_intygSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name','username','username__site_id']

class Kompetenser_intygsPostAPIView(views.APIView):
    def post(self, request):
        data= request.data
        serializer = Kompetenser_intygSerializer(data=data)
        if serializer.is_valid() and int(request.user.id) == int(request.data['username']):
            serializer.save()
            return Response(serializer.data,status=201)
        return Response(serializer.errors,status=400)

    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticatedOrReadOnly]


class Kompetenser_intygAPIView(views.APIView):
    def get_object(self,id):
        try:
            return Kompetenser_intyg.objects.get(id=id)
        except Kompetenser_intyg.DoesNotExist as e:
            return Response( {"error":"Given Kompetenser_intyg was mot found."},status=404)
    def get(self, request,id=None):
        instance = self.get_object(id)
        serializer = Kompetenser_intygSerializer(instance)
        return Response(serializer.data, status=200)

    def put(self, request,id=None):
        data= request.data
        instance = self.get_object(id)
        serializer = Kompetenser_intygSerializer(instance,data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=200)
        return Response(serializer.errors,status=400)
    def delete(self,request,id=None):
        instance = self.get_object(id)
        instance.delete()
        return HttpResponse(status=204)
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticatedOrReadOnly]

class IntressensListAPIView(ListAPIView):
    queryset = Intressen.objects.all()
    serializer_class = IntressenSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name','username','username__site_id']
    pagination_class = LimitOffsetPagination

class IntressensPostAPIView(views.APIView):
    def post(self, request):
        data= request.data
        serializer = IntressenSerializer(data=data)
        if serializer.is_valid() and int(request.user.id) == int(request.data['username']):
            serializer.save()
            return Response(serializer.data,status=201)
        return Response(serializer.errors,status=400)

    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticatedOrReadOnly]

class IntressenAPIView(views.APIView):
    def get_object(self,id):
        try:
            return Intressen.objects.get(id=id)
        except Intressen.DoesNotExist as e:
            return Response( {"error":"Given Intressen was mot found."},status=404)
    def get(self, request,id=None):
        instance = self.get_object(id)
        serializer = IntressenSerializer(instance)
        return Response(serializer.data, status=200)

    def put(self, request,id=None):
        data= request.data
        instance = self.get_object(id)
        serializer = IntressenSerializer(instance,data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=200)
        return Response(serializer.errors,status=400)
    def delete(self,request,id=None):
        instance = self.get_object(id)
        instance.delete()
        return HttpResponse(status=204)
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticatedOrReadOnly]



class StudiersListAPIView(ListAPIView):
    queryset = Studier.objects.all()
    serializer_class = StudierSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name','username','username__site_id']

class StudiersPostAPIView(views.APIView):
    def post(self, request):
        data= request.data
        serializer = StudierSerializer(data=data)
       # print(request.data['username'])
        if serializer.is_valid() and int(request.user.id) == int(request.data['username']):
            serializer.save()
            return Response(serializer.data,status=201)
        return Response(serializer.errors,status=400)

    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticatedOrReadOnly]

class userStudierAPIView(views.APIView):
    
    def get_object(self,site_id):
        try:
            return Intressen.objects.get(site_id__site_id=site_id)
        except Intressen.DoesNotExist as e:
            return Response( {"error":"Given userStudierAPIView was mot found."},status=404)
    def get(self, request,site_id=None):
        instance = self.get_object(site_id)
        serializer = StudierSerializer(instance)
        return Response(serializer.data, status=200)
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookupfield = 'site_id'

class StudierAPIView(views.APIView):
    def get_object(self,id):
        try:
            return Studier.objects.get(id=id)
        except Studier.DoesNotExist as e:
            return Response( {"error":"Given Studier was mot found."},status=404)
    def get(self, request,id=None):
        instance = self.get_object(id)
        serializer = StudierSerializer(instance)
        return Response(serializer.data, status=200)

    def put(self, request,id=None):
        data= request.data
        instance = self.get_object(id)
        serializer = StudierSerializer(instance,data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=200)
        return Response(serializer.errors,status=400)
    def delete(self,request,id=None):
        instance = self.get_object(id)
        instance.delete()
        return HttpResponse(status=204)
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticatedOrReadOnly]

class ErfarenhetsListAPIView(ListAPIView):
    queryset = Erfarenhet.objects.all()
    serializer_class = ErfarenhetSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name','username','username__site_id']
    pagination_class = LimitOffsetPagination

class ErfarenhetsPostAPIView(views.APIView):
    def post(self, request):
        data= request.data
        serializer = ErfarenhetSerializer(data=data)
        
        if serializer.is_valid() and int(request.user.id) == int(request.data['username']):
            serializer.save()
            return Response(serializer.data,status=201)
        return Response(serializer.errors,status=400)

    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticatedOrReadOnly]

class ErfarenhetAPIView(views.APIView):
    def get_object(self,id):
        try:
            return Erfarenhet.objects.get(id=id)
        except Erfarenhet.DoesNotExist as e:
            return Response( {"error":"Given Erfarenhet was mot found."},status=404)
    def get(self, request,id=None):
        instance = self.get_object(id)
        serializer = ErfarenhetSerializer(instance)
        return Response(serializer.data, status=200)

    def put(self, request,id=None):
        data= request.data
        instance = self.get_object(id)
        #print(instance)
        serializer = ErfarenhetSerializer(instance, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=200)
        return Response(serializer.errors,status=400)
    def delete(self,request,id=None):
        instance = self.get_object(id)
        instance.delete()
        return HttpResponse(status=204)
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticatedOrReadOnly]