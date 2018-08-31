import pandas as pd
import sqlite3
from sqlalchemy import create_engine

from web_utils import clean_tweet


def preprocess(tweet):
    # create the preprocessed pandas dataframe for tweets
    preprocessed_dict = {'tweet': [clean_tweet(tweet[0])], 'date': [tweet[1]]}
    preprocessed_df = pd.DataFrame(preprocessed_dict)
    preprocessed_df.date = pd.to_datetime(preprocessed_df.date)

    # store the preprocessed tweets into database
    try:
        engine = sqlite3.connect('preprocessed_tweets.db')
        preprocessed_df.to_sql('preprocessed_tweets', con=engine, if_exists='replace')

    except:  # todo: too broad exception cause, do not use bare expect
        engine = create_engine('sqlite:///preprocessed_tweets.db')
        preprocessed_df.to_sql('preprocessed_tweets', con=engine)
