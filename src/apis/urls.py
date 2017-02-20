from django.conf.urls import include, url
from .views import RecipeList, CategoryList, RecipeDetail

urlpatterns = [
    url(r'recipes/$', RecipeList.as_view(), name="recipe-list"),
    url(r'categories/$', CategoryList.as_view(), name="category-list"),
    url(r'^recipes/(?P<slug>[-\w]+)/$', RecipeDetail.as_view(), name="recipe-detail"),

]