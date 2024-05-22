import requests
from flask import render_template, request, Blueprint, jsonify
from flaskblog.models import Post
from flaskblog import db
import sqlite3 

main = Blueprint('main', __name__)

TOP_STORIES_URL = 'https://hacker-news.firebaseio.com/v0/topstories.json?print=pretty'
ITEM_URL = 'https://hacker-news.firebaseio.com/v0/item/{}.json?print=pretty'

def get_top_stories():
    response = requests.get(TOP_STORIES_URL)
    return response.json()

def get_news_data(news_id):
    url = ITEM_URL.format(news_id)
    response = requests.get(url)
    return response.json()
    
def create_table(conn):
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS news (
            id INTEGER PRIMARY KEY,
            title TEXT,
            url TEXT
        )
    """)
    conn.commit()

def insert_into_db(conn, news_data):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO news (id, title, url) VALUES (?, ?, ?)", (news_data['id'], news_data['title'], news_data.get('url', '')))
    conn.commit()


@main.route("/")
@main.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts)


@main.route("/about")
def about():
    return render_template('about.html', title='About')
    
    
@main.route("/newsfeed")
def newsfeed():
    news_ids = get_top_stories()

    # Fetch data for the first 5 news IDs for simplicity
    news_data = [get_news_data(news_id) for news_id in news_ids[:5]]

    # You can customize this to fit your data model
    json_data = {
        "news": [
            {
                "id": item.get("id"),
                "title": item.get("title"),
                "url": item.get("url", ""),
            }
            for item in news_data
        ]
    }

    return jsonify(json_data)
