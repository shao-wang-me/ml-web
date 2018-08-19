import tweepy

consumer_key = None
consumer_secret = None
access_token = None
access_token_secret = None

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)


class Listener(tweepy.StreamListener):
    pass


streamListener = Listener()
stream = tweepy.Stream(auth=auth, listener=streamListener)

stream.sample(async=True)
# stream.filter(async=True)