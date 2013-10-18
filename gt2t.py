#!/usr/bin/python -Wignore::DeprecationWarning

import xmpp
import twitter
import time
import sys

# GTALK
_SERVER  = 'talk.google.com', 5223
USERNAME = ''
PASSWORD = ''
TARGET   = ''

# TWITTER
# Get consumer and access info at 
# https://dev.twitter.com/apps/new
twitter_name    = ''
consumer_key    = ''
consumer_secret = ''
access_key      = ''
access_secret   = ''

api = None

# Get gmail status
def getStatus(username=USERNAME, password=PASSWORD,target=TARGET):
    jid = xmpp.protocol.JID(username)
    client = xmpp.Client(jid.getDomain(), debug=[])
    if not client:
      print 'Connection failed!'
      return
    con = client.connect(server=_SERVER)
    print 'connected with', con
    auth = client.auth(jid.getNode(), password, 'gt2t')
    if not auth:
      print 'Authentication failed!'
      return
    client.sendInitPresence()
    roster = client.getRoster()
    t = time.time() + 1
    while time.time() < t:
        client.Process(1)
        time.sleep(0.1)
    status = roster.getStatus(target)
    client.disconnect()
    return status

# Get twitter timeline
def getTimeLine():
    global api
    api = twitter.Api(consumer_key=consumer_key, consumer_secret=consumer_secret,
                    access_token_key=access_key, access_token_secret=access_secret,
                    input_encoding=None)
    return api.GetUserTimeline(twitter_name)

def main():
    print time.asctime( time.localtime(time.time()) )
    status = getStatus()
    timeLine = getTimeLine()
    if not timeLine is None and not status is None:
        if not any(status[0:99] in tweet.text for tweet in timeLine):
            while len(status) > 140:
                tweet = api.PostUpdate(status[0:139])
                print "posted: " + tweet.text
                status = status[140:]
            api.PostUpdate(status)
            print "Finished Posting"
        else:
            print "No reposts: " + status
    else:
        print "Error"
    print "Fin."

if __name__ == "__main__":
  main()
