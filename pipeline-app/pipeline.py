import json
import time
from dateutil import parser

import mysql.connector as mysql
from configparser import ConfigParser
from pathlib import Path

import tweepy

# Connect to Twitter & Authenticate with Tweepy


def twitter_connect(config_file):
    """twitter_connect: Connect to Twitter client using .cfg config file

    Returns:
        obj: Twitter/Tweepy auth object
    """

    CONFIG_FILE = Path.cwd() / f"{config_file}"

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
        """
        Automatic detection of the kind of data collected from Twitter
        This method reads in tweet data as JSON and extracts the data we want.
        """
        try:
            # parse as json
            raw_data = json.loads(data)

            # extract the relevant data
            if "text" in raw_data:
                user = raw_data["user"]["screen_name"]
                created_at = parser.parse(raw_data["created_at"])
                tweet = raw_data["text"]
                retweet_count = raw_data["retweet_count"]
                id_str = raw_data["id_str"]

            # insert data just collected into MySQL my_database
            populate_table(user, created_at, tweet, retweet_count, id_str)
            print(f"Tweet colleted at: {created_at}")

        except Error as e:
            print(e)

# Connect to Database (MySQL)
# TODO: Move 'localhost' results to a dotenv file for deployment to prod.


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

    # Update the SQL statement based on needed database
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


def main():
    DATABASE = {
        'host': 'localhost',
        'user': 'root',
        'password': '',
        'db': 'twitterdb'
    }


if __name__ == "__main__":
    main()
