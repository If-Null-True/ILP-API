from flask import Flask, g
import articles as articles
from flask_mongoengine import MongoEngine
import settings
import auth

db = MongoEngine()
app = Flask(__name__)
app.config.from_pyfile("config.py")
db.init_app(app)

@app.route("/", methods=['GET'])
@auth.is_authorized
def welcome():
    return f'Welcome to the ILP API. You are {g.uid} and have the scopes: {g.scopes}'    

app.register_blueprint(settings.settings_bp, url_prefix='/settings')
app.register_blueprint(articles.articles_blueprint, url_prefix='/articles')