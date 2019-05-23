#!/usr/bin/python
#twitter_bot_testing.py

'''I mainly used this file to test things out and try out things that I found
online. Because this is not really used in my project, I did not clean it up or
comment it well. However, I did keep it for my own reference.

Note: I did make a function that could recognize audio from a .wav file, but I
did not go forward with it, because I didn't think it would be practical.'''

import tweepy
import tkinter as tk

import speech_recognition as sr
import markovify

consumer_key = 'TnezN4tSh4k31qwFJyr2COJEv'
consumer_secret = 'uxICLrtpi2xPQxU2V6MAZvpUN3Z91sEwWK40v6J4SNE7UFN8BB'
access_token = '1114591239956041735-06izeRmbq34uQ9coZYrvgCkCfgGwFk'
access_token_secret = 'WmZFhfvCam2Gt7s9r6bvtKezUNl9BHA8WU1CSA5J2IAfI'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

user = api.me()
print(user.name)

r = sr.Recognizer()


#pacer = sr.AudioFile('20meterPACER_2017.wav')
#with pacer as source:
    #audio1 = r.record(source, duration=4) #offset=4.7, 
    #audio2 = r.record(source, duration=4, offset=.5)
#print(r.recognize_google(audio1), "\n", r.recognize_google(audio2))

mic = sr.Microphone()
#with mic as source:
    #audio = r.listen(source)
    #print(r.recognize_google(audio))

api = tweepy.API(auth)
#api.update_status(r.recognize_google(audio1))

def get_tweets(user_name):
    
    # Authorize twitter API and initialize tweepy
    authorization = tweepy.OAuthHandler(consumer_key, consumer_secret)
    authorization.set_access_token(access_token, access_token_secret)
    api_handle = tweepy.API(authorization)

    # Holds all the returned tweets for a user
    list_of_tweets = []
    
    try:
        list_of_tweets = api_handle.user_timeline(user_name,count=200,tweet_mode="extended")
    except tweepy.TweepError as error:
        print("An error has occurred: ", error)
    
    for i in range(0, len(list_of_tweets)):
        for x in range(0, len(list_of_tweets[i].full_text)):
            print(list_of_tweets[i].full_text.split()[x])
            #if list_of_tweets[i].full_text[x][0:4] == "https":
                #list_of_tweets[x].full_text.strip(x)
    
    filename = user_name + ".txt"
    file = open(filename, 'w')    
    
    for x in range (0, len(list_of_tweets)):
        file.write(list_of_tweets[x].full_text.replace('\n'," ").strip().strip("&amp"))
        
        file.write("\n")
    
    file.close()
    
get_tweets("elonmusk")

with open("elonmusk.txt") as f:
    text = f.read()

text_model = markovify.Text(text)
for i in range(3):
    print(text_model.make_short_sentence(280) + "\n")