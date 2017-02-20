from recipes.models import Recipe, Category, Comment, Ingredient
from rest_framework_mongoengine.serializers import DocumentSerializer, EmbeddedDocumentSerializer


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
        updated_instance = super(RecipeSerializer, self).update(instance, validated_data)

        for comment in comments:
            updated_instance.comments.append(Comment(**comment))

        updated_instance.save()
        return updated_instance
