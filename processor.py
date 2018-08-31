import datetime, pickle

import spacy
from gensim import models, corpora

from web_utils import get_db_data

# get the current time(utc) and the one-hour-before current time
now = datetime.datetime.utcnow()
now_str = '\'' + str(now) + '\''
before = now - datetime.timedelta(hours=1)
before_str = '\'' + str(before) + '\''

# select the tweets between these dates
execution = 'SELECT tweet FROM preprocessed_tweets WHERE date BETWEEN ' + before_str + ' AND ' + now_str
tweets_clean = get_db_data('preprocessed_tweets.db', execution)


# generate nlp object
def generate_nlp_object():
    nlp = spacy.load('en')

    texts = []
    for tweet in tweets_clean:
        text = []
        doc = nlp(tweet[0])

        my_stop_words = ['']

        for stopword in my_stop_words:
            stop = nlp.vocab[stopword]
            stop.is_stop = True
            stop = nlp.vocab[stopword.lower()]
            stop.is_stop = True

        for w in doc:
            if not w.is_stop and not w.is_punct and not w.like_num and w.lemma_ != '-PRON-' and len(w) > 3:
                text.append(w.lemma_)

        texts.append(text)

    bigram = models.Phrases(texts)
    texts = [bigram[line] for line in texts]
    dictionary = corpora.Dictionary(texts)
    # dictionary.filter_extremes(no_below=10, no_above=0.8)
    corpus = [dictionary.doc2bow(text) for text in texts]

    return texts, dictionary, corpus


texts, dictionary, corpus = generate_nlp_object()


# Use LDA to generate topics
def generate_topics_lda(num_topics=1):
    lda_model = models.LdaModel(corpus=corpus, num_topics=num_topics, id2word=dictionary)
    return lda_model


model = generate_topics_lda()
topics_list = model.show_topics()

# store the generated topics into pickle file
now_name = str(now.month) + str(now.day) + str(now.hour) + str(now.minute) + str(now.second)
before_name = str(before.month) + str(before.day) + str(before.hour) + str(before.minute) + str(before.second)
pickle_name = now_name + '-' + before_name + '.pkl'
pickle_out = open(pickle_name, 'wb')
pickle.dump(topics_list, pickle_out)
pickle_out.close()
