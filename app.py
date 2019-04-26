import twitter
import json
import time
from textblob import TextBlob
import re
import tweepy
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy import API
import sys
#from tweepy.streaming import StreamListener
from SentimentAnalysis.TwitterStreamListener import StreamListenerImpl
from SentimentAnalysis.DMHandler import DMHandler



def main():
    consumer_key = '---enter consumer key----'
    consumer_secret = '---enter consumer secret-----'
    access_token_key = '-----enter access token key-----'
    access_token_secret = '-----enter access token secret-----'

    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token_key, access_token_secret)
    api = API(auth)

    print(api.me().name)

    print("Going for DM query now")
    query = api.direct_messages()
    print(query[0])
    print(query[0].id_str)

    curid = query[0].id_str

    dmInstance = DMHandler(api, curid)
    #dmInstance.handleCurrentDM()
    print("Going for stream launching now....")
    stream_listener = StreamListenerImpl(api)
    stream = Stream(auth, stream_listener, verify= True)

    stream.filter(track=["@WindItalia", "WindTre", "winditalia", "#WindTre", "@Tre_It", "h3g", "3Italia", "@WindTreOfficial"])
    #stream.filter(track=["#skadeftzung4534"])
    #stream.userstream()


    #dmsgs = api.direct_messages(count = 100, full_text = True)
    #for msg in dmsgs:
        #print(msg)



if __name__ == '__main__':
    main()