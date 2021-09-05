"""from app.recipe.views import RecipeView"""
from rest_framework import serializers
from core.models import Tag, Ingredient, Recipe

class TagSerializer(serializers.ModelSerializer):
    """Serializer for tag objects"""

    class Meta:
        model = Tag
        fields =('id','name')
        read_only_fields = ('id',)

class IngredientSerializer(serializers.ModelSerializer):
    """Serializer the ingredient"""
    class Meta:
        model = Ingredient
        fields =('id','name')
        read_only_fields = ('id',)

class RecipeSerializer(serializers.ModelSerializer):
    """Serializer the recipe"""
    ingredients = serializers.PrimaryKeyRelatedField(
        many = True,
        queryset = Ingredient.objects.all()
    )
    tags = serializers.PrimaryKeyRelatedField(
        many = True,
        queryset = Tag.objects.all()
    )

    class Meta:
        model = Recipe
        fields = ('id','name','ingredients','tags','time','price','link')
        read_only_fields = ('id',)

class DetailRecipeSerializer(RecipeSerializer):
    """seralizer the recipe detail"""
    ingredients = IngredientSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)