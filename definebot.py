import tweepy
from bs4 import BeautifulSoup
import requests
import json
import urllib.request
import re
import time
import os 

from tweepy_keys import *


auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)


def defineWordBS(word): #beautifulsoup version, web-scrapes in case of TypeError exception
    try:
        page = requests.get("https://www.merriam-webster.com/dictionary/" + str(word))
        soup = BeautifulSoup(page.content, 'html.parser')
        info = soup.find(class_="vg")
        text = info.find(class_='dtText').get_text()
        text=text[2:]
        word_type = soup.find(class_='fl').get_text()
        # print(text)
        # print(word_type)
        return(str(word) + ' (' + word_type + '): ' + text)
    except:
            return str(word) + ": We're not sure about this one... or at least Merriam Webster isn't..."

def defineWord(word):
    keyfile = open(r"C:\Users\noahk\DefineEveryWordBot\mwkey.txt", 'r')
    keys = keyfile.readline()
    word = str(word)
    result=[]
    urlfrmt = "https://dictionaryapi.com/api/v3/references/collegiate/json/"+word+"?key=" + keys
    response = urllib.request.urlopen(urlfrmt)
    jsStruct = json.load(response)
    if jsStruct == []:
        return word + ": We're not too sure about this one... or at least Merriam Webster isn't..."

    for meaning in jsStruct:
        try:
            definitions = meaning['shortdef']
        except TypeError:
            return defineWordBS(word)
        # if meaning['meta']['id'] != word:
            # print("\n"+meaning['meta']['id'])
        # try:
        # print('('+meaning['fl']+')')
        for i, eachDef in enumerate(definitions, 1):
            result.append(str(i) + ". " + eachDef)
        try:
            return (word + ' ('+meaning['fl']+'): ' + '\n' +
                    result[0] + '\n' +
                    result[1] + '\n' +
                    result[2])
        except:
            try:
                return (word + ' ('+meaning['fl']+'): ' + '\n' +
                        result[0] + '\n' +
                        result[1])
            except:
                return (word + ' ('+meaning['fl']+'): ' + '\n' +
                        result[0])


    # print("\nUsage") #For including usage

    # for usage in jsStruct:
    #     try:
    #         longdefs = usage['def']
    #         for i, eachDef in enumerate(longdefs, 1):
    #             if 'sseq' in eachDef:
    #                 # test[*][0][1]['dt'] - gives list of illustrations
    #                 for ill in eachDef['sseq']:
    #                     if 'dt' in ill[0][1]:
    #                         for illus in ill[0][1]['dt']:
    #                             if illus[0] == 'vis':
    #                                 # enumerate
    #                                 for ii in range(1, len(illus)):
    #                                     L = len(illus[ii])
    #                                     for jj in range(L):
    #                                         if 't' in illus[ii][jj]:
    #                                             # remove everything within braces before printing
    #                                             print("* "+illus[ii][jj]['t'])
    #     except KeyError:
    #         return str(word) + ": We're not sure about this one..."

def get_last_id(file_name):
    f_read = open(file_name, 'r')
    last_seen_id = str(f_read.read().strip())
    f_read.close()
    return last_seen_id

def store_last_id(last_seen_id, file_name):
    f_write = open(file_name, 'w')
    f_write.write(str(last_seen_id))
    f_write.close()
    return

# def getImage(word):
#     return img_file


def makeTweets():
    filename = r'C:\Users\noahk\DefineEveryWordBot\last_seen_id.txt'
    last_seen_id = get_last_id(filename)
    stuff = api.user_timeline(screen_name = 'fckeveryword', count = 1)
    most_recent = stuff[0]
    print(most_recent.id_str,last_seen_id,most_recent.id_str==last_seen_id)
    if most_recent.id_str != last_seen_id:
        phrase = "In case you didn't know..."
        text = most_recent.text
        words = text.split()
        word = words[1]
        definition = defineWord(word)
        reply_definition = definition
        # print(definition)
        if len(reply_definition) >= 239:
            reply_definition = reply_definition[:239]
        if reply_definition.split()[1] == "We're":
            api.update_status(status = '@' + 'fckeveryword' + ' ' + '\n' + reply_definition, in_reply_to_status_id = most_recent.id_str)
        else:
            api.update_status(status = '@' + 'fckeveryword' + ' ' + phrase + '\n' + reply_definition, in_reply_to_status_id = most_recent.id_str)
        print("Replying with: " + '\n' + reply_definition)
        if len(definition) >= 247-len(word):
            definition = definition[:247-len(word)]
        tweet_string = 'Yay! @fckeveryword just fucked ' + word + '!' + '\n' + definition
        print("Tweeting out: " + '\n' + tweet_string)
        api.update_status(status = tweet_string)
        store_last_id(most_recent.id_str, filename)
        return 

def main():
    while(True):
        start = time.time()
        makeTweets()
        print("----------TWEETS SENT---------- " + str(time.time()))
        end = time.time()
        time.sleep(1800 - (end-start) + .1)

#function where if someone tweets:

# @DefineAllWords ... #define <word> ...
# we reply to their tweet with the definition, the same as it would be run for the fck bot

# class MyStreamListener(tweepy.StreamListener):

#     def on_status(self, status):
#         print(status.text)

    # def on_error(self, status_code):
    #     if status_code == 420:-
    #         #returning False in on_error disconnects the stream
    #         return False

# myStreamListener = MyStreamListener()
# myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)

# myStream.filter(track=['@DefineAllWords'])

# def main():
#   makeTweets() #for single runs
        
if __name__ == '__main__':
    main()

