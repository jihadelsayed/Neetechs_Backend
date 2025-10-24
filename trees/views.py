from rest_framework import viewsets, permissions
from .models import Tree
from .serializers import TreeSerializer

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner_id == getattr(request.user, "id", None)



class TreeViewSet(viewsets.ModelViewSet):
    """
    /api/trees [GET, POST]
    /api/trees/{id} [GET, PATCH, DELETE]
    """
    queryset = Tree.objects.all().order_by("-id")
    serializer_class = TreeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        # attach the current user as owner (fallback to first user if unauth)
        user = self.request.user if self.request.user.is_authenticated else None
        serializer.save(owner=user or self._first_user())

    def _first_user(self):
        from django.contrib.auth import get_user_model
        return get_user_model().objects.order_by("id").first()
