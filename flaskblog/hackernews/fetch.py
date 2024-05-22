import requests
import sqlite3

# Function to get the latest news IDs from HackerNews API
def get_top_stories():
    url = "https://hacker-news.firebaseio.com/v0/topstories.json?print=pretty"
    response = requests.get(url)
    return response.json()

# Function to get news data by ID from HackerNews API
def get_news_data(news_id):
    url = f"https://hacker-news.firebaseio.com/v0/item/{news_id}.json?print=pretty"
    response = requests.get(url)
    return response.json()

# Function to create SQLite table if it doesn't exist
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

# Function to insert news data into SQLite database
def insert_into_db(conn, news_data):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO news (id, title, url) VALUES (?, ?, ?)", (news_data['id'], news_data['title'], news_data.get('url', '')))
    conn.commit()

# Main function to fetch news IDs, retrieve data, and save to SQLite database
def main():
    # Fetch the latest news IDs
    news_ids = get_top_stories()

    # Initialize SQLite database
    conn = sqlite3.connect("hackernews.db")
    create_table(conn)

    # Fetch data for each news ID and save to database
    for news_id in news_ids:
        news_data = get_news_data(news_id)
        insert_into_db(conn, news_data)

    # Close the database connection
    conn.close()

if __name__ == "__main__":
    main()