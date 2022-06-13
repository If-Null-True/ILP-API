from flask import Flask
import pymongo
import json
from bson import json_util
from markupsafe import escape

config = {}
with open("config.json", "r") as read_file:
    config = json.load(read_file)

conn_str = f'mongodb://{config["mongodb"]["username"]}:{config["mongodb"]["password"]}@{config["mongodb"]["host"]}/ilp?retryWrites=true&w=majority'
print(conn_str)

# set a 5-second connection timeout
client = pymongo.MongoClient(conn_str, serverSelectionTimeoutMS=5000)
try:
    print("Connected to Mongo Database")
except Exception:
    print("Unable to connect to the server.")

db = client.ilp
articles = db.articles

def jsonify(docs):
    json_docs = [doc for doc in docs]
    return json.dumps(json_docs, default=json_util.default)

app = Flask(__name__)

@app.route("/articles/all", methods=['GET'])
def all_articles():
    return jsonify(articles.find())

@app.route("/articles/student/<student>", methods=['GET'])
def student_article(student):
    return jsonify(articles.find({"student": student}))

@app.route("/articles/category/<category>", methods=['GET'])
def article_category(category):
    return jsonify(articles.find({"category": category}))

@app.route("/articles/tag/<tag>", methods=['GET'])
def article_tag(tag):
    return jsonify(articles.find({"tags": tag}))