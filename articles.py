import datetime
import os
from flask import Blueprint, current_app, request, g
from mongoengine.context_managers import switch_db
import auth
import models
from article import upload

def from_documents_to_json(documents):
    return '[%s]' % (','.join([doc.to_json() for doc in documents]))

articles_blueprint = Blueprint('/articles', __name__,)

# Retrieve
@articles_blueprint.route("/all", methods=['GET'])
def all_articles():
    with switch_db(models.Article, "default"):
        return from_documents_to_json(models.Article.objects)

@articles_blueprint.route("/search/<search>", methods=['GET'])
def student_search(search):
    with switch_db(models.Article, "default"):
        return from_documents_to_json(models.Article.objects.search_text(search).order_by('$text_score'))
        
@articles_blueprint.route("/student/<student>", methods=['GET'])
def student_article(student):
    with switch_db(models.Article, "default"):
        return from_documents_to_json(models.Article.objects(students=student))

@articles_blueprint.route("/category/<category>", methods=['GET'])
def article_category(category):
    with switch_db(models.Article, "default"):
        return from_documents_to_json(models.Article.objects(category=category))

@articles_blueprint.route("/tag/<tag>", methods=['GET'])
def article_tag(tag):
    with switch_db(models.Article, "default"):
        return from_documents_to_json(models.Article.objects(tags=tag))

@articles_blueprint.route("/create", methods=['POST'])
@auth.is_authorized
def article_upload():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        try:
            json = request.json
            with switch_db(models.Article, "default"):
                article = models.Article(**json)
                article.students = [g.uid]
                article.authors = ["Unknown Full Name Etc", "Other Person"]
                article.favoured = 0
                article.draft = True

                article.last_updated = datetime.datetime.utcnow()

                article.save()

                folder_path = os.path.join(current_app.config['UPLOAD_FOLDER'], str(article.id))
                os.mkdir(folder_path)
 
                return str(article.id)
            
        except Exception as e:
            return str(e), 400

    else:
        return 'Content-Type not supported!'

articles_blueprint.register_blueprint(upload.articles_upload, url_prefix='/upload')