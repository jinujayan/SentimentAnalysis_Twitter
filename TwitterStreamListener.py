import twitter
import json
from textblob import TextBlob
import re
import tweepy
import sys
from tweepy.streaming import StreamListener

class StreamListenerImpl(tweepy.StreamListener):

    def __init__(self,api):
        tweepy.StreamListener.__init__(self)
        self.api = api

    def on_data(self, data):
        try:
            print("Inside on On Data")
            #print(data)
            #json_str = json.dumps(data)
            #print(json_str)

            jsonobj = json.loads(data)
            #print("Show encoded string...")
            #print(jsonobj['extended_tweet'].encode('utf8'))

            #print(jsonobj)
            user_name = jsonobj['user']['name']
            screenName = jsonobj['user']['screen_name']

            print("The user and screen names are {}, {}".format(user_name, screenName))
            if "extended_tweet" in data:
                print("Found extended tweet")
                #exttweet = jsonobj['extended_tweet']['full_text']
                #print(str(status).split('\"full_text\":\"')[0])
                #print("---------------------------------------------------------")
                #print(str(status).split('full_text\': ')[1])
                fullTweet = data.split('\"full_text\":\"')[1].split('\",')[0]
                #print(fullTweet)
                #fullTweet = exttweet
                #print(fullTweet.encode('utf8'))
                tweettext = fullTweet
            else:
                # json_str = json.dumps(status._json)
                # jsonobj = json.loads(json_str)
                tweettext = jsonobj['text']
            print(tweettext.encode('utf8'))
            lang_blob = TextBlob(tweettext)
            lang = lang_blob.detect_language()
            print("The language detected is {}".format(lang))

            if lang != 'en':
                print("Translated text to follow")
                sent_blob = lang_blob.translate(to='en')
                print(sent_blob)
            else:
                sent_blob = TextBlob(tweettext)
            print(sent_blob.sentiment)
            tweetSentiment = StreamListenerImpl.evaluateSentiment(sent_blob.sentiment.polarity,
                                                                  sent_blob.sentiment.subjectivity)
            print("The sentiment identified is {}".format(tweetSentiment))
            print("------------------------------------------------------------------------")

            if "NEGATIVE" in tweetSentiment:
                msg = "Hello " + user_name + ", \nPlease share your phone number for us to quickly check on the issue"
                self.api.send_direct_message(screen_name=screenName, text=msg)
                print("DM successfully sent")

            return True
        except Exception as e:
            print(repr(e))
            print("Oops!", sys.exc_info()[0], "occured.")



    def evaluateSentiment (polarity, subjectivity):
        if (polarity < 0 and subjectivity <= 0.6):
            sentiment = "NEGATIVE"
            #print("Sentiment analyzed as NEGATIVE")
        elif (polarity < 0 and subjectivity > 0.6):
            sentiment = "HIGLY NEGATIVE"
            #print("Sentiment analyzed as HIGLY NEGATIVE")
        elif (polarity == 0 and subjectivity == 0):
            sentiment = "HIGLY NEUTRAL"
            #print("Sentiment analyzed as HIGLY NEUTRAL")
        elif (polarity > 0 and subjectivity > 0.6):
            sentiment = "HIGLY POSITIVE"
            #print("Sentiment analyzed as HIGLY POSITIVE")
        elif (polarity > 0 and subjectivity <= 0.6):
            sentiment = "POSITIVE"
            #print("Sentiment analyzed as POSITIVE")
        else:
            sentiment = "NEUTRAL"
            #print("Sentiment analyzed as NEUTRAL")
        return sentiment

    def on_disconnect(self, notice):
        print("Connection lost!! : ", notice)

    def on_error(self, status_code):
        if status_code == 420:
            return False

    def main(self):
        print("This is the main of imported class")

