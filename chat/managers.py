from django.db import models
from django.db.models import Count
#from .models import Message

class ThreadManager(models.Manager):
   # def get_object(self,threadName,Namethread):
       # try:
        #    try:
         #       return Message.objects.filter(thread__name=threadName)
          #  except Message.DoesNotExist:
           #     return Message.objects.filter(thread__name=Namethread)
      #  except Message.DoesNotExist as e:
       #     return Response( {"error":"Given message was not found."},status=404)
    def get_or_create_personal_thread(self, userownersiterid, userfriendsiteid):
        threads = self.get_queryset().filter(thread_type='personal')
        threads = threads.filter(users__in=[userownersiterid, userfriendsiteid]).distinct()
        threads = threads.annotate(u_count=Count('users')).filter(u_count=2)
        if threads.exists():
            return threads.first()
        else:
            thread = self.create(thread_type='personal')
            thread.users.add(userownersiterid)
            thread.users.add(userfriendsiteid)
            return thread

    def by_user(self, user):
        return self.get_queryset().filter(users__in=[user])