from datetime import date, datetime
import os
from flask import Blueprint, current_app, request, g
from mongoengine.context_managers import switch_db
import auth
import models
from mongoengine.queryset.visitor import Q
from article import upload, modify

def from_documents_to_json(documents):
    return '[%s]' % (','.join([doc.to_json() for doc in documents]))

articles_blueprint = Blueprint('/articles', __name__,)

# Retrieve
@articles_blueprint.route("/all", methods=['GET'])
def all_articles():
    args = request.args
    with switch_db(models.Article, "default"):
        if args.get("date_start") and args.get("date_end"):
            return from_documents_to_json(models.Article.objects(
                Q(created__lte=date.fromisoformat(args.get("date_end"))) & 
                Q(created__gte=date.fromisoformat(args.get("date_start")))).order_by('authors'))
        else:
            return from_documents_to_json(models.Article.objects.order_by('authors'))

@articles_blueprint.route("/search/<search>", methods=['GET'])
def student_search(search):
    args = request.args
    with switch_db(models.Article, "default"):
        if args.get("date_start") and args.get("date_end"):
            return from_documents_to_json(models.Article.objects(
                Q(created__lte=date.fromisoformat(args.get("date_end"))) & 
                Q(created__gte=date.fromisoformat(args.get("date_start")))).search_text(search).order_by('$text_score'))
        else:
            return from_documents_to_json(models.Article.objects.search_text(search).order_by('$text_score'))
        
@articles_blueprint.route("/student/<student>", methods=['GET'])
def student_article(student):
    args = request.args
    with switch_db(models.Article, "default"):
        if args.get("date_start") and args.get("date_end"):
            return from_documents_to_json(models.Article.objects(
                Q(created__lte=date.fromisoformat(args.get("date_end"))) & 
                Q(created__gte=date.fromisoformat(args.get("date_start"))) &
                Q(students=student)).order_by('authors'))
        else:
            return from_documents_to_json(models.Article.objects.order_by('authors'))

@articles_blueprint.route("/category/<category>", methods=['GET'])
def article_category(category):
    args = request.args
    with switch_db(models.Article, "default"):
        if args.get("date_start") and args.get("date_end"):
            return from_documents_to_json(models.Article.objects(
                Q(created__lte=date.fromisoformat(args.get("date_end"))) & 
                Q(created__gte=date.fromisoformat(args.get("date_start"))) &
                Q(category=category)).order_by('authors'))
        else:
            return from_documents_to_json(models.Article.objects.order_by('authors'))

@articles_blueprint.route("/tag/<tag>", methods=['GET'])
def article_tag(tag):
    args = request.args
    with switch_db(models.Article, "default"):
        if args.get("date_start") and args.get("date_end"):
            return from_documents_to_json(models.Article.objects(
                Q(created__lte=date.fromisoformat(args.get("date_end"))) & 
                Q(created__gte=date.fromisoformat(args.get("date_start"))) &
                Q(tags=tag)).order_by('authors'))
        else:
            return from_documents_to_json(models.Article.objects.order_by('authors'))

@articles_blueprint.route("/owned", methods=['GET'])
@auth.is_authorized
def article_owned():
    print(g.uid)
    with switch_db(models.Article, "default"):
        return from_documents_to_json(models.Article.objects(students=g.uid).order_by('authors'))

@articles_blueprint.route("/create", methods=['POST'])
@auth.is_authorized
@auth.need_user_info
def article_upload():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        try:
            json = request.json
            with switch_db(models.Article, "default"):
                article = models.Article(**json)
                article.students = [g.uid]
                article.authors = [g.display_name]
                article.favoured = 0
                article.draft = True

                article.last_updated = datetime.utcnow()

                article.save()

                folder_path = os.path.join(current_app.config['UPLOAD_FOLDER'], str(article.id))
                os.mkdir(folder_path)
 
                return str(article.id)
            
        except Exception as e:
            return str(e), 400

    else:
        return 'Content-Type not supported!'

articles_blueprint.register_blueprint(upload.articles_upload, url_prefix='/upload')
articles_blueprint.register_blueprint(modify.article_modify, url_prefix='/modify')