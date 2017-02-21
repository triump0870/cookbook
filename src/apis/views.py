from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView
from apis.serializers import RecipeSerializer, CategorySerializer
from recipes.models import Recipe, Category
from rest_framework_mongoengine.generics import RetrieveUpdateDestroyAPIView
from rest_framework.response import Response


# Create your views here.
class CategoryList(ListCreateAPIView):
    serializer_class = CategorySerializer
    # queryset = Category.find()


class RecipeList(ListCreateAPIView):
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()
    lookup_field = 'slug'


class RecipeDetail(RetrieveUpdateDestroyAPIView):
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()
    lookup_field = 'slug'