from rest_framework import serializers

from chat.models import Message, Thread
from knox_allauth.models import CustomUser

class MessageSerializers(serializers.ModelSerializer):
    sender_name = serializers.SerializerMethodField(source="site_id.site_id")
    created_at = serializers.DateTimeField(format='%Y-%m-%d %I:%M %p')
    #19‏/02‏/2021 11:06 ص
    def get_sender_name(self, obj):
        return obj.sender.site_id
    class Meta:
        model = Message
        fields = ('created_at', 'id','orderId','type', 'thread', 'sender', 'updated_at', 'text','sender_name','created_at')
        #fields = '__all__','site_id'

class ThreadSerializers(serializers.ModelSerializer):
    FriendName = serializers.SerializerMethodField('get_friend_name')
    FriendImg = serializers.SerializerMethodField('get_friend_img')
    LastMessageText = serializers.SerializerMethodField('get_last_message')
    LastMessageDate = serializers.SerializerMethodField('get_last_message_date')
    created_at = serializers.DateTimeField(format='%Y-%m-%d %I:%M %p')

    class Meta:
        model = Thread
        fields = ('created_at', 'id','LastMessageText', 'LastMessageDate', 'ThreadName', 'thread_type', 'updated_at', 'users','FriendName','FriendImg')
    
    def get_friend_name(self, obj):
        friend_site_id = obj.ThreadName.replace(self.context['request'].user.site_id, "")
        if friend_site_id == "":
            FriendName = CustomUser.objects.get(site_id=self.context['request'].user.site_id).first_name
        else:
            FriendName = CustomUser.objects.get(site_id=friend_site_id).first_name
        return FriendName
    
    def get_last_message(self, obj):
        last_message = Message.objects.filter(thread__ThreadName=obj.ThreadName).last().text
        return last_message
        
    def get_last_message_date(self, obj):
        last_message_date = Message.objects.filter(thread__ThreadName=obj.ThreadName).last().created_at.strftime("%Y-%m-%d %I:%M %p")
        print(last_message_date)
        return last_message_date
        
    def get_friend_img(self, obj):
        friend_site_id = obj.ThreadName.replace(self.context['request'].user.site_id, "")
        if friend_site_id == "":
            FriendImg = CustomUser.objects.get(site_id=self.context['request'].user.site_id).picture.url
        else:
            FriendImg = CustomUser.objects.get(site_id=friend_site_id).picture.url
        return FriendImg




