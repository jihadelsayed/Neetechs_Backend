
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from Category.models import ModelCategory


class ChildCategorySerializer(serializers.ModelSerializer):
	"""Serializer used for documenting nested child categories."""
	children = serializers.SerializerMethodField()

	class Meta:
		model = ModelCategory
		fields = ('id', 'name', 'parent', 'children','description', 'updatedAt', 'createdAt', 'img')
		ref_name = "CategoryChild"

	@extend_schema_field('CategoryChild')
	def get_children(self, obj):
		children = ModelCategory.objects.filter(parent=obj)
		serializer = ChildCategorySerializer(children, many=True, context=self.context)
		return serializer.data


class CategorySerializer(serializers.ModelSerializer):
	"""
	Serializes ModelCategory instances.
	Includes a 'children' field that recursively serializes child categories,
	allowing for a nested representation of the category hierarchy.
	"""
	children = serializers.SerializerMethodField() # Defines a custom field that gets its value from the get_children method.

	class Meta:
		model = ModelCategory
		# Specifies the fields to include in the serialized output,
		# including the custom 'children' field for nested categories.
		fields = ('id', 'name', 'parent', 'children','description', 'updatedAt', 'createdAt', 'img')

	@extend_schema_field(ChildCategorySerializer(many=True))
	def get_children(self, obj):
		"""
		Retrieves and serializes the direct children of a given category instance.
		This method is called by the 'children' SerializerMethodField.
		"""
		children = ModelCategory.objects.filter(parent=obj)
		# Recursively uses the same serializer for children to maintain consistency.
		serializer = ChildCategorySerializer(children, many=True, context=self.context)
		return serializer.data


class AllCategorySerializer(serializers.ModelSerializer):
    """
    Serializes ModelCategory instances, including all fields from the model.
    This provides a complete representation of a category without any custom nesting.
    """
    class Meta:
        model = ModelCategory
        fields = '__all__' # Includes all fields from ModelCategory.
