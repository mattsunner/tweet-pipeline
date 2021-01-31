import os
import json
from dateutil import parser

from dotenv import load_dotenv
from pathlib import Path
import tweepy
from twitter_connection import twitter_connect, populate_table, start_stream
from mysql_connection import create_table
from env_loading import env_load


CONFIG_FILE = Path.cwd() / "../config.cfg"


class CustomListener(tweepy.StreamListener):
    def on_error(self, status_code):
        if status_code == 420:
            return False

    def on_status(self, status):
        print(status.text)
        return True

    def on_data(self, data):
        try:
            raw_data = json.loads(data)

            if "text" in raw_data:
                user = raw_data["user"]["screen_name"]
                created_at = parser.parse(raw_data["created_at"])
                tweet = raw_data["text"]
                retweet_count = raw_data["retweet_count"]
                id_str = raw_data["id_str"]

            populate_table(user, created_at, tweet,
                           retweet_count, id_str)
            print(f"Tweet colleted at: {created_at}")

        except Exception as e:
            print(e)


def main():
    create_table(env_load(), 'tweets')

    twitter = twitter_connect(CONFIG_FILE)

    StreamListener = CustomListener()
    tweetStream = tweepy.Stream(
        auth=twitter.auth, listener=StreamListener, timeout=30)

    start_stream(tweetStream, track=["python"])


if __name__ == "__main__":
    main()
