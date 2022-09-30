from django.utils import timezone
from contextvars import Token
from Checkout.models import ServiceOrder
from channels.consumer import SyncConsumer, AsyncConsumer
from asgiref.sync import async_to_sync, sync_to_async
from knox.auth import TokenAuthentication
from knox_allauth.models import CustomUser
from chat.models import Thread, Message
import json
from channels.db import database_sync_to_async
# from push_notifications.models import

from fcm_django.models import FCMDevice


class ChatConsumer(AsyncConsumer):
    room_name = ""

    async def websocket_connect(self, event):

        self.authidd = self.scope["url_route"]["kwargs"]['authkey']
    #    device = GCMDevice(name=device_name, user=user, device_id=device_id, registration_id=device_registration_id)
    #    device.save()
    #    devices = GCMDevice.objects.filter(user=user)
    #    devices.send_message("Push notification message!")
        if await sync_to_async(auth_key_is_expired)(self.authidd) == True:
            await self.send({
                "type": "websocket.send",
                "text": "invalidToken"
            })
        else:
            self.userowner = await sync_to_async(get_user_from_auth_key)(self.authidd)
            await self.send({
                'type': 'websocket.accept'
            })
            print(f'[{self.channel_name}] - has been connected')
            # print(event)

    async def websocket_receive(self, event):
        # json translator
        self.ReceivedData = json.loads(event["text"])
        # notification type is chating
        if self.ReceivedData['notificationType'] == "Chat":
            print(f'[{self.channel_name}] - recieved messag - {event["text"]}')
            self.friendusername = self.ReceivedData['friendUsername']
            self.message = self.ReceivedData['message']
            print("hello", self.userowner, self.friendusername)
            self.thread_obj = await sync_to_async(get_or_create_personal_thread)(self.userowner, self.friendusername)
            self.room_name = self.thread_obj.ThreadName
            await self.channel_layer.group_add(self.room_name, self.channel_name)
            msg = json.dumps({
                'text': event.get('text'),
                'username': self.userowner
            })
            await storeMessage(self, self.message)
            await sendNotification(self, self.message, self.friendusername, self.userowner, self.room_name)

        if self.ReceivedData['notificationType'] == "Order":
            print(f'[{self.channel_name}] - recieved messag - {event["text"]}')
            self.friendusername = self.ReceivedData['friendUsername']
            self.message = self.ReceivedData['message']
            print("hello", self.userowner, self.friendusername)
            self.thread_obj = await sync_to_async(get_or_create_personal_thread)(self.userowner, self.friendusername)
            self.room_name = self.thread_obj.ThreadName
            await self.channel_layer.group_add(self.room_name, self.channel_name)
            msg = json.dumps({
                'text': event.get('text'),
                'username': self.userowner
            })
            await storeOrder(self, self.message)
            await sendNotification(self, self.message, self.friendusername, self.userowner)

        if self.ReceivedData['notificationType'] == "dss":
            print(f'[{self.channel_name}] - recieved messag - {event["text"]}')
            self.friendusername = self.ReceivedData['friendUsername']
            self.message = self.ReceivedData['message']
            print("hello", self.userowner, self.friendusername)
            self.thread_obj = await sync_to_async(get_or_create_personal_thread)(self.userowner, self.friendusername)
            self.room_name = self.thread_obj.ThreadName
            await self.channel_layer.group_add(self.room_name, self.channel_name)
            msg = json.dumps({
                'text': event.get('text'),
                'username': self.userowner
            })
            await storeMessage(self, self.message)
        await self.channel_layer.group_send(
            self.room_name, {
                'type': 'websocket.message',
                # 'type': 'websocket.send',
                'text': event.get('text')
            }
        )

        # async_to_sync(channel_layer.group_send)('broadcast',{'type':'websocket.message','text':'message from the shell'})

    async def websocket_message(self, event):
        print(f'[{self.channel_name}] - sent message  - {event["text"]}')
        await self.send({
            "type": "websocket.send",
            "text": event["text"]
        })
       # await async_to_sync(self.channel_layer.group_add(self.room_name, self.channel_name))

    async def websocket_disconnect(self, event):
        print(f'[{self.channel_name}] - has been disconnected')
        await self.channel_layer.group_discard(self.room_name, self.channel_name)
        print("Connect is disconnect")


