from flask import Blueprint, request, g, current_app, send_file
import werkzeug
import auth
import models
import os

def allowed_file(filename):
    return '.' in filename 
    # and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

articles_upload = Blueprint('/upload', __name__,)

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
        if g.uid not in article.students and not ("nbscmanlys-h:teacher" in g.scopes or g.uid in current_app.config["ADMINS"]):
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
    if g.uid not in article.students and not ("nbscmanlys-h:teacher" in g.scopes or g.uid in current_app.config["ADMINS"]):
        return "You do not have edit access to this article.", 401
    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], article_id, "index.html")
    print(request.data, file_path)
    f = open(file_path, "w")
    f.write(bytes.decode(request.data))
    return "Yes"

@articles_upload.route('/retrieve/<article_id>/<file_name>', methods=['GET'])
@auth.is_authorized
def retrieve_file(article_id, file_name):
    try:
        article = models.Article.objects.get(id=article_id)
        if g.uid not in article.students and not ("nbscmanlys-h:teacher" in g.scopes or g.uid in current_app.config["ADMINS"]):
            return "You do not have edit access to this article.", 401
        sec_filename = werkzeug.utils.secure_filename(file_name)
        return send_file(os.path.join(current_app.config['UPLOAD_FOLDER'], article_id, sec_filename))
    except Exception as e:
        return str(e), 400

@articles_upload.route('/retrieve/<article_id>/index', methods=['GET'])
@auth.is_authorized
def retrieve_index(article_id):
    try:
        article = models.Article.objects.get(id=article_id)
        if g.uid not in article.students and not ("nbscmanlys-h:teacher" in g.scopes or g.uid in current_app.config["ADMINS"]):
            return "You do not have edit access to this article.", 401
        return send_file(os.path.join(current_app.config['UPLOAD_FOLDER'], article_id, 'index.html'))
    except Exception as e:
        return str(e), 404