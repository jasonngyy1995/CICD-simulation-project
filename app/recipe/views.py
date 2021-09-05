from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from core.models import Tag, Ingredient, Recipe
from recipe import serializers

class Tagview(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
    """manage tags in the database"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer 

    def get_queryset(self):
        """return objects for the current user"""
        return self.queryset.filter(user=self.request.user).order_by('-name')

    def perform_create(self,serizalizer):
        """Create a new tag"""
        serizalizer.save(user=self.request.user)
 

class IngredientView(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
    """Ingredient in the database"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer

    def get_queryset(self):
        """return objects for the current user"""
        return self.queryset.filter(user=self.request.user).order_by('-name')

    def perform_create(self,serizalizer):
        """Create a new ingredient"""
        serizalizer.save(user=self.request.user)

class RecipeView(viewsets.ModelViewSet):
    """manage recipe in the database"""
    serializer_class = serializers.RecipeSerializer
    queryset = Recipe.objects.all()
    auth_class = (TokenAuthentication,)
    permission = (IsAuthenticated,)

    def get_queryset(self):
        """retrieve the recipes for the authenticated user"""
        return self.queryset.filter(user=self.request.user)

    def get_serializer_class(self):
        """return appropriate serializer class"""
        if self.action == 'retrieve':
            return serializers.DetailRecipeSerializer
        
        return self.serializer_class

    def create_recipe(self,serializer):
        """create a new recipe"""
        serializer.save(user=self.request.user)
        

