from chat.managers import ThreadManager
from django.db import models
from Neetechs import settings
class TrackingModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Thread(TrackingModel):
    THREAD_TYPE = (
        ('personal', 'Personal'),
        ('group', 'Group')
    )

    ThreadName = models.CharField(max_length=50, null=True, blank=True)
    thread_type = models.CharField(max_length=15, choices=THREAD_TYPE, default='personal')
    users = models.ManyToManyField(settings.AUTH_USER_MODEL)

    objects = ThreadManager()

    def __str__(self) -> str:
        if self.thread_type == 'personal' and self.users.count() == 2:
            return f'{self.users.first()} and {self.users.last()}'
        return f'{self.ThreadName}'

class Message(TrackingModel):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField(blank=False, null=False)
    orderId = models.TextField(default="none")
    type = models.TextField(default="none")
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'From <Thread - {self.thread}>'