from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from core.models import Recipe, Tag, Ingredient
from recipe.serializers import RecipeSerializer, DetailRecipeSerializer

Recipe_URL = reverse('recipe:recipe-list')

#/api/recipe/recipes/id/
def detail_url(recipe_id):
    """return recipe detail url"""
    return reverse('recipe:recipe-detail',args=[recipe_id])

def sample_tag(user,name='test'):
    """create a sample tag"""
    return Tag.objects.create(user=user,name=name)

def sample_ingredient(user,name='test'):
    """create a sample ingredient"""
    return Ingredient.objects.create(user=user,name=name)

def sample_recipe(user,**params):
    """Create a sample recipe"""
    """create a default recipe"""
    defaults = { 
        'name':'Sample recipe',
        'time': 5,
        'price': 10.00,
    }
    defaults.update(params)
    return Recipe.objects.create(user=user, **defaults)

class PublicRecipeApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        res =self.client.get(Recipe_URL)
        self.assertEqual(res.status_code,status.HTTP_401_UNAUTHORIZED)

class PrivateRecipeApiTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'test@gmail.com'
            'password123'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)
    
    def test_retrieve_recipe(self):
        sample_recipe(user=self.user)
        sample_recipe(user=self.user)
        res=self.client.get(Recipe_URL)
        recipes = Recipe.objects.all().order_by('-id')
        serializer=RecipeSerializer(recipes,many=True)

        self.assertEqual(res.status_code,status.HTTP_200_OK)
        self.assertEqual(res.data,serializer.data)

    def test_create_basic_recipe_success(self):
        """Test create a new recipe"""
        payload = {
            'name':'recipe2',
            'time': 10, 
            'price':8.00,
        }
        res = self.client.post(Recipe_URL, payload)
        self.assertEqual(res.status_code,status.HTTP_201_CREATED)

        recipe = Recipe.objects.get(id=res.data['id'])
        for key in payload.keys():
            self.assertEqual(payload[key],getattr(recipe,key))

    def test_detail_recipe_url(self):
        recipe = sample_recipe(user=self.user)
        recipe.tags.add(sample_tag(user=self.user))
        recipe.ingredients.add(sample_ingredient(user=self.user))
        url =detail_url(recipe.id)
        res =self.client.get(url)

        serializer = DetailRecipeSerializer(recipe)
        self.assertEqual(res.data, serializer.data)

