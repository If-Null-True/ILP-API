from flask import Blueprint, g, current_app
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
            if user_id in article.students:
                return "User already has edit access!", 400
            students.append(json_data["user_id"])
            authors = article.authors
            authors.append(json_data["display_name"])
            article.update(students=students, authors=authors)
            print(article.students)
            return article.students
    except Exception as e:
        return ("Failed to get user info!\n" + str(e)), 401