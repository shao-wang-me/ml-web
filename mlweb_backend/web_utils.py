import re
import sqlite3

from tweepy import OAuthHandler, API


# set twitter app tokens
def set_twitter_app_tokens(tokens):

    auth = OAuthHandler(tokens['consumer_key'], tokens['consumer_secret'])
    auth.set_access_token(tokens['access_token'], tokens['access_token_secret'])
    api = API(auth)

    return api


# clean tweet
def clean_tweet(text):
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|#[A-Za-z0-9]+|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", text).split())


# connect the database and return all data
def get_db_data(db_path, execute):

    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute(execute)
    tweets = c.fetchall()
    conn.close()

    return tweets

