import tweepy
from bs4 import BeautifulSoup
import requests
import json
import urllib.request
import re
import time

from tweepy_keys import *


auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)


# def defineWord(word):
#     try:
#         page = requests.get("https://www.merriam-webster.com/dictionary/" + str(word))
#         soup = BeautifulSoup(page.content, 'html.parser')
#         info = soup.find(class_="vg")
#         text = info.find(class_='dtText').get_text()
#         text=text[2:]
#         word_type = soup.find(class_='fl').get_text()
#         # print(text)
#         # print(word_type)
# #         return str(word) + ' (' + word_type + '): ' + text
    # except:
    #         return str(word) + ": We're not sure about this one..."

def defineWord(word):
    keyfile = open(r"C:\Users\noahk\DefineEveryWord\mwkey.txt", 'r')
    keys = keyfile.readline()
    word = str(word)
    phrase = "In case you didn't know..."
    result=[]
    urlfrmt = "https://dictionaryapi.com/api/v3/references/collegiate/json/"+word+"?key=" + keys
    response = urllib.request.urlopen(urlfrmt)
    jsStruct = json.load(response)
    if jsStruct == []:
        return word + ": We're not too sure about this one..."

    print(jsStruct)
    for meaning in jsStruct:
        definitions = meaning['shortdef']
        # if meaning['meta']['id'] != word:
            # print("\n"+meaning['meta']['id'])
        # try:
        # print('('+meaning['fl']+')')
        for i, eachDef in enumerate(definitions, 1):
            result.append(str(i) + ". " + eachDef)
        try:
            return (phrase + '\n' +
                    word + ' ('+meaning['fl']+'): ' + '\n' +
                    result[0] + '\n' +
                    result[1] + '\n' +
                    result[2])
        except:
            try:
                return (phrase + '\n' +
                        word + ' ('+meaning['fl']+'): ' + '\n' +
                        result[0] + '\n' +
                        result[1])
            except:
                return (phrase + '\n' +
                        word + ' ('+meaning['fl']+'): ' + '\n' +
                        result[0])


        

    # print("\nUsage")

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

def replyToTweet():
    filename = r'C:\Users\noahk\DefineEveryWord\last_seen_id.txt'
    stuff = api.user_timeline(screen_name = 'fckeveryword', count = 1)
    most_recent = stuff[0]
    last_seen_id = get_last_id(filename)
    if most_recent.id_str != last_seen_id:
        store_last_id(most_recent.id_str, filename)
        text = most_recent.text
        words = text.split()
        word = words[1]
        definition = defineWord(word)
        print(definition)
        if len(definition) >= 266:
            definition = definition[:266]
        api.update_status(status = '@' + 'fckeveryword' + ' ' + definition, in_reply_to_status_id = most_recent.id_str)

# while(True):
#     start = time.time()
#     replyToTweet()
#     end = time.time()
#     time.sleep(1800-(end-start)+0.01)

replyToTweet()
