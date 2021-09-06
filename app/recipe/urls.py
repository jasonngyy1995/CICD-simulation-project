from django.urls import path, include
from rest_framework.routers import DefaultRouter
from recipe import views
from .views import IndexView

router = DefaultRouter()
router.register('tags',views.Tagview)
router.register('ingredients',views.IngredientView)
router.register('recipes',views.RecipeView)
app_name = 'recipe'
urlpatterns = [
    path('index',IndexView.as_view()),
    path('', include(router.urls))
]