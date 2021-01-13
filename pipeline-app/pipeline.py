from sqlite3 import connect
from configparser import ConfigParser
from pathlib import Path

import tweepy

with connect('airflowdb.db') as conn:
    cur = conn.cursor()
    print(cur)


CONFIG_FILE = Path.cwd() / "config.cfg"

config = ConfigParser()
config.read(CONFIG_FILE)

auth = tweepy.OAuthHandler(config.get("twitter", "consumer_key"), config.get("twitter", "consumer_secret"))
auth.set_access_token(config.get("twitter", "access_token"), config.get("twitter", "access_token_secret"))

twitter = tweepy.API(auth)

public_tweets = twitter.home_timeline()

for tweet in public_tweets:
    print(tweet.text)