def get_or_create_personal_thread(userowner, friendusername):
    threadName = userowner+friendusername
    Namethread = friendusername+userowner
    print("thread =" + threadName)
    try:
        try:
            return Thread.objects.get(ThreadName=threadName)
        except Thread.DoesNotExist:
            return Thread.objects.get(ThreadName=Namethread)
    except Thread.DoesNotExist:
        user1 = CustomUser.objects.get(site_id=userowner)
        user2 = CustomUser.objects.get(site_id=friendusername)
        thread = Thread.objects.create(ThreadName=threadName)
        thread.users.add(user1)
        thread.users.add(user2)
        print(thread)
        return thread


@database_sync_to_async
def storeMessage(self, text):
    threadid = Thread.objects.get(ThreadName=self.thread_obj.ThreadName)
    userid = CustomUser.objects.get(site_id=self.userowner)
    Message.objects.create(thread=threadid, sender=userid, text=text)


@database_sync_to_async
def sendNotification(self, messag, friend, owner, room_name):
    from firebase_admin import messaging
    from firebase_admin.messaging import Notification
    friendusername = CustomUser.objects.get(site_id=friend).pk
    friendusernameTest = CustomUser.objects.get(site_id=friend)
    print(friendusername)

    FCMDevice.objects.filter(user=friendusername, active=True).send_message(
        messaging.Message(notification=Notification(title=owner, body=messag), data={
            "title": owner,
            "body": messag,
            "detailsId": room_name,
        }
        )
    )
    FCMDevice.objects.filter(user=friendusernameTest, active=True).send_message(
        messaging.Message(notification=Notification(title=owner, body=messag), data={
            "title": owner,
            "body": messag,
            "detailsId": room_name,
        }
        )
    )
    # for device in devices:
    # single_result = device.send_message(Message(notification=Notification(title="test ios4", body="test body4"),
    #   data={"title": "test ios5", "body": "test body5","view": "DEVICE","id": "4"},)
    # device.send_message(self,owner, messag)  token = device.registration_id
    # deviceId=str(device.registration_id)
    #send = devices.send_message(title=owner, body=messag, badge=1)
    # print(send)

    # print(devices.registration_id)
    #device.send_message(message={"title" : owner, "body" : messag}, extra={"foo": "bar"}, badge=1)
    # device.send_message({'message':messag})


@database_sync_to_async
def storeOrder(self, text):
    threadid = Thread.objects.get(ThreadName=self.thread_obj.ThreadName)
    #userid = CustomUser.objects.get(site_id=self.userowner)
    ServiceOrder.objects.create(
        thread=threadid, customerIdd=self.userowner, employedIdd=self.friendusername)


def get_user_from_auth_key(token):
    """
    Gets the user from current User model using the passed session_key
    :param session_key: django.contrib.sessions.models.Session - session_key
    :return: User instance or None if not found
    """
    # print(token[:8])
    # print(token)
    # digest="3c56d2304c793061fe60ac5427daa84a4cdbcd823c8e0561fabf089119279ade55adabee922d8b4fcf037aaa3049bbd58d0c9f766ae4ec18479e0eaee2b8eaa7"
    token_key = TokenAuthentication.model.objects.get(token_key=token[:8])
    if token_key:
        uid = token_key.user_id
        user = CustomUser.objects.filter(id=uid).first()
        site_id = token_key.user.site_id
        return site_id
    else:
        return None


def auth_key_is_expired(token):
    # print(token)
    # digest="3c56d2304c793061fe60ac5427daa84a4cdbcd823c8e0561fabf089119279ade55adabee922d8b4fcf037aaa3049bbd58d0c9f766ae4ec18479e0eaee2b8eaa7"
   # token_key = TokenAuthentication.model.objects.get(token_key=token[:8], expiry__gt=timezone.now())
    token_key = TokenAuthentication.model.objects.get(token_key=token[:8])

    if token_key:
        expiry = token_key.expiry
        now = timezone.now()
        if expiry >= now:
            return False
        else:
            return True
    else:
        return True
