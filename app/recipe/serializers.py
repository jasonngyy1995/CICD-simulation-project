from rest_framework import serializers
from core.models import Tag, Ingredient,Recipe

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
    ingredient = serializers.PrimaryKeyRelatedField(
        many = True,
        queryset = Ingredient.objects.all()
    )
    tags = serializers.PrimaryKeyRelatedField(
        many = True,
        queryset = Tag.objects.all()
    )
    
    class Meta:
        model = Recipe
        fields = ('id','name','ingredient','tags','time','price','link')
        read_only_fields = ('id',)

