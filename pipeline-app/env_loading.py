import os

from dotenv import load_dotenv


def env_load():
    load_dotenv()

    HOST = os.getenv("HOST")
    USER = os.getenv("USER")
    PASSWORD = os.getenv("PASSWORD")
    DB = os.getenv("DB")

    DATABASE = {
        'host': HOST,
        'user': USER,
        'password': PASSWORD,
        'db': DB
    }

    return DATABASE
