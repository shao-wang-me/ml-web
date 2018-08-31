# Complete the followings in terminal:
# 1. Install NLP Packages: gensim, spacy
# 2. Run this after spacy is installed: python -m spacy download en


import re

import spacy
from gensim import corpora

def clean_tweet(tweet):
    """
    clean single tweet - no non-alphanumeric characters, no hashtag #, no mention @, no links https://...
    :param tweet: single tweet string
    :return: cleaned single tweet string
    """
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|#[A-Za-z0-9]+|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())


def clean_all_tweets(tweets):
    """
    clean all tweets - based on the function 'clean_tweet()'
    :param tweets - a list contains all tweets. Each tweet is a string.
    :return: cleaned all tweets
    """

    clean_tweets = []
    for tweet in tweets:
        clean_tweets.append(clean_tweet(tweet))

    return clean_tweets


def word_id_mapping_dictionary(cleaned_tweets):
    """
    Create a gensim dictionary for future word-index mapping
    :param cleaned_tweets: a list contains all cleaned tweets.
    :return: gensim corpora dictionary generated from cleaned_tweets
    """

    # load spacy English model
    nlp = spacy.load('en')

    texts = []

    # load each tweet into spacy model
    for tweet in cleaned_tweets:
        text = []
        doc = nlp(tweet)

    # remove stopwords and punctuations, then lemmatization of words
        for w in doc:
            if not w.is_stop and not w.is_punct and w.lemma_ !='-PRON-':
                text.append(w.lemma_)
        texts.append(text)

    # generate the gensim corpora dictionary
    dictionary = corpora.Dictionary(texts)

    return dictionary


if __name__ == '__main__':
    tweets = ['AI is so great! @ShaoWang @YiranLiu #AIThriving http://www.ai.com',
              'What is wrong with AI? I lose a lot of money in this technology! #AISucks']

    cleaned_tweets = clean_all_tweets((tweets))
    dictionary = word_id_mapping_dictionary((cleaned_tweets))
    print(dictionary.token2id)
