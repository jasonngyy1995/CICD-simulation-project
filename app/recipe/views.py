from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from core.models import Tag
from recipe import serializers

class Tagview(viewsets.GenericViewSet, mixins.ListModelMixin):
    """manage tags in the database"""
    auth_class = (TokenAuthentication,)
    permission_class = (IsAuthenticated,)
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer 

    def get_queryset(self):
        """return objects for the current user"""
        return self.queryset.filter(user=self.request.user).order_by('_name')



