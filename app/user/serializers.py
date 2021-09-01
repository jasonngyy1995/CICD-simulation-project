from django.contrib.auth import get_user_model
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object"""
    class Meta:
        model = get_user_model()
        fields = ('email','password','name')
        extra_key = {'password':{'write_only':True, 'min_length':6}}

    def create(self,data):
        """Create a new user with vaild password and return it"""
        return get_user_model().objects.create_user(**data)
        