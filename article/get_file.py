from flask import Blueprint, send_from_directory, g, current_app
from mongoengine.context_managers import switch_db
import werkzeug
import auth
import models
import os

article_get_file = Blueprint('/get_file', __name__,)

@article_get_file.route('/<article_id>/<file>', methods=['GET'])
@auth.is_authorized
def get_file(article_id, file):
    article = models.Article.objects.get(id=article_id)
    if g.uid not in article.students:
        return "You do not have edit access to this article.", 401
    filename = werkzeug.utils.secure_filename(file)
    return send_from_directory(os.path.join(current_app.config['UPLOAD_FOLDER'], article_id), filename)

