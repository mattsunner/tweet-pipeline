import json
import time
from dateutil import parser
import os

import mysql.connector as mysql
from configparser import ConfigParser
from pathlib import Path

import tweepy
from dotenv import load_dotenv

# Env Variable Loading
load_dotenv()

HOST = os.getenv("HOST")
USER = 'root'  # TODO: Troubleshoot 'root' env variable loading in as main user
PASSWORD = os.getenv("PASSWORD")
DB = os.getenv("DB")

DATABASE = {
    'host': HOST,
    'user': USER,
    'password': PASSWORD,
    'db': DB
}

CONFIG_FILE = Path.cwd() / "config.cfg"

# Connect to Twitter & Authenticate with Tweepy


def twitter_connect():
    """twitter_connect: Connect to Twitter client using .cfg config file

    Returns:
        obj: Twitter/Tweepy auth object
    """

    config = ConfigParser()
    config.read(CONFIG_FILE)

    auth = tweepy.OAuthHandler(config.get(
        "twitter", "consumer_key"), config.get("twitter", "consumer_secret"))
    auth.set_access_token(config.get("twitter", "access_token"),
                          config.get("twitter", "access_token_secret"))

    twitter = tweepy.API(auth, wait_on_rate_limit=True,
                         wait_on_rate_limit_notify=True)

    return twitter

# Stream Listerner Class


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

# Connect to Database (MySQL)


def connect_db(database):
    """connect_db: Connect to a given database, based on input params

    Args:
        database(dict): Dict of MySQL connection details

    Returns:
        dbconnect: MySql database connection object
    """
    try:
        dbconnect = mysql.connect(
            host=database.get("host"),
            user=database.get("user"),
            password=database.get("password"),
            db=database.get("db"),
        )
        print(f'Connection to host successful')
        return dbconnect
    except mysql.Error as e:
        print(e)


def create_table(database, table_name):
    """create_table: Create a new MySQL table

    Args:
        database (dict): Dict of MySQL connection details
        table_name (str): String of new table name 
    """

    dbconnect = connect_db(database)
    cursor = dbconnect.cursor()

    cursor.execute("USE twitterdb")
    cursor.execute(f"DROP TABLE IF EXISTS {table_name}")

    query = (
        f"CREATE TABLE `{table_name}` ("
        "  `id` INT(11) NOT NULL AUTO_INCREMENT,"
        "  `user` varchar(100) NOT NULL ,"
        "  `created_at` timestamp,"
        "  `tweet` varchar(255) NOT NULL,"
        "  `retweet_count` int(11) ,"
        "  `id_str` varchar(100),"
        "  PRIMARY KEY (`id`))"
    )

    cursor.execute(query)
    dbconnect.close()
    cursor.close()


def populate_table(
    user, created_at, tweet, retweet_count, id_str, my_database=DATABASE
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


def main():
    create_table(DATABASE, 'tweets')

    twitter = twitter_connect()

    StreamListener = CustomListener()
    tweetStream = tweepy.Stream(
        auth=twitter.auth, listener=StreamListener, timeout=30)

    start_stream(tweetStream, track=["python"])


if __name__ == "__main__":
    main()
