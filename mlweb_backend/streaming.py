import logging

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tweepy import StreamListener
from tweepy import Stream

from web_utils import set_twitter_app_tokens

# set the log file
logging.basicConfig(filename="streaming.log",
                    level=logging.DEBUG,
                    format="%(asctime)s:%(levelname)s:%(message)s")


base = declarative_base()
table_name = ''
db_name = ''


# set the database class to add streaming tweet
class TweetDb(base):
    __tablename__ = table_name

    index = Column(Integer, primary_key=True)
    tweet = Column(String(500))
    created_at = Column(String(300))
    user_name = Column(String(300))


# create the session for database
engine = create_engine('sqlite:///' + db_name + '.db')
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

        new_data = TweetDb(tweet=status.text,
                           created_at=status.created_at,
                           user_name=status.user.screen_name)

        self.session.add(new_data)
        self.session.commit()

    def on_error(self, status_code):
        if status_code == 420:
            return False


# input the twitter app tokens
twitter_app_tokens = dict(consumer_key='',
                          consumer_secret='',
                          access_token='',
                          access_token_secret='')

# run the streaming
api = set_twitter_app_tokens(twitter_app_tokens)
listener = MyStreamListener(session)
my_stream = Stream(auth = api.auth, listener=listener)
track_words = ['']
my_stream.filter(track=track_words, languages=["en"])