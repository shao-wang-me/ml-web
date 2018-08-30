import pandas as pd
import sqlite3
from sqlalchemy import create_engine

from web_utils import clean_tweet, get_db_data

# get the tweets from streaming database
tweets = get_db_data('?.db', 'SELECT tweet, created_at FROM ')

# create the preprocessed pandas dataframe for tweets
clean_tweets = []
tweets_datetime = []
for tweet in tweets:
    clean_tweets.append(clean_tweet(tweet[0]))
    tweets_datetime.append(tweet[1])

preprocessed_dict = {'tweet': clean_tweets, 'date': tweets_datetime}
preprocessed_df = pd.DataFrame(preprocessed_dict)
preprocessed_df.date = pd.to_datetime(preprocessed_df.date)


# store the preprocessed tweets into database
try:
    engine = sqlite3.connect('preprocessed_tweets.db')
    preprocessed_df.to_sql('preprocessed_tweets', con=engine, if_exists='replace')

except:
    engine = create_engine('sqlite:///preprocessed_tweets.db')
    preprocessed_df.to_sql('preprocessed_tweets', con=engine)
