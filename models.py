import datetime
from flask_mongoengine import MongoEngine
from jsonschema import ValidationError

db = MongoEngine()

article_categories = ["art", "entrepeneurial", "research", "design", "subject"] # Should make this configurable through admin API

def is_valid_category(category):
    if category not in article_categories:
        raise ValidationError("Category \"" + category + "\" is not a valid category")

class Article(db.Document):
    title = db.StringField(max_length=50, required=True)
    authors = db.ListField(db.StringField(max_length=50), required=True)
    students = db.ListField(db.StringField(max_length=50), required=True)
    tags = db.ListField(db.StringField(max_length=30), required=True)
    link = db.URLField()
    category = db.StringField(max_length=30, required=True, validation=is_valid_category)
    description = db.StringField(max_length=140, required=True)
    created = db.DateTimeField(default=datetime.datetime.utcnow, required=True)
    last_updated = db.DateTimeField(required=True)
    favoured = db.FloatField(required=True)
    draft = db.BooleanField(required=True)

    meta = {'indexes': [
        {'fields': ['$title', "$authors", "$tags", "$category", "$description"],
         'default_language': 'english',
         'weights': {'title': 15, 'authors': 10, 'tags': 5, 'category': 20, 'description': 4}
        }
    ]}
