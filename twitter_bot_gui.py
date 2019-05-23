#!/usr/bin/python
#twitter_bot_gui.py

'''This is a GUI that allows a user to control a Twitter bot. The functions 
include: generating a random Tweet based off of an existing user's activity 
using Markov Chains, creating a Tweet using microphone input and a speech to 
text recognition library, posting a Tweet, and viewing the bot's account.'''

__author__ = "Beth Fineberg"
__version__ = "1.0"

import speech_recognition as sr

import time

import webbrowser

import tweepy
import generate_tweets

from PIL import Image, ImageTk

import tkinter as tk
root = tk.Tk()

root.title("Twitter Bot Controller")

#sets up dimensions of window
w = 593 
h = 420
x = 20
y = 20

root.geometry('%dx%d+%d+%d' % (w, h, x, y))
root.configure(background="#e5ecf0")

#I tried my best with the icon, but I think it's literally impossible with a Mac
#https://stackoverflow.com/questions/48981184/set-window-icon-tkinter-macosx?rq=1
root.iconbitmap("icon_256x256.icns")

#creates tools to recognize speech from microphone input
r = sr.Recognizer()
mic = sr.Microphone()

#keys from my Twitter developer account necessary to use API and post Tweets
consumer_key = 'TnezN4tSh4k31qwFJyr2COJEv'
consumer_secret = 'uxICLrtpi2xPQxU2V6MAZvpUN3Z91sEwWK40v6J4SNE7UFN8BB'
access_token = '1114591239956041735-06izeRmbq34uQ9coZYrvgCkCfgGwFk'
access_token_secret = 'WmZFhfvCam2Gt7s9r6bvtKezUNl9BHA8WU1CSA5J2IAfI'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)
user = api.me()

def record_speech():
    """
    Activates microphone to uses recognition library to display recognized 
    speech in TKinter window. I used online tutorials to understand how to do 
    this.
    """
    tweet.delete(1.0, 'end')
    
    with mic as source:
        audio = r.listen(source)
        
    speech = r.recognize_google(audio)   
    
    tweet.insert("end", speech)
    
def post_tweet():
    """
    Posts Tweet on the status of my bot's account. Makes sure that Tweet is 
    under 280 character limit.
    """
    inputted_text = tweet.get(1.0, "end")
    
    if len(inputted_text) > 280:
        inputted_text = inputted_text[0:280]
        
    api.update_status(inputted_text)
    
def see_account():
    """
    Opens a webbrowser window that allows you to view the bot's account and its
    posted Tweets.
    """
    webbrowser.open('https://twitter.com/beths_bot')
    
def generate_tweet():
    """
    Uses methods from generate_tweets module to use Markov Chains to mimic the
    Twitter user specified within the textfield.
    """
    user_name = tweet.get("1.0", "end")
    
    if user_name != "" and user_name != instructions:
        #note: for some reason line continuation with \ is causing errors for me
        #randomly this gives off an error I don't understand
        generated_tweet = generate_tweets.get_tweets(user_name, consumer_key, consumer_secret, access_token, access_token_secret)
        
        tweet.delete(1.0, "end")
        tweet.insert("end", generated_tweet)
    else:
        tweet.delete(1.0, "end")
        tweet.insert("end", "Your input is not valid. Please try again")        

def quit():
    """
    Quits app and stops tkinter window from running.
    """       
    root.destroy()

img = ImageTk.PhotoImage(Image.open("top_banner.png"))
panel = tk.Label(root, image=img, background="#e5f5fe")
panel.grid(row=0, column=0)

record_button = tk.Button(text = "Record Speech", command=record_speech, highlightbackground="#e5ecf0", font=("HelveticNeue", 14, "bold"))
record_button.grid(row=1, column=0, padx=10, pady=10, sticky="W")

generate_button = tk.Button(text = "Mimic User", command=generate_tweet, highlightbackground="#e5ecf0", font=("HelveticNeue", 14, "bold"))
generate_button.grid(row=1, column=0, padx=10, pady=10, sticky="E")

see_account_button = tk.Button(text = "See Bot's Account", command=see_account, highlightbackground="#e5ecf0", font=("HelveticNeue", 14, "bold"))
see_account_button.grid(row=2, column=0, padx=10, pady=10, sticky="W")

post_button = tk.Button(text = "Post Tweet", command=post_tweet, highlightbackground="#e5ecf0", font=("HelveticNeue", 14, "bold"))
post_button.grid(row=2, column=0, padx=10, pady=10, sticky="E")

tweet = tk.Text(root, height=8, width=50, bg="#ffffff", wrap="word", font=("HelveticNeue", 16), highlightthickness=7)
tweet.grid(row=3, column=0, pady=20)

'''
I wanted to add a picture to make it look more like Twitter, but I couldn't get 
it to work properly. I did try to use code from the internet to figure this out.

image_file = Image.open("profile.png")
image_usable = ImageTk.PhotoImage(image_file)
tweet.image_create("current",image=image_usable)
'''

#I used """, because it created errors with "
instructions = """Press \"Record Speech\" to record a tweet using your \
microphone. Enter in a username, then press \"Mimic User\" to generate a tweet \
in their style. Press \"Post Tweet\" to post a tweet of what is in this box to \
the bot's account."""
tweet.insert("end", instructions)

quit_button = tk.Button(text = "Quit", command=quit, highlightbackground="#e5ecf0", font=("HelveticNeue", 14, "bold"))
quit_button.grid(row=4, column=0, padx=10, pady=10)


root.mainloop()