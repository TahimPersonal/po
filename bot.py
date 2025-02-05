import requests
import time
import feedparser
from bs4 import BeautifulSoup
from telegram import Bot
from telegram.error import TelegramError
from flask import Flask

# Initialize Flask app
app = Flask(__name__)

# Replace with your Telegram bot token and channel ID
API_TOKEN = '7843096547:AAHzkh6gwbeYzUrwQmNlskzft6ZayCRKgNU'
CHANNEL_ID = '-1002440398569'

# The URL of the RSS feed
RSS_URL = 'https://www.1tamilmv.pm/discover/all.php'

# List to store processed links (you can also save this list in a file or database for persistence)
processed_links = []

# List to store the latest links from the most recent feed check
latest_links = []

# Initialize Telegram Bot
bot = Bot(token=API_TOKEN)

# Function to scrape magnet links from a webpage
def scrape_magnet_link(post_url):
    try:
        response = requests.get(post_url)
        soup = BeautifulSoup(response.content, 'html.parser')
        # Scrape the magnet link (adjust the selector as per the website structure)
        magnet_link = soup.find('a', {'href': lambda x: x and x.startswith('magnet:')})
        if magnet_link:
            return magnet_link['href']
        return None
    except Exception as e:
        print(f"Error scraping magnet link from {post_url}: {e}")
        return None

# Function to send message to Telegram
def send_to_telegram(magnet_link):
    try:
        message = f"/qbleech {magnet_link}\n<b>Tag:</b> <code>@Mr_official_300</code> <code>2142536515</code>"
        bot.send_message(chat_id=CHANNEL_ID, text=message, parse_mode='HTML')
    except TelegramError as e:
        print(f"Error sending message to Telegram: {e}")

# Function to process RSS feed and check for new posts
def process_rss_feed():
    global processed_links, latest_links

    # Parse RSS feed
    feed = feedparser.parse(RSS_URL)

    # Collect the latest links from the current feed
    new_latest_links = []

    for entry in feed.entries:
        post_url = entry.link
        # Scrape the magnet link for the post
        magnet_link = scrape_magnet_link(post_url)
        if magnet_link and post_url not in processed_links:
            new_latest_links.append((post_url, magnet_link))

    # If new posts are found, process them
    if new_latest_links:
        print(f"Found new posts, sending the latest first...")

        # Send the most recent magnet link first
        latest_post = new_latest_links[-1]
        send_to_telegram(latest_post[1])  # Send the magnet link of the latest post
        processed_links.append(latest_post[0])  # Mark this post as processed
        print(f"Latest post sent, waiting for 5 minutes...")

        # Delay for 5 minutes to avoid spamming
        time.sleep(300)

        # Then, send older posts from the same check
        for post_url, magnet_link in reversed(new_latest_links[:-1]):
            send_to_telegram(magnet_link)
            processed_links.append(post_url)  # Mark this post as processed
            print(f"Sent older post: {post_url}")
            time.sleep(300)  # Delay of 5 minutes between posts
    else:
        print("No new posts found, sending old posts...")

        # If no new posts, send from processed links (old ones)
        for post_url in processed_links:
            magnet_link = scrape_magnet_link(post_url)
            if magnet_link:
                send_to_telegram(magnet_link)
                print(f"Sent old post: {post_url}")
                time.sleep(300)  # Delay of 5 minutes between posts

# Flask route for health check
@app.route('/health', methods=['GET'])
def health_check():
    return "OK", 200

# Main function to run the bot
def main():
    print("Bot started...")
    while True:
        process_rss_feed()
        print("Waiting for 10 minutes to check for new posts...")
        time.sleep(600)  # Wait for 10 minutes before checking the feed again

# Run the Flask server
if __name__ == "__main__":
    # Run the Flask health check server in a separate thread or process
    from threading import Thread
    health_thread = Thread(target=lambda: app.run(host='0.0.0.0', port=5000))
    health_thread.start()
    main()
