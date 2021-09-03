from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from django.utils.translation import ugettext_lazy as _


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object"""
    class Meta:
        model = get_user_model()
        fields = ('email','password','name')
        extra_key = {'password':{'write_only':True, 'min_length':6}}

    def create(self,data):
        """Create a new user with vaild password and return it"""
        return get_user_model().objects.create_user(**data)
        
class AuthTokenSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField(style = {'input_type':'password'})

    def validate(self,attributes):
        """validate and authenticate the user"""
        email = attributes.get('email')
        password = attributes.get('password')
        user = authenticate(
            request=self.context.get('request'),
            username = email,
            password = password
        )
        if not user:
            message = ('unable to authenticate the user')
            raise serializers.ValidationError(message,code ='authentication')

        attributes['user'] =user
        return attributes