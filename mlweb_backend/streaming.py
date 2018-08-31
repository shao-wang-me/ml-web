import logging
import sys
import argparse

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tweepy import StreamListener
from tweepy import Stream

from web_utils import set_twitter_app_tokens


# set the database class to add streaming tweet
class TweetDb(base):
    __tablename__ = table_name

    index = Column(Integer, primary_key=True)
    tweet = Column(String(500))
    created_at = Column(String(300))
    user_name = Column(String(300))


# set the streaming listener
class MyStreamListener(StreamListener):
    def __init__(self, sess):
        super().__init__()
        self.session = sess

    def on_status(self, status):
        try:
            if status.retweeted_status:
                return
        except AttributeError:
            pass

        new_data = TweetDb(tweet=status.text,
                           created_at=status.created_at,
                           user_name=status.user.screen_name)

        self.session.add(new_data)
        self.session.commit()

    def on_error(self, status_code):
        if status_code == 420:
            return False


def main(args):
    # set the log file
    logging.basicConfig(filename="streaming.log",
                        level=logging.DEBUG,
                        format="%(asctime)s:%(levelname)s:%(message)s")

    base = declarative_base()

    # create the session for database
    engine = create_engine('sqlite:///' + args.db_name + '.db')
    base.metadata.create_all(engine)
    db_session = sessionmaker(bind=engine)
    session = db_session()

    # input the twitter app tokens
    twitter_app_tokens = dict(consumer_key=args.consumer_key,
                              consumer_secret=args.consumer_secret,
                              access_token=args.access.token,
                              access_token_secret=args.access_token_secrets)

    # run the streaming
    api = set_twitter_app_tokens(twitter_app_tokens)
    listener = MyStreamListener(session)
    my_stream = Stream(auth=api.auth, listener=listener)
    track_words = args.track_words
    my_stream.filter(track=track_words, languages=["en"])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('consumer_key')
    parser.add_argument('consumer_secret')
    parser.add_argument('access_token')
    parser.add_argument('access_token_secret')
    parser.add_argument('table_name')
    parser.add_argument('db_name')
    parser.add_argument('track_words')
    args = parser.parse_args()

    main(args)
