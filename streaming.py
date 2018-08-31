import logging
import argparse
import concurrent.futures

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tweepy import StreamListener
from tweepy import Stream

from web_utils import set_twitter_app_tokens
import preprocessor

# set the log file
logging.basicConfig(filename="streaming.log",
                    level=logging.DEBUG,
                    format="%(asctime)s:%(levelname)s:%(message)s")

# set up arg parser
parser = argparse.ArgumentParser()
parser.add_argument('consumer_key')
parser.add_argument('consumer_secret')
parser.add_argument('access_token')
parser.add_argument('access_token_secret')
parser.add_argument('table_name')
parser.add_argument('db_name')
parser.add_argument('track_words')
args = parser.parse_args()

# set up process pool
process_pool = concurrent.futures.ProcessPoolExecutor(max_workers=5)

base = declarative_base()


# set the database class to add streaming tweet
class TweetDb(base):
    __tablename__ = args.table_name

    index = Column(Integer, primary_key=True)
    tweet = Column(String(500))
    created_at = Column(String(300))
    user_name = Column(String(300))


# create the session for database
engine = create_engine('sqlite:///' + args.db_name + '.db')
base.metadata.create_all(engine)
db_session = sessionmaker(bind=engine)
session = db_session()


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

        # run preprocessor in another thread
        process_pool.submit(fn=preprocessor.preprocess, args=[status.text, status.created_at, status.user.screen_name])

        # save new tweet to database
        # todo: 写数据会不会慢？
        new_data = TweetDb(tweet=status.text,
                           created_at=status.created_at,
                           user_name=status.user.screen_name)

        self.session.add(new_data)
        self.session.commit()

    def on_error(self, status_code):
        if status_code == 420:
            return False


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
