from datetime import datetime
from flask import Blueprint, g, current_app, request
from mongoengine.context_managers import switch_db
import requests
import auth
import models
import os

article_modify = Blueprint('/modify', __name__,)

def from_documents_to_json(documents):
    return '[%s]' % (','.join([doc.to_json() for doc in documents]))

@article_modify.route('/<article_id>/share/<user_id>', methods=['GET'])
@auth.is_authorized
def share_article(article_id, user_id):
    try:
        url = os.path.join(current_app.config["APP_API_URL"], "user", user_id)
        headers = {'Authorization': g.authorization}
        req = requests.get(url, headers=headers)
        if not req.status_code == 200:
            return "Unknown User ID", 400

        json_data = req.json()

        with switch_db(models.Article, "default"):
            article: models.Article = models.Article.objects.get(id=article_id)
            students = article.students
            if not g.uid == students[0]:
                return "You are not the owner of this article!", 400
            if user_id in students:
                return "User already has edit access!", 400
            students.append(json_data["user_id"])
            authors = article.authors
            authors.append(json_data["display_name"])
            article.update(students=students, authors=authors)
            print(article.students)
            return {
                'students': students,
                'authors': authors
            }
    except Exception as e:
        return ("Failed to get user info!\n" + str(e)), 401

@article_modify.route('/<article_id>/unshare/<user_id>', methods=['GET'])
@auth.is_authorized
def unshare_article(article_id, user_id):
    with switch_db(models.Article, "default"):
        article: models.Article = models.Article.objects.get(id=article_id)
        students = article.students
        if not g.uid == students[0]:
            return "You are not the owner of this article!", 400
        if not user_id in students:
            return "User already doesn't has edit access!", 400
        if g.uid == user_id:
            return "You can not remove your own access!", 400
        student_index = students.index(user_id)
        del students[student_index]
        authors = article.authors
        del authors[student_index]
        article.update(students=students, authors=authors)
        return {
            'students': students,
            'authors': authors
        }

@article_modify.route("/<article_id>", methods=['POST'])
@auth.is_authorized
def article_upload(article_id):
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        try:
            json = request.json
            print(json)
            with switch_db(models.Article, "default"):
                article: models.Article = models.Article.objects.get(id=article_id)
                if not g.uid in article.students:
                    return "You don't have edit access!", 400
                json.pop('_id', None)
                json.pop('students', None)
                json.pop('authors', None)
                json.pop('created', None)
                json.pop('last_updated', None)
                json.pop('favoured', None)
                json.pop('draft', None)
                json.pop('type', None)

                article.update(
                    **json,
                    last_updated=datetime.utcnow()
                )
 
                article: models.Article = models.Article.objects.get(id=article_id)
                return article.to_json()
            
        except Exception as e:
            return str(e), 400

    else:
        return 'Content-Type not supported!'