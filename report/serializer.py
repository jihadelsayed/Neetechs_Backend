from rest_framework import serializers
from .models import ReportMoudel

class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportMoudel
        fields = ('id','addedAt','updatedAt','title','orderNumber','type','message','image')
    
    def validate(self, attrs):
        if len(attrs['title']) < 3:
            raise serializers.ValidationError("the title muste be loonger")
        if len(attrs['message']) < 10:
            raise serializers.ValidationError("you should write more info")
        return attrs
		

