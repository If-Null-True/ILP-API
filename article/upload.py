from flask import Blueprint, flash, redirect, request, g, url_for, current_app
from mongoengine.context_managers import switch_db
import werkzeug
import auth
import models
import os


articles_upload = Blueprint('/upload', __name__,)


def allowed_file(filename):
    return '.' in filename 
    # and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@articles_upload.route('/<article_id>/file', methods=['POST'])
@auth.is_authorized
def upload_file(article_id):
    # check if the post request has the file part
    if 'file' not in request.files:
        print('No file part')
        return "No file part uploaded", 400
    file = request.files['file']
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == '':
        print('No selected file')
        return "No file selected", 400
    if file and allowed_file(file.filename):
        article = models.Article.objects.get(id=article_id)
        if g.uid not in article.students:
            return "You do not have edit access to this article.", 401
        filename = werkzeug.utils.secure_filename(file.filename)
        file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], article_id, filename))
        file_url = os.path.join(article_id, filename)
        return file_url
    return "Unknown Error", 500

@articles_upload.route('/<article_id>/index', methods=['POST'])
@auth.is_authorized
def upload_index(article_id):
    article = models.Article.objects.get(id=article_id)
    if not len(request.data):
        return "Invalid index.html contents!", 400
    if g.uid not in article.students:
        return "You do not have edit access to this article.", 401
    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], article_id, "index.html")
    print(request.data, file_path)
    f = open(file_path, "w")
    f.write(bytes.decode(request.data))
    return "Yes"