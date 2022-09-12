import datetime
from flask_mongoengine import MongoEngine
from jsonschema import ValidationError

db = MongoEngine()

article_categories = ["art", "entrepreneurial", "research", "design", "subjectSpecific"] # Should make this configurable through admin API

def is_valid_category(category):
    if category not in article_categories:
        raise ValidationError("Category \"" + category + "\" is not a valid category")

article_types = ["websiteFiles", "websiteLink", "textEditor"]

def is_valid_article_type(type):
    if type not in article_types:
        raise ValidationError("Articel Type: \"" + type + "\" is not a valid category")

def _not_empty(val):
    if not val:
        raise ValidationError('No inputs can be empty!')

class Article(db.Document):
    title = db.StringField(validation=_not_empty, required=True)
    authors = db.ListField(db.StringField(), required=True)
    students = db.ListField(db.StringField(), required=True)
    question = db.StringField(required=True, validation=_not_empty)
    link = db.URLField()
    type = db.StringField(required=True, validation=is_valid_article_type)
    tags = db.ListField(db.StringField(max_length=30, validation=_not_empty), required=True)
    category = db.StringField(max_length=30, required=True, validation=is_valid_category)
    description = db.StringField(max_length=1000, validation=_not_empty, required=True)
    created = db.DateTimeField(default=datetime.datetime.utcnow, required=True)
    last_updated = db.DateTimeField(required=True)
    favoured = db.FloatField(required=True)
    draft = db.BooleanField(required=True)

    meta = {
        'indexes': [
            {'fields': ['$title', "$authors", "$tags", "$category", "$description", "$question"],
            'default_language': 'english',
            'weights': {'title': 15, 'authors': 10, 'tags': 5, 'category': 20, 'description': 4, 'question': 15}
            }
    ]}