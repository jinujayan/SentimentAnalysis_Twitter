import twitter
import json
from textblob import TextBlob
import re
import tweepy
import sys
import time
import threading
from tweepy.streaming import StreamListener

class DMHandler:

    def __init__(self, api, id):
        self.currid = id
        self.api = api

        print("In the DM handler init method....")
        thread = threading.Thread(target=self.handleCurrentDM, args=())
        thread.daemon = True
        thread.start()

    def handleCurrentDM(self):
        sinceid = self.currid
        while (True):
            print("Firing in now.....")
            query = self.api.direct_messages(since_id = sinceid, full_text = True)
            #print("Show the DM msg count now ---> {}".format(len(query)))
            if len(query) > 0:
                print("New DM scenario...start processing")
                for msg in query:
                    print(msg)
                    print(msg.text)
                    out = re.findall('([0-9]{12}|[0-9]{10})', msg.text)
                    print("The Customer number retrieved is -> {}".format(out[0]))
                print("Sleeping now.....")
                time.sleep(10)
                self.currid = query[0].id_str
                sinceid = self.currid
                print("The sinceid used for next run is {}".format(self.currid))
            else:
                print("No new DMs received for the run")
                print("Sleeping now.....")
                time.sleep(10)
            print("--------------END OF DM POLL-----------------")


