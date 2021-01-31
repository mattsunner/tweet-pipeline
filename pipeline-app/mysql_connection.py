import time
from dateutil import parser
import os

import mysql.connector as mysql


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
