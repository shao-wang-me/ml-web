import tweepy
import sys
import sqlite3


class Listener(tweepy.StreamListener):
    def on_data(self, data):
        print(data)
        return True

    def on_error(self, status):
        print(status)


if __name__ == '__main__':
    consumer_key = sys.argv[1]
    consumer_secret = sys.argv[2]
    access_token = sys.argv[3]
    access_token_secret = sys.argv[4]

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    streamListener = Listener()
    stream = tweepy.Stream(auth=auth, listener=streamListener)

    conn = sqlite3.connect('twitter.db')
    c = conn.cursor()
    stream.sample()
    # stream.filter()
