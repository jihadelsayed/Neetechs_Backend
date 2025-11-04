from chat.models import Thread, Message
from rest_framework import viewsets,views
from chat.serializers import MessageSerializers, ThreadSerializers
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from knox.auth import TokenAuthentication
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse,HttpResponse
from knox_allauth.models import CustomUser
from django.contrib.auth import get_user_model

class ThreadViewSet(viewsets.ModelViewSet):
    serializer_class = ThreadSerializers
    queryset = Thread.objects.all()
    authentication_classes = (TokenAuthentication,)

    def get_queryset(self):
        user = self.request.user
        print(user)
        queryset = Thread.objects.filter(users=user).order_by("-updated_at")
        return queryset
    permission_classes = [IsAuthenticated]


#class ThreadsAPIView(views.APIView):
 #   def get(self, request,site_id=None):
  #      current_user = self.request.user.site_id
   #     threadName = current_user + site_id
    #    print(threadName)
     #   try:
           # user = Thread.objects.get(users)
            #site_id = CustomUser.objects.get(site_id=user)
    #        th = Thread.objects.filter(ThreadName=threadName)
     #   except Thread.DoesNotExist as e:
      #      return Response( {"error":"Given Thread was not found."},status=404)


       # instance = th
        #serializer = ThreadSerializers(instance,many=True)
#        return Response(serializer.data, status=200)
 #   def post(self, request):
  #      data= request.data
   #     serializer = ThreadSerializers(data=data)
    #    if serializer.is_valid():
     #       serializer.save()
      #      return Response(serializer.data,status=201)
       # return Response(serializer.errors,status=400)

class MessagesAPIView(views.APIView):
    def get_object(self,threadName,Namethread):
        try:
            if Message.objects.filter(thread__ThreadName=Namethread).first() == None:
                return Message.objects.filter(thread__ThreadName=threadName)
            else:
                return Message.objects.filter(thread__ThreadName=Namethread)
        except Message.DoesNotExist as e:
            return Response( {"error":"Given message was not found."},status=404)
    def get(self, request,site_id=None):
        current_user = self.request.user.site_id
        threadName = current_user + site_id
        Namethread = site_id + current_user
        instance = self.get_object(threadName,Namethread)
        serializer = MessageSerializers(instance,many=True)
        return Response(serializer.data, status=200)

    def post(self, request):
        data= request.data
        serializer = MessageSerializers(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=201)
        return Response(serializer.errors,status=400)

    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated]

class MessageAPIView(views.APIView):
    def get_object(self,id):
        try:
            return Message.objects.get(id=id)
        except Message.DoesNotExist as e:
            return Response( {"error":"Given message was mot found."},status=404)
    def get(self, request,id=None):
        instance = self.get_object(id)
        serializer = MessageSerializers(instance,many=True)
        return Response(serializer.data, status=200)

    def put(self, request,id=None):
        data= request.data
        instance = self.get_object(id)
        serializer = MessageSerializers(data=data)
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

