import requests
from datetime import datetime
from flaskblog import db
from models import Post

class HackerNewsFetcher:
    TOP_STORIES_URL = 'https://hacker-news.firebaseio.com/v0/topstories.json?print=pretty'
    ITEM_URL = 'https://hacker-news.firebaseio.com/v0/item/{}.json?print=pretty'

    def __init__(self):
        self.app = db.create_app()
        self.app.app_context().push()

    def fetch_and_save_news(self):
        # Fetch the latest news IDs
        top_stories_response = requests.get(self.TOP_STORIES_URL)
        top_stories = top_stories_response.json()

        # Iterate over each news ID and fetch the relevant JSON data
        for story_id in top_stories:
            item_response = requests.get(self.ITEM_URL.format(story_id))
            item_data = item_response.json()

            # Save the news data into the database
            post = Post(
                title=item_data.get('title', 'No Title'),
                content=item_data.get('url', 'No Content'),
                date_posted=datetime.utcnow()
            )
            db.session.add(post)

        # Commit changes
        db.session.commit()

    def get_latest_news_json(self):
        # Fetch the saved data from the database and convert it to a list of dictionaries
        posts_data = Post.query.all()
        return [{'title': post.title, 'content': post.content, 'date_posted': post.date_posted} for post in posts_data]