from chat.models import Message, Thread
from chat.serializers import MessageListSerializer, MessageSerializer, ThreadSerializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from knox.auth import TokenAuthentication
from rest_framework import status, viewsets
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from drf_spectacular.utils import OpenApiResponse, extend_schema

class ThreadViewSet(viewsets.ModelViewSet):
    serializer_class = ThreadSerializers
    queryset = Thread.objects.all()
    authentication_classes = (TokenAuthentication,)

    def get_queryset(self):
        request = getattr(self, "request", None)
        if (
            getattr(self, "swagger_fake_view", False)
            or not request
            or not getattr(request, "user", None)
            or not request.user.is_authenticated
        ):
            return Thread.objects.none()
        return Thread.objects.filter(users=request.user).order_by("-updated_at")
    permission_classes = [IsAuthenticated]


#class ThreadsAPIView(views.APIView):
 #   def get(self, request,site_id=None):
  #      current_user = self.request.user.site_id
   #     threadName = current_user + site_id
    #    print(threadName)
     #   try:
           # user = Thread.objects.get(users)
            #site_id = User.objects.get(site_id=user)
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

class MessagesAPIView(GenericAPIView):
    serializer_class = MessageListSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated]

    def _thread(self):
        if not hasattr(self, "_thread_cache"):
            thread_uuid = self.kwargs.get("thread_id")
            self._thread_cache = get_object_or_404(Thread, uuid=thread_uuid)
        return self._thread_cache

    def get_queryset(self):
        request = getattr(self, "request", None)
        if (
            getattr(self, "swagger_fake_view", False)
            or not request
            or not getattr(request, "user", None)
            or not request.user.is_authenticated
        ):
            return Message.objects.none()

        if not self.kwargs.get("thread_id"):
            return Message.objects.none()

        thread = self._thread()
        if not thread.users.filter(id=request.user.id).exists():
            return Message.objects.none()

        queryset = Message.objects.filter(thread=thread).order_by("created_at")
        return queryset

    @extend_schema(
        responses=MessageListSerializer,
        operation_id="chat_thread_messages_list",
    )
    def get(self, request, thread_id=None):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        request=MessageSerializer,
        responses=MessageSerializer,
        operation_id="chat_thread_message_create",
    )
    def post(self, request, thread_id=None, *args, **kwargs):
        thread = self._thread()
        if not thread.users.filter(id=request.user.id).exists():
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = MessageSerializer(data=request.data, context=self.get_serializer_context())
        serializer.is_valid(raise_exception=True)
        serializer.save(thread=thread)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MessageAPIView(GenericAPIView):
    serializer_class = MessageSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Message.objects.none()
        queryset = Message.objects.all()
        thread_uuid = self.kwargs.get("thread_id")
        if thread_uuid:
            queryset = queryset.filter(thread__uuid=thread_uuid)
        return queryset

    def get_object(self):
        return get_object_or_404(self.get_queryset(), uuid=self.kwargs.get("message_id"))

    @extend_schema(
        responses=MessageSerializer,
        operation_id="chat_thread_message_retrieve",
    )
    def get(self, request, thread_id=None, message_id=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        request=MessageSerializer,
        responses=MessageSerializer,
        operation_id="chat_thread_message_update",
    )
    def put(self, request, thread_id=None, message_id=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        request=None,
        responses={204: OpenApiResponse(description="Deleted")},
        operation_id="chat_thread_message_delete",
    )
    def delete(self, request, thread_id=None, message_id=None):
        instance = self.get_object()
        instance.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)
