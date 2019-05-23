#!/usr/bin/python
#generate_tweets.py

'''This file contains a method that allows a tweet to be generated based upon a
Markov chain that mimics a Twitter user's posts.

Online resources: 
https://chrisalbon.com/python/other/generate_tweets_using_markov_chain/
https://realpython.com/python-speech-recognition/
https://medium.freecodecamp.org/creating-a-twitter-bot-in-python-with-tweepy-ac524157a607
'''

import tweepy
import markovify

def get_tweets(user_name, consumer_key, consumer_secret, access_token, access_token_secret):
    """
    Generates Tweets that mimic a Twitter user based upon Markov Chains. I used 
    a lot of online tutorials to help figure this out.
    
    :param user_name: Twitter username to mimic
    :param consumer_key: key necessary to use Twitter API
    :param consumer_secret: key necessary to use Twitter API
    :param access_token: key necessary to use Twitter API
    :param access_token_secret: key necessary to use Twitter API
    :return finished_tweet: generated message that is less than 280 characters
    """ 
    
    #authorizes twitter API and initializes tweepy
    authorization = tweepy.OAuthHandler(consumer_key, consumer_secret)
    authorization.set_access_token(access_token, access_token_secret)
    api_handle = tweepy.API(authorization)

    #all tweets from Twitter user
    list_of_tweets = []
    
    try:
        list_of_tweets = api_handle.user_timeline(user_name, count=500, tweet_mode="extended")
    except tweepy.TweepError as error:
        print("An error has occurred: ", error)
    
    #for some reason a ? would always appear at end
    filename = user_name[0:(len(user_name) - 1)] + ".txt"
    file = open(filename, 'w')    
    
    for x in range (0, len(list_of_tweets)):
        file.write(list_of_tweets[x].full_text.replace('\n'," ").strip())
        
        file.write("\n")
    file.close()
    
    with open(filename) as f:
        text = f.read()
        
    text_list = text.split()
    
    clean_text = ''
    #remove unwanted characters and links from Tweets (they hinder Markov chain)
    for i in range(len(text_list)):
        if text_list[i][0:4] != 'http' and text_list[i][0:4] != "&amp":
            clean_text += text_list[i] + " " 
    
    f1 = open(filename, 'w')
    f1.write(clean_text)
    f1.close()
    
    text_model = markovify.Text(clean_text)
    
    #generates tweet that is 280 characters max
    finished_tweet = text_model.make_short_sentence(280)
    
    return finished_tweet