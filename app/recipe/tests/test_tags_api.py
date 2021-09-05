from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from rest_framework import serializers, status
from rest_framework.test import APIClient
from core.models import Tag
from recipe.serializers import TagSerializer

Tags_URL =reverse('recipe:tag-list')

class PublicTagsApiTest(TestCase):
    """Test the public available tags api"""
    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        res =self.client.get(Tags_URL)
        self.assertEqual(res.status_code,status.HTTP_401_UNAUTHORIZED)

class PrivateTagsApiTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'test@gmail.com'
            'password123'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)
    
    def test_retrieve_tags(self):
        Tag.objects.create(user=self.user,name='Vegan')
        Tag.objects.create(user=self.user,name='Dessert')
        res=self.client.get(Tags_URL)
        tags = Tag.objects.all().order_by('-name')
        serializer=TagSerializer(tags,many=True)
        self.assertEqual(res.status_code,status.HTTP_200_OK)
        self.assertEqual(res.data,serializer.data)

    def test_create_tag_success(self):
        """Test create a new tag"""
        payload = {'name':'Test tag'}
        self.client.post(Tags_URL, payload)
        exists=Tag.objects.filter(
            user = self.user,
            name = payload['name']
        ).exists()
        self.assertTrue(exists)

    