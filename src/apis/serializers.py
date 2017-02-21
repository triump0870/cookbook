from recipes.models import Recipe, Category, Comment, Ingredient
from rest_framework_mongoengine.serializers import DocumentSerializer, EmbeddedDocumentSerializer
import json
from django.forms.models import model_to_dict
from bson.objectid import ObjectId
from mongoengine import connect
from os import environ as env

_MONGODB_USER = env.get("MONGODB_USER")
_MONGODB_PASSWD = env.get("MONGODB_PASSWD")
_MONGODB_HOST = env.get("MONGODB_HOST")
_MONGODB_NAME = env.get("MONGODB_NAME")
_MONGODB_PORT = env.get("MONGODB_PORT")
_MONGODB_DATABASE_HOST = \
    'mongodb://%s:%s@%s:%s/%s' \
    % (_MONGODB_USER, _MONGODB_PASSWD, _MONGODB_HOST, _MONGODB_PORT, _MONGODB_NAME)

db = connect(_MONGODB_NAME, host=_MONGODB_DATABASE_HOST)


class CommentSerializer(EmbeddedDocumentSerializer):
    class Meta:
        model = Comment
        fields = ("name", "content")


class CategorySerializer(EmbeddedDocumentSerializer):
    class Meta:
        model = Category
        fields = ('name', 'description')


class IngredientSerializer(EmbeddedDocumentSerializer):
    class Meta:
        model = Ingredient
        fields = ('name', 'description', 'quantity', 'unit')


class RecipeSerializer(DocumentSerializer):
    categories = CategorySerializer(source='category', many=True)
    comment = CommentSerializer(source='comments', many=True)
    ingredient = IngredientSerializer(source='ingredients', many=True)

    class Meta:
        model = Recipe
        fields = ('id', 'title', 'ingredient', 'preparation', 'time_for_preparation',
                  'number_of_portions', 'difficulty', 'categories', 'comment')

        depth = 2

    def to_representation(self, instance):
        data = super(RecipeSerializer, self).to_representation(instance)
        data['slug'] = instance.slug
        return data

    def create(self, validated_data):
        categories = validated_data.pop('category')
        ingredients = validated_data.pop('ingredients')
        updated_instance = super(RecipeSerializer, self).create(validated_data)

        for ingredient in ingredients:
            updated_instance.ingredients.append(Ingredient(**ingredient))
        for category in categories:
            updated_instance.category.append(Category(**category))

        updated_instance.save()
        return updated_instance

    def update(self, instance, validated_data):
        comments = validated_data.pop("comments")
        for comment in comments:
            instance.comments.append(Comment(**comment))

        instance.save()
        return instance
