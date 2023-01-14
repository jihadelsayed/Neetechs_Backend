
from rest_framework import serializers

from Cactegory.models import ModelCategory

class CategorySerializer(serializers.ModelSerializer):
	children = serializers.SerializerMethodField()

	class Meta:
		model = ModelCategory
		fields = ('id', 'name', 'parent', 'children','description', 'updatedAt', 'createdAt', 'img')

	def get_children(self, obj):
		children = ModelCategory.objects.filter(parent=obj)
		serializer = self.__class__(children, many=True)
		return serializer.data


class AllCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelCategory
        fields = '__all__'