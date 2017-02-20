from __future__ import unicode_literals

from django.utils.text import slugify
from django.utils.timezone import now
from mongoengine import *

DIFFICULTY_EASY = 1
DIFFICULTY_MEDIUM = 2
DIFFICULTY_HARD = 3
DIFFICULTIES = (
    (DIFFICULTY_EASY, u'easy'),
    (DIFFICULTY_MEDIUM, u'normal'),
    (DIFFICULTY_HARD, u'hard'),
)

UNITS = (
    (1, u'grams'),
    (2, u'ml')
)


# Create your models here.
class Comment(EmbeddedDocument):
    """

    """
    content = StringField()
    name = StringField(max_length=100)


class Category(EmbeddedDocument):
    """
    A model class describing a category.
    """
    name = StringField(max_length=100)
    description = StringField(null=True)

    def __str__(self):
        return self.name


class Ingredient(EmbeddedDocument):
    """
    A model class describing a recipe ingredient.
    """
    name = StringField(max_length=50)
    description = StringField(null=True)
    quantity = IntField(help_text=u'In grams/ml')
    unit = IntField(choices=UNITS, default=1)


class Recipe(Document):
    """
    A model describing a cookbook recipe.
    """
    title = StringField(max_length=255, required=True)
    slug = StringField(unique=True, max_length=300, null=True)
    ingredients = ListField(EmbeddedDocumentField(Ingredient))
    preparation = StringField(required=True)
    time_for_preparation = IntField(verbose_name=u'Preparation time',
                                    help_text=u'In minutes', null=True)
    number_of_portions = IntField()
    difficulty = IntField(verbose_name=u'Difficulty', choices=DIFFICULTIES, default=DIFFICULTY_MEDIUM)
    category = ListField(EmbeddedDocumentField(Category))
    comments = ListField(EmbeddedDocumentField(Comment))
    author = ReferenceField('User', reverse_delete_rule=CASCADE, verbose_name=u'Author', null=True)
    date_created = DateTimeField(default=now())
    date_updated = DateTimeField(default=now())

    meta = {
        "index": ["slug"],
        "ordering": ["-date_created"]
    }

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Recipe, self).save(*args, **kwargs)

    def modify(self, *args, **update):
        self.date_updated = now()
        super(Recipe, self).modify(*args, **update)

    def __str__(self):
        return self.title
