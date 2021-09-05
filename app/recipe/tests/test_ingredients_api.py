from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from core.models import Ingredient
from recipe.serializers import IngredientSerializer

Ingredient_URL =reverse('recipe:ingredient-list')

class PublicIngredientsApiTest(TestCase):
    """Test the public available ingredients api"""
    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        res =self.client.get(Ingredient_URL)
        self.assertEqual(res.status_code,status.HTTP_401_UNAUTHORIZED)

class PrivateIngredientsApiTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'test@gmail.com'
            'password123'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)
    
    def test_retrieve_ingredients(self):
        Ingredient.objects.create(user=self.user,name='Egg')
        Ingredient.objects.create(user=self.user,name='Salt')
        res=self.client.get(Ingredient_URL)
        ingredients = Ingredient.objects.all().order_by('-name')
        serializer=IngredientSerializer(ingredients,many=True)
        self.assertEqual(res.status_code,status.HTTP_200_OK)
        self.assertEqual(res.data,serializer.data)

    def test_create_ingredient_success(self):
        """Test create a new ingredients"""
        payload = {'name':'Test ingredient'}
        self.client.post(Ingredient_URL, payload)
        exists=Ingredient.objects.filter(
            user = self.user,
            name = payload['name'],
        ).exists()
        self.assertTrue(exists)