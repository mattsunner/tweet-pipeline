import json
import time
import os

import mysql.connector as mysql
from configparser import ConfigParser
import tweepy


from mysql_connection import connect_db
from env_loading import env_load


def twitter_connect(config_file):
    """twitter_connect: Connect to Twitter client using .cfg config file

    Returns:
        obj: Twitter/Tweepy auth object
    """

    config = ConfigParser()
    config.read(config_file)

    auth = tweepy.OAuthHandler(config.get(
        "twitter", "consumer_key"), config.get("twitter", "consumer_secret"))
    auth.set_access_token(config.get("twitter", "access_token"),
                          config.get("twitter", "access_token_secret"))

    twitter = tweepy.API(auth, wait_on_rate_limit=True,
                         wait_on_rate_limit_notify=True)

    return twitter


def populate_table(
    user, created_at, tweet, retweet_count, id_str, my_database=env_load()
):
    """Populate table with collected data from Twitter

    Args:
        user (str): username from the status
        created_at (datetime): when the tweet was created
        tweet (str): text
        retweet_count (int): number of retweets
        id_str (int): unique id for the tweet
    """

    dbconnect = connect_db(my_database)

    cursor = dbconnect.cursor()
    cursor.execute("USE twitterdb")

    query = "INSERT INTO tweets(user, created_at, tweet, retweet_count, id_str) VALUES(%s,%s,%s,%s,%s)"

    args = (user, created_at, tweet, retweet_count, id_str)

    try:
        cursor.execute(query, args)
        dbconnect.commit()
        print("commited")

    except mysql.Error as e:
        print(e)
        dbconnect.rollback()

    cursor.close()
    dbconnect.close()

    return


def start_stream(stream, **kwargs):
    """Start the stream, prints the disconnection error

    Args:
        stream (obj): stream object to start
    """

    try:
        stream.filter(**kwargs)
    except Exception:
        stream.disconnect()
        print("Fatal exception")
